import os
import json
from PIL import Image
import numpy as np
from ultralytics import YOLO  # (assuming this is a custom class)

 # Import the YOLO class for inference


image_dir = "data/market-1501/bounding_box_train"
out_dir = "data/keypoints/keypoints.json"  # Output JSON file path
yolo_path = "HPE/yolo11n-pose.pt"         # Use forward slashes for cross-platform compatibility


def main():
    os.makedirs(os.path.dirname(out_dir), exist_ok = True)
    pose_estimator = YOLO("HPE/yolo11n-pose.pt")
    KP_dict = {}# store keypoints for all images
    img_names = sorted(os.listdir(image_dir))
    for img_name in img_names: #Loop through all images
        if not img_name.lower().endswith((".jpg",".png",".jpeg")):  #Skip non-image files
            continue
        img_path = os.path.join(image_dir, img_name)# construct the full image (just complete the path,"bounding_box_train/0002_c1s1_000451_03.jpg")
        try:
            img = Image.open(img_path).convert("RGB")
        except Exception as e:
            print(f"could not open {img_path}: {e}")
            continue   
        results = pose_estimator(img_path)#infer- cv2.imread
        if(len(results) > 0):
            keypoints = results[0].keypoints.data.cpu().numpy().tolist() #first image (.data.cpu().numpy().tolist() → converts the PyTorch tensor into a Python list.)
        if len(keypoints) > 0:
            KP_dict[img_name] = keypoints # store keypoints

    with open(out_dir,"w") as f:
        json.dump(KP_dict,f)    
    print(f"Saved keypoints for {len(KP_dict)} images to {out_dir}")
if __name__ == "__main__":
    main()
