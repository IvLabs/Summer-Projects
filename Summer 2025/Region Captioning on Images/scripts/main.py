import torch
import pickle
import os
import matplotlib.pyplot as plt

from vocabulary import Vocabulary
from model import GenerativeEncoderCNN, DecoderMRNN, FasterRCNNRegionDetector
from inference import generate_region_captions

def main():

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    encoder_path = 'Project/models/gen_encoder_cnn-30.pth'
    decoder_path = 'Project/models/decoder_mrnn-30.pth'
    
    test_image = "Project/data/test_img/Screenshot 2025-10-29 140418.png" 
 
    vocab_path = 'Project/data/vocab.pkl'
    
    embed_size = 512
    hidden_size = 512

    print(f"Loading vocabulary from {vocab_path}...")
    with open(vocab_path, 'rb') as f:
        vocab = pickle.load(f)
    
    print("Loading models...")

    encoder = GenerativeEncoderCNN(embed_size).to(device)
    decoder = DecoderMRNN(embed_size, hidden_size, len(vocab)).to(device)
    
    encoder.load_state_dict(torch.load(encoder_path, map_location=device))
    decoder.load_state_dict(torch.load(decoder_path, map_location=device))
    
    encoder.eval()
    decoder.eval() 

    faster_rcnn_model = FasterRCNNRegionDetector().to(device)
    faster_rcnn_model.eval()

    print(f"Running inference on image: {test_image}")
    
    # Returns the final PIL image with boxes/text drawn on it
    # and a list of (box, caption) tuples
    final_image_with_boxes, region_caps = generate_region_captions(
        image_path=test_image,
        faster_rcnn_model=faster_rcnn_model,
        encoder=encoder,
        decoder=decoder,
        vocab=vocab,
        device=device,
    )
    
    print("\n--- Generated Captions ---")
    if not region_caps:
        print("No regions were detected or captioned.")
    for box, cap in region_caps:
        # Box coordinates are (x1, y1, x2, y2)
        print(f"Region at [{int(box[0])}, {int(box[1])}, {int(box[2])}, {int(box[3])}]: {cap}")
    print("------------------------")
    
    save_path = "result_image.jpg"
    try:
        final_image_with_boxes.save(save_path)
        print(f"\nSuccessfully saved annotated image to: {save_path}")
        print("Please open this file in your file explorer to see the result.")
    except Exception as e:
        print(f"\nError saving image: {e}")
        print("Could not save the final image.")


if __name__ == "__main__":
    main()

