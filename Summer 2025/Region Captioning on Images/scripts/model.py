import torch
import torch.nn as nn
import torchvision
from torchvision.models.detection import fasterrcnn_resnet50_fpn
import torchvision.models as models
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence

class FasterRCNNRegionDetector(nn.Module):
    """
    Faster R-CNN based region detector.
    It takes a tensor image and returns a
    list of bounding boxes.
    """
    def __init__(self, confidence_threshold=0.5):
        super(FasterRCNNRegionDetector, self).__init__()
        self.confidence_threshold = confidence_threshold
        self.model = fasterrcnn_resnet50_fpn(weights=torchvision.models.detection.FasterRCNN_ResNet50_FPN_Weights.DEFAULT)
        self.model.eval()

    def forward(self, image_tensor):
        """ 
        Args : image_tensor (torch.Tensor): A single image tensor [C, H, W]   
        Returns : torch.Tensor: Filtered bounding boxes [N, 4] where N is the number of boxes found
         """
        if image_tensor.dim() != 3:
            raise ValueError(f"Expected a 3D tensor [C, H, W], but got {image_tensor.shape}")

        # model expects a list of tensors
        with torch.no_grad():
            detections = self.model([image_tensor])
        
        # Detections is a list of dicts, one per image. We only have one.
        det = detections[0]
        
        scores = det['scores']
        boxes = det['boxes']
        
        # Filter by confidence threshold
        keep = scores > self.confidence_threshold
        filtered_boxes = boxes[keep]
        
        return filtered_boxes

# Alignment Models

class AlignmentEncoderCNN(nn.Module):
    """
    Encoder for the alignment model.
    Takes image regions, passes them through CNN (e.g., VGG),
    and applies linear layer to get to embed_size.
    
    NOTE: In the paper, this processes *regions*. Your dataset.py
    is set up to pass *full images*.
    """
    def __init__(self, embed_size):
        super(AlignmentEncoderCNN, self).__init__()
        vgg = models.vgg19(weights=models.VGG19_Weights.DEFAULT)
        self.cnn = nn.Sequential(*list(vgg.features.children()))
        
        self.avgpool = nn.AdaptiveAvgPool2d((7, 7))
        self.fc = nn.Linear(vgg.classifier[0].in_features , embed_size)
        self.init_weights()

    def init_weights(self):
        self.fc.weight.data.normal_(0.0, 0.02)
        self.fc.bias.data.fill_(0)

    def forward(self, images):
        features = self.cnn(images)
        features = self.avgpool(features)
        features = torch.flatten(features, 1)
        features = self.fc(features)
        
        # Normalize features
        features = features / torch.norm(features, p=2, dim=1, keepdim=True)
        return features


class AlignmentDecoderRNN(nn.Module):
    def __init__(self, embed_size, hidden_size, vocab_size, num_layers=1):
        super(AlignmentDecoderRNN, self).__init__()
        self.embed = nn.Embedding(vocab_size, embed_size)
        self.gru = nn.GRU(embed_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, embed_size)
        self.init_weights()

    def init_weights(self):
        self.embed.weight.data.uniform_(-0.1, 0.1)
        self.fc.weight.data.normal_(0.0, 0.02)
        self.fc.bias.data.fill_(0)

    def forward(self, captions, lengths):
        embeddings = self.embed(captions)
        packed = pack_padded_sequence(embeddings, lengths, batch_first=True, enforce_sorted=False)
        
        outputs, _ = self.gru(packed)
        
        # Unpack and get the last relevant output
        unpacked_outputs, _ = pad_packed_sequence(outputs, batch_first=True)
        
        # Get the last valid output for each sequence
        idx = (torch.LongTensor(lengths) - 1).view(-1, 1).expand(
            len(lengths), unpacked_outputs.size(2)
        ).to(captions.device)
        idx = idx.unsqueeze(1)
        last_outputs = unpacked_outputs.gather(1, idx).squeeze(1)
        
        features = self.fc(last_outputs)
        
        # L2-normalize features
        features = features / torch.norm(features, p=2, dim=1, keepdim=True)
        return features

# ----------------------------------------------------------------------------
# Generative Models (MRNN)
# ----------------------------------------------------------------------------

class GenerativeEncoderCNN(nn.Module):
    """
    Encoder for the generative model.
    Takes a full image and produces features.
    """
    def __init__(self, embed_size):
        super(GenerativeEncoderCNN, self).__init__()
        # Use a pre-trained ResNet, but remove the final fc layer
        resnet = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
        modules = list(resnet.children())[:-1] # Remove classifier
        self.resnet = nn.Sequential(*modules)
        
        # Add a linear layer to map to embed_size
        self.fc = nn.Linear(resnet.fc.in_features, embed_size)
        self.bn = nn.BatchNorm1d(embed_size, momentum=0.01)
        self.init_weights()

    def init_weights(self):
        self.fc.weight.data.normal_(0.0, 0.02)
        self.fc.bias.data.fill_(0)

    def forward(self, images):
        with torch.no_grad():
            features = self.resnet(images)
        features = features.reshape(features.size(0), -1)
        features = self.fc(features)
        features = self.bn(features)
        return features


class DecoderMRNN(nn.Module):
    """
    Decoder for the generative model (Multimodal RNN).
    Takes image features and generates a caption.
    """
    def __init__(self, embed_size, hidden_size, vocab_size, num_layers=1):
        super(DecoderMRNN, self).__init__()
        self.embed = nn.Embedding(vocab_size, embed_size)
        
        # LSTM input is concatenation of word embedding and image features
        self.lstm = nn.LSTM(embed_size * 2, hidden_size, num_layers, batch_first=True)
        
        self.fc = nn.Linear(hidden_size, vocab_size)
        self.init_weights()

    def init_weights(self):
        self.embed.weight.data.uniform_(-0.1, 0.1)
        self.fc.weight.data.normal_(0.0, 0.02)
        self.fc.bias.data.fill_(0)

    def forward(self, features, captions, lengths):
        embeddings = self.embed(captions)
        
        # Concatenate image features with each word embedding
        # features shape: [batch_size, embed_size]
        # embeddings shape: [batch_size, seq_len, embed_size]
        # We need to tile image features to match seq_len
        features_tiled = features.unsqueeze(1).repeat(1, embeddings.size(1), 1)
        
        # combined shape: [batch_size, seq_len, embed_size * 2]
        combined = torch.cat((features_tiled, embeddings), dim=2)
        
        packed = pack_padded_sequence(combined, lengths, batch_first=True, enforce_sorted=False)
        
        lstm_out, _ = self.lstm(packed)
        
        # Pass LSTM outputs through the final linear layer
        outputs = self.fc(lstm_out.data)
        
        return outputs

    def sample(self, features, vocab, max_length=20):
        """
        Generate a caption for a given image feature.
        (Used for inference)
        """
        batch_size = features.size(0)
        
        # Hidden state starts with image features
        # We need to format this for LSTM (h_0, c_0)
        # We can just use it to initialize the input, as per paper
        
        # Start token
        inputs = torch.full((batch_size, 1), vocab.word2idx['<start>'],
                            dtype=torch.long, device=features.device)
        
        # We need to maintain hidden state
        h_state, c_state = None, None
        
        caption_ids = []
        
        with torch.no_grad():
            for i in range(max_length):
                embeddings = self.embed(inputs).squeeze(1) # [batch_size, embed_size]
                
                # Concatenate image features (context)
                # features shape: [batch_size, embed_size]
                combined = torch.cat((features, embeddings), dim=1).unsqueeze(1)
                
                if h_state is None:
                    lstm_out, (h_state, c_state) = self.lstm(combined)
                else:
                    lstm_out, (h_state, c_state) = self.lstm(combined, (h_state, c_state))
                
                # Get scores for next word
                outputs = self.fc(lstm_out.squeeze(1)) # [batch_size, vocab_size]
                
                predicted_ids = outputs.argmax(dim=1) # [batch_size]
                caption_ids.append(predicted_ids)
                
                # Check for <end> token
                if (predicted_ids == vocab.word2idx['<end>']).all():
                    break
                
                # Use prediction as next input
                inputs = predicted_ids.unsqueeze(1) # [batch_size, 1]
                
        # Concatenate all predictions
        if caption_ids:
            caption_ids = torch.stack(caption_ids, dim=1)
        else:
            caption_ids = torch.empty(batch_size, 0, dtype=torch.long, device=features.device)
            
        return caption_ids
