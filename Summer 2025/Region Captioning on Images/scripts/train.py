import torch
import torch.nn as nn
from tqdm import tqdm
import numpy as np
from torch.nn.utils.rnn import pack_padded_sequence

def cosine_similarity(v1, v2):
    # Compute cosine similarity between two tensors
    return torch.dot(v1, v2) / (torch.norm(v1) * torch.norm(v2))

def contrastive_loss(image_features, text_features, margin=0.2):
    """
    Compute contrastive loss (max-margin loss).
    image_features: [batch_size, embed_size]
    text_features: [batch_size, embed_size]
    """
    scores = torch.mm(image_features, text_features.t())

    diagonal = scores.diag().view(-1, 1)
    
    # Compare matching pairs to all other pairs
    # Image-to-Text: Compare image_i to text_j
    cost_s = (margin - diagonal + scores).clamp(min=0)
    # Text-to-Image: Compare text_i to image_j
    cost_im = (margin - diagonal.t() + scores).clamp(min=0)
    
    # Clear diagonals
    cost_s = cost_s - torch.diag(cost_s.diag())
    cost_im = cost_im - torch.diag(cost_im.diag())
    
    # Sum of max-margin violations
    loss = cost_s.sum() + cost_im.sum()
    
    loss = loss / image_features.size(0)
    
    return loss

def train_alignment_epoch(image_encoder, text_encoder, data_loader, optimizer, device):
    """Train the alignment model for one epoch."""
    image_encoder.train()
    text_encoder.train()
    
    total_loss = 0.0
    
    for images, captions, lengths in tqdm(data_loader, desc="Training Alignment"):
        if images is None: continue # Skip batch for bad data
        
        images = images.to(device)
        captions = captions.to(device)
        
        optimizer.zero_grad()
        
        img_embeds = image_encoder(images)
        cap_embeds = text_encoder(captions, lengths)
 
        loss = contrastive_loss(img_embeds, cap_embeds)
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item()

    return total_loss / len(data_loader)

def train_generative_epoch(encoder, decoder, data_loader, optimizer, criterion, device):
    # Train the generative model for one epoch
    encoder.train()
    decoder.train()
    
    total_loss = 0.0

    for images, captions, lengths in tqdm(data_loader, desc="Training Generative"):
        if images is None: continue # Skip batch for bad data
        
        images = images.to(device)
        captions = captions.to(device)
        
        optimizer.zero_grad()
        
        features = encoder(images)
        # We predict all words except <start>
        # Input to decoder: captions[:, :-1] (all but <end>)
        # Lengths: [l - 1]
        outputs = decoder(features, captions[:, :-1], [l - 1 for l in lengths])
        
        # Target for criterion: captions[:, 1:] (all but not <start>)
        targets = pack_padded_sequence(captions[:, 1:], [l - 1 for l in lengths],
                                       batch_first=True, enforce_sorted=False).data
        
        loss = criterion(outputs, targets)
        
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item()

    return total_loss / len(data_loader)

