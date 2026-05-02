import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import transforms
import pickle
import os

from vocabulary import Vocabulary
from dataset import FlickrDataset, collate_fn
from model import GenerativeEncoderCNN, DecoderMRNN
from train import train_generative_epoch

def main_generative():

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    image_dir = 'Project/data'
    train_captions_file = 'Project/data/captions.txt'
    vocab_path = 'Project/data/vocab.pkl'
    model_save_dir = 'Project/models'

    embed_size = 512
    hidden_size = 512
    num_epochs = 75
    batch_size = 128
    learning_rate = 0.003

    os.makedirs(model_save_dir, exist_ok=True)

    print("Loading vocabulary...")
    with open(vocab_path, 'rb') as f:
        vocab = pickle.load(f)
    
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize((0.485, 0.456, 0.406),
                             (0.229, 0.224, 0.225))
    ])

    print("Loading training dataset...")
    train_dataset = FlickrDataset(
        captions_file=train_captions_file,
        root_dir=image_dir,
        vocab=vocab,
        transform=transform
    )
    
    train_loader = DataLoader(
        dataset=train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=16,
        collate_fn=collate_fn
    )

  
    print("Initializing generative models...")
    encoder = GenerativeEncoderCNN(embed_size).to(device)
    decoder = DecoderMRNN(embed_size, hidden_size, len(vocab)).to(device)
    
    for param in encoder.resnet.parameters():
        param.requires_grad = False
    
    trainable_params = list(decoder.parameters()) + \
                       list(encoder.fc.parameters()) + \
                       list(encoder.bn.parameters())
                       
    optimizer = optim.Adam(trainable_params, lr=learning_rate)
    
    # Loss function
    criterion = nn.CrossEntropyLoss()

    print("--- Starting Generative Training (Stage 2) ---")
    for epoch in range(1, num_epochs + 1):
        print(f"\nEpoch {epoch}/{num_epochs}")
        
        avg_loss = train_generative_epoch(
            encoder=encoder,
            decoder=decoder,
            data_loader=train_loader,
            optimizer=optimizer,
            criterion=criterion,
            device=device
        )
        
        print(f"Epoch {epoch} Average Loss: {avg_loss:.4f}")

        if epoch % 5 == 0:
            print(f"Saving models for epoch {epoch}...")
            torch.save(encoder.state_dict(), os.path.join(model_save_dir, f'gen_encoder_cnn-{epoch}.pth'))
            torch.save(decoder.state_dict(), os.path.join(model_save_dir, f'decoder_mrnn-{epoch}.pth'))

    print("--- Generative Training Complete ---")
    print(f"Final models saved to {model_save_dir}")

if __name__ == "__main__":
    main_generative()
