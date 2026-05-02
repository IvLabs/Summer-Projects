import os
import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

# === PATHS ===
keypoints_json = "data/keypoints/keypoints.json"       # Input keypoints JSON
out_heatmap_dir = "data/keypoints/heatmaps"             # Folder for individual heatmaps
merged_heatmap_path = "data/keypoints/body_heatmap.png" # One combined average heatmap

# === SETTINGS ===
img_size = (256, 128)  # (height, width)
sigma = 5              # Gaussian blur strength

# === MAIN FUNCTION ===
def generate_heatmaps():
    # --- Load keypoints ---
    with open(keypoints_json, "r") as f:
        kp_data = json.load(f)
    print(f"Loaded keypoints for {len(kp_data)} images")

    os.makedirs(out_heatmap_dir, exist_ok=True)

    # Initialize for combined average heatmap
    combined_heatmap = np.zeros(img_size, dtype=np.float32)
    count = 0

    # --- Process each image's keypoints ---
    for img_name, keypoints_list in kp_data.items():
        heatmap = np.zeros(img_size, dtype=np.float32)

        # Loop through all detected persons in the image
        for person_keypoints in keypoints_list:
            keypoints = np.array(person_keypoints)
            if keypoints.ndim == 3:  # [N, num_kpts, 3]
                keypoints = keypoints[0]
            for (x, y, conf) in keypoints:
                if conf > 0.3:  # confidence threshold
                    x, y = int(x), int(y)
                    if 0 <= x < img_size[1] and 0 <= y < img_size[0]:
                        heatmap[y, x] += 1.0

        # Smooth the heatmap
        heatmap = gaussian_filter(heatmap, sigma=sigma)

        # --- Save individual heatmap with image name ---
        base_name = os.path.splitext(os.path.basename(img_name))[0]
        out_path = os.path.join(out_heatmap_dir, f"{base_name}_heatmap.png")
        plt.imsave(out_path, heatmap, cmap='hot')
        print(f"✅ Saved: {out_path}")

        # Add to combined average
        combined_heatmap += heatmap
        count += 1

    # --- Save combined average heatmap ---
    if count > 0:
        combined_heatmap /= count
        plt.imsave(merged_heatmap_path, combined_heatmap, cmap='hot')
        print(f"\n🔥 Saved combined body heatmap to: {merged_heatmap_path}")
    else:
        print("⚠ No keypoints processed!")

# === RUN ===
if __name__ == "__main__":
    generate_heatmaps()
