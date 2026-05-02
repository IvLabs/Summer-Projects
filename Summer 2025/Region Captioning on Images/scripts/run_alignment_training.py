import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import transforms
import pickle
import os

from vocabulary import Vocabulary
from dataset import FlickrDataset, collate_fn
from model import AlignmentEncoderCNN, AlignmentDecoderRNN
from train import train_alignment_epoch

def main_alignment():

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    image_dir = 'Project/data'
    train_captions_file = 'Project/data/captions.txt'
    vocab_path = 'Project/data/vocab.pkl'
    model_save_dir = 'Project/models'
    
    embed_size = 512
    hidden_size = 512
    num_epochs = 45
    batch_size = 128
    learning_rate = 0.001

    os.makedirs(model_save_dir, exist_ok=True)
    
    # Load Vocab
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
        root_dir = image_dir,
        captions_file=train_captions_file,
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

    print("Initializing alignment models...")
    image_encoder = AlignmentEncoderCNN(embed_size).to(device)
    text_encoder = AlignmentDecoderRNN(embed_size, hidden_size, len(vocab)).to(device)
   
    # Combine parameters from both encoders
    params = list(image_encoder.parameters()) + list(text_encoder.parameters())
    optimizer = optim.Adam(params, lr=learning_rate)

    print("--- Starting Alignment Training (Stage 1) ---")
    for epoch in range(1, num_epochs + 1):
        print(f"\nEpoch {epoch}/{num_epochs}")
        
        avg_loss = train_alignment_epoch(
            image_encoder=image_encoder,
            text_encoder=text_encoder,
            data_loader=train_loader,
            optimizer=optimizer,
            device=device
        )
        
        print(f"Epoch {epoch} Average Loss: {avg_loss:.4f}")
        
        if epoch % 5 == 0:
            print(f"Saving models for epoch {epoch}...")
            torch.save(image_encoder.state_dict(), os.path.join(model_save_dir, f'align_encoder_cnn-{epoch}.pth'))
            torch.save(text_encoder.state_dict(), os.path.join(model_save_dir, f'align_decoder_rnn-{epoch}.pth'))

    print("--- Alignment Training Complete ---")
    print(f"Final models saved to {model_save_dir}")

if __name__ == "__main__":
    main_alignment()
    