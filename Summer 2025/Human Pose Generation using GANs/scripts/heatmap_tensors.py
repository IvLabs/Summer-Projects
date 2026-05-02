import os
import json
import numpy as np
import torch
from scipy.ndimage import gaussian_filter

# === PATHS ===
keypoints_json = "data/keypoints/keypoints.json"   # Input keypoints JSON
out_heatmap_dir = "data/keypoints/heatmaps"        # Output directory for tensor files

# === SETTINGS ===
img_size = (256, 128)  # (height, width)
sigma = 5              # Gaussian blur strength

# === MAIN FUNCTION ===
def generate_heatmaps_and_save_as_tensors():
    # --- Load keypoints ---
    with open(keypoints_json, "r") as f:
        kp_data = json.load(f)
    print(f"📥 Loaded keypoints for {len(kp_data)} images")

    # Create output directory if it doesn't exist
    os.makedirs(out_heatmap_dir, exist_ok=True)

    # --- Process each image's keypoints ---
    for img_name, keypoints_list in kp_data.items():
        heatmap_np = np.zeros(img_size, dtype=np.float32)

        # Loop through all detected persons in the image
        for person_keypoints in keypoints_list:
            keypoints = np.array(person_keypoints)
            if keypoints.ndim == 3:  # [N, num_kpts, 3]
                keypoints = keypoints[0]
            for (x, y, conf) in keypoints:
                if conf > 0.3:  # confidence threshold
                    x, y = int(x), int(y)
                    if 0 <= x < img_size[1] and 0 <= y < img_size[0]:
                        heatmap_np[y, x] += 1.0

        # Apply Gaussian blur
        heatmap_np = gaussian_filter(heatmap_np, sigma=sigma)

        # Convert to tensor
        heatmap_tensor = torch.from_numpy(heatmap_np).unsqueeze(0)  # Shape: (1, H, W)

        # Generate output path
        base_name = os.path.splitext(os.path.basename(img_name))[0]
        out_path = os.path.join(out_heatmap_dir, f"{base_name}_heatmap.pt")

        # Save tensor
        torch.save(heatmap_tensor, out_path)
        print(f"✅ Saved tensor: {out_path}")

# === RUN ===
if __name__ == "__main__":
    generate_heatmaps_and_save_as_tensors()
