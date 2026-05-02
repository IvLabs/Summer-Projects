import torch
from torchvision import transforms
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import numpy as np

def load_image(image_path):
    """Loads and returns a PIL image in RGB format."""
    return Image.open(image_path).convert("RGB")

def preprocess_for_detector(image_pil):
    """Prepares a PIL image for the Faster R-CNN detector."""
    transform = transforms.Compose([
        transforms.ToTensor()
    ])
    return transform(image_pil)

def preprocess_for_generative_encoder(region_pil):
    """Prepares a cropped PIL image region for the GenerativeEncoderCNN."""
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize((0.485, 0.456, 0.406),
                             (0.229, 0.224, 0.225))
    ])
    return transform(region_pil).unsqueeze(0)

def tokens_to_sentence(tokens, vocab):
    """Converts a list of token IDs back into a string."""
    caption_words = []
    for word_id in tokens:
        word = vocab.idx2word[word_id.item()]
        if word == "<end>":
            break
        if word != "<start>":
            caption_words.append(word)
    return " ".join(caption_words)


def caption_image(image_pil, encoder, decoder, vocab, device):
    # Used for COCO evaluation.
        
    image_tensor = preprocess_for_generative_encoder(image_pil).to(device)
    
    with torch.no_grad():
        features = encoder(image_tensor)
        sampled_ids = decoder.sample(features, vocab)
        
    return tokens_to_sentence(sampled_ids[0], vocab)


def caption_region(region_pil, encoder, decoder, vocab, device):
    
    # Generates a caption for a cropped region of an image.

    region_tensor = preprocess_for_generative_encoder(region_pil).to(device)
    
    with torch.no_grad():
        features = encoder(region_tensor)
        sampled_ids = decoder.sample(features, vocab) # [1, seq_len]

    return tokens_to_sentence(sampled_ids[0], vocab)


def generate_region_captions(image_path, faster_rcnn_model, encoder, decoder, vocab, device, conf_thresh=0.5):
    """
    Detect regions with Faster R-CNN, then generate captions for each region.
    Returns image with drawn boxes + captions and list of region captions.
    """
    image = load_image(image_path)
    
    image_tensor = preprocess_for_detector(image).to(device)
    faster_rcnn_model.confidence_threshold = conf_thresh 
    
    with torch.no_grad():
        boxes = faster_rcnn_model(image_tensor) # [N, 4]

    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype("arial.ttf", 15)
    except IOError:
        font = ImageFont.load_default()
        
    region_captions = []

    for box in boxes:
        x1, y1, x2, y2 = box.tolist()

        region_pil = image.crop((x1, y1, x2, y2))

        caption = caption_region(region_pil, encoder, decoder, vocab, device)
        region_captions.append(((x1, y1, x2, y2), caption))

        draw.rectangle([x1, y1, x2, y2], outline="red", width=2)

        text_bbox = draw.textbbox((x1, y1), caption, font=font)
        draw.rectangle(text_bbox, fill="red")
        draw.text((x1, y1), caption, fill="white", font=font)

    return image, region_captions