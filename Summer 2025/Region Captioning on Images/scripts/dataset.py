import os
import torch
import pandas as pd
import nltk
from torch.utils.data import Dataset
from PIL import Image

class FlickrDataset(Dataset):
    """
    Reads data based on the specified file structure:
    - root_dir/
      - Images/ (all.jpg images)
      - captions.txt (CSV with 'image' and 'caption' headers)
    """
    def __init__(self, root_dir, captions_file, vocab, transform=None, stage='alignment'):
        self.root_dir = root_dir
        self.df = pd.read_csv(captions_file)
        self.vocab = vocab
        self.transform = transform
        self.stage = stage # 'alignment' or 'generative'

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        img_name = os.path.join(self.root_dir, 'Images', row['image'])
        caption = str(row['caption']) # Ensure caption is a string

        # Load image
        try:
            image = Image.open(img_name).convert('RGB')
        except FileNotFoundError:
            print(f"Warning: Image not found at {img_name}. Returning None.")
            # Handle this in collate_fn
            return None 

        if self.transform:
            image = self.transform(image)
        
        # Tokenize caption
        try:
            tokens = nltk.tokenize.word_tokenize(caption.lower())
        except Exception as e:
            print(f"Error tokenizing caption: {caption} | Error: {e}")
            tokens = [] # Return empty tokens

        # Convert caption to tensor
        caption_vec = []
        caption_vec.append(self.vocab('<start>'))
        caption_vec.extend([self.vocab(token) for token in tokens])
        caption_vec.append(self.vocab('<end>'))
        target = torch.Tensor(caption_vec)
                
        return image, target

def collate_fn(data):
    """Creates mini-batch tensors from the list of tuples (image/regions, caption)."""
    # Filter out None entries (from missing images)
    data = [d for d in data if d is not None]
    if not data:
        return None, None, None

    data.sort(key=lambda x: len(x[1]), reverse=True)
    images, captions = zip(*data)

    # Merge images (from tuple of tensors to a single tensor).
    images = torch.stack(images, 0)

    # Merge captions (from tuple of 1D tensor to 2D tensor).
    lengths = [len(cap) for cap in captions]
    targets = torch.zeros(len(captions), max(lengths)).long()
    for i, cap in enumerate(captions):
        end = lengths[i]
        targets[i, :end] = cap[:end]
        
    return images, targets, lengths
