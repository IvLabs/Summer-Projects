import os
import random
import csv
from collections import defaultdict

# --- Configuration ---
# Path to your folder containing heatmap images
source_image_dir = "C:/Users/hp/OneDrive/Pictures/Documents/TEST/data/market-1501/bounding_box_train"
out_train_pairs = "C:/Users/hp/OneDrive/Desktop/test/data/splits/train_pairs.csv"
out_val_pairs = "C:/Users/hp/OneDrive/Desktop/test/data/splits/val_pairs.csv"
val_split_ratio = 0.1  # fraction of identities for validation
# --------------------

def read_identities_from_filenames(source_image_dir):
    """
    Reads image files from the specified path and groups them by an 'identity_id'
    extracted from the filename (the part before the first underscore).
    Returns dict: identity_id -> list of image_names
    """
    pid2imgs = defaultdict(list)
    if not os.path.exists(source_image_dir):
        print(f"Error: Directory not found at {source_image_dir}")
        return pid2imgs

    files = sorted(os.listdir(source_image_dir))
    for file in files:
        if not (file.lower().endswith(".png") or file.lower().endswith(".jpg") or file.lower().endswith(".jpeg")):
           continue

        
        # Extract ID part — first part before underscore
        # Example: "MEN-Denim-id_00000080-01_7_additional.png" -> "MEN-Denim-id"
        parts = file.split("_", 1) # Split only on the first underscore
        if len(parts) > 0:
            pid = parts[0]
            pid2imgs[pid].append(file)
    return pid2imgs

def make_pairs_for_id(img_list):
    """
    Given a list of images of one identity, return a list of (src, tgt) pairs.
    Generates all ordered pairs where src != tgt.
    """
    pairs = []
    n = len(img_list)
    if n < 2: # Need at least two images to form a pair
        return pairs
    
    for i in range(n):
        for j in range(n):
            if i == j: # Don't pair an image with itself
                continue
            pairs.append((img_list[i], img_list[j]))
    return pairs

def split_identities(pid2imgs, val_ratio=0.1, seed=42):
    """
    Splits identity IDs into training and validation sets.
    """
    pids = list(pid2imgs.keys())
    random.seed(seed)
    random.shuffle(pids)
    
    n_val = int(len(pids) * val_ratio)
    val_pids = set(pids[:n_val])
    train_pids = set(pids[n_val:])
    
    return train_pids, val_pids

def write_pairs(pairs, out_csv):
    """
    Writes a list of image pairs to a CSV file.
    """
    os.makedirs(os.path.dirname(out_csv), exist_ok=True)
    with open(out_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        for (a, b) in pairs:
            writer.writerow([a, b])
    print(f"Wrote {len(pairs)} pairs to {out_csv}")

def main():
    pid2imgs = read_identities_from_filenames(source_image_dir)
    
    if not pid2imgs:
        print("No identities found or directory is empty. Exiting.")
        return

    train_pids, val_pids = split_identities(pid2imgs, val_ratio=val_split_ratio)

    train_pairs = []
    val_pairs = []

    for pid, imgs in pid2imgs.items():
        pairs = make_pairs_for_id(imgs)
        if pid in train_pids:
            train_pairs.extend(pairs)
        else:
            val_pairs.extend(pairs)
    
    # Optionally: shuffle the generated pairs
    random.shuffle(train_pairs)
    random.shuffle(val_pairs)

    write_pairs(train_pairs, out_train_pairs)
    write_pairs(val_pairs, out_val_pairs)

    print(f"✅ Training and validation pair CSVs generated successfully!")

if __name__ == "__main__":
    main()
