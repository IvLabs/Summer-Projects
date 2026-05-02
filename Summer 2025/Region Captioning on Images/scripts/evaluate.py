import torch
import json
import os
import pandas as pd
import pickle
from tqdm import tqdm
from pycocotools.coco import COCO
from pycocoevalcap.eval import COCOEvalCap
from torch.utils.data import DataLoader
from torchvision import transforms
from PIL import Image

from dataset import FlickrDataset, collate_fn
from vocabulary import Vocabulary
from model import GenerativeEncoderCNN, DecoderMRNN
from inference import caption_image, load_image

def format_for_coco_eval(captions_df, generated_captions):
    """
    Formats the ground truth and generated captions into the COCO JSON format.
    
    Args:
        captions_df (pd.DataFrame): DataFrame with 'image' and 'caption' columns for ground truth.
        generated_captions (list of dicts): List of {'image_id': int, 'caption': str}.
        
    Returns:
        tuple: (path_to_ground_truth_json, path_to_results_json)
    """
    annotations = []
    images_info = []
    img_id_map = {} # Maps image filename to integer ID
    img_counter = 0

    print("Formatting ground truth captions...")
    for idx, row in tqdm(captions_df.iterrows(), total=len(captions_df)):
        img_name = row['image']
        if img_name not in img_id_map:
            img_id_map[img_name] = img_counter
            images_info.append({'id': img_counter, 'file_name': img_name})
            img_counter += 1
        
        img_id = img_id_map[img_name]
        annotations.append({
            'image_id': img_id,
            'id': idx,
            'caption': row['caption']
        })

    ground_truth = {
        'info': {'description': 'Flickr Ground Truth'},
        'images': images_info,
        'annotations': annotations,
        'type': 'captions'
    }
    
    print("Formatting generated captions...")
    results = []
    for gen_cap in generated_captions:
        img_name = gen_cap['image_file']
        if img_name in img_id_map:
            results.append({
                'image_id': img_id_map[img_name],
                'caption': gen_cap['caption']
            })
        else:
            print(f"Warning: Image file {img_name} from results not found in ground truth map.")

    # Saving JSON files
    eval_dir = 'evaluation'
    os.makedirs(eval_dir, exist_ok=True)
    
    ann_file = os.path.join(eval_dir, 'ground_truth_annotations.json')
    res_file = os.path.join(eval_dir, 'generated_results.json')
    
    with open(ann_file, 'w') as f:
        json.dump(ground_truth, f)
    with open(res_file, 'w') as f:
        json.dump(results, f)
        
    return ann_file, res_file

def run_evaluation():
    """
    Main function to run evaluation.
    Generates captions for a test set and computes COCO metrics.
    """
    # Configuration
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # Paths
    data_root = 'data'
    test_captions_file = 'data/test_captions.txt'
    image_dir = os.path.join(data_root, 'Images')
    vocab_path = 'data/vocab.pkl'
    encoder_path = 'models/gen_encoder_cnn.pth'
    decoder_path = 'models/decoder_mrnn.pth'

    # Model parameters
    embed_size = 512
    hidden_size = 512

    # Load Vocabulary

    print(f"Loading vocabulary from {vocab_path}...")
    try:
        with open(vocab_path, 'rb') as f:
            vocab = pickle.load(f)
    except FileNotFoundError:
        print(f"Error: Vocabulary file not found at {vocab_path}")
        return

    # Load Generative models
 
    print("Loading generative models...")
    gen_encoder_cnn = GenerativeEncoderCNN(embed_size).to(device)
    decoder_mrnn = DecoderMRNN(embed_size, hidden_size, len(vocab)).to(device)
    
    try:
        gen_encoder_cnn.load_state_dict(torch.load(encoder_path, map_location=device))
        decoder_mrnn.load_state_dict(torch.load(decoder_path, map_location=device))
    except FileNotFoundError:
        print(f"Error: Model files not found at {encoder_path} or {decoder_path}. Aborting.")
        return
        
    gen_encoder_cnn.eval()
    decoder_mrnn.eval()

    # Load Test Data

    try:
        captions_df = pd.read_csv(test_captions_file)
        test_image_files = captions_df['image'].unique()
    except FileNotFoundError:
        print(f"Error: Test captions file not found at {test_captions_file}")
        print("This file is needed for ground truth. Please create it.")
        return
        
    print(f"Found {len(test_image_files)} unique images in test set.")

    # Generate Captions for Test Set

    generated_captions = []
    print("Generating captions for test set...")
    
    for img_file in tqdm(test_image_files):
        img_path = os.path.join(image_dir, img_file)
        try:
            image_pil = load_image(img_path)
            
            caption = caption_image(image_pil, gen_encoder_cnn, decoder_mrnn, vocab, device)
            generated_captions.append({
                'image_file': img_file,
                'caption': caption
            })
        except FileNotFoundError:
            print(f"Warning: Image file not found {img_path}")
        except Exception as e:
            print(f"Error processing {img_file}: {e}")

    # Format for COCO

    ann_file, res_file = format_for_coco_eval(captions_df, generated_captions)

    # Run COCO Evaluation

    print("Running COCO evaluation...")
    coco = COCO(ann_file)
    coco_res = coco.loadRes(res_file)
    
    coco_eval = COCOEvalCap(coco, coco_res)
    
    # Evaluate on all images in the result file
    coco_eval.params['image_id'] = coco_res.getImgIds()
    
    coco_eval.evaluate()

    print("\n--- Evaluation Metrics ---")
    for metric, score in coco_eval.eval.items():
        print(f"{metric}: {score:.4f}")
    print("--------------------------")

if __name__ == '__main__':
    run_evaluation()
