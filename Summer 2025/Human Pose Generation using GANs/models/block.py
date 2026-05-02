import os
from PIL import Image
import numpy as np
import torch
from torch.utils.data import Dataset
import torchvision.transforms as T

class MarketPoseDataset(Dataset):
    """
    Dataset for Market-1501 pose transfer. Each example is a pair:
    (src_image, src_pose_map, tgt_pose_map, tgt_image)
    """
    def _init_(self,
                 images_dir: str,
                 pose_maps_dir: str,
                 pairs_csv: str,
                 img_size=(256,256),
                 transform=None):
        self.images_dir = images_dir
        self.pose_maps_dir = pose_maps_dir
        self.pairs = []

        # Read CSV and filter pairs with missing files
        with open(pairs_csv, 'r') as f:
            for line in f:
                src_name, tgt_name = line.strip().split(',')

                src_path = os.path.join(self.images_dir, src_name)
                tgt_path = os.path.join(self.images_dir, tgt_name)
                src_pose_path = os.path.join(self.pose_maps_dir, os.path.splitext(src_name)[0] + ".npy")
                tgt_pose_path = os.path.join(self.pose_maps_dir, os.path.splitext(tgt_name)[0] + ".npy")

                if os.path.exists(src_path) and os.path.exists(tgt_path) \
                   and os.path.exists(src_pose_path) and os.path.exists(tgt_pose_path):
                    self.pairs.append((src_name, tgt_name))
                else:
                    print(f"Skipping missing pair: {src_name}, {tgt_name}")

        self.img_size = img_size

        # Define default transforms if not provided
        if transform is None:
            self.transform = T.Compose([
                T.Resize(self.img_size),
                T.ToTensor(),
                T.Normalize(mean=[0.5,0.5,0.5], std=[0.5,0.5,0.5])
            ])
        else:
            self.transform = transform

    def _len_(self):
        return len(self.pairs)

    def _getitem_(self, idx):
        src_name, tgt_name = self.pairs[idx]
        src_path = os.path.join(self.images_dir, src_name)
        tgt_path = os.path.join(self.images_dir, tgt_name)

        src_pose_path = os.path.join(self.pose_maps_dir, os.path.splitext(src_name)[0] + ".npy")
        tgt_pose_path = os.path.join(self.pose_maps_dir, os.path.splitext(tgt_name)[0] + ".npy")

        # Load images
        src_img = Image.open(src_path).convert("RGB")
        tgt_img = Image.open(tgt_path).convert("RGB")
        src_img = self.transform(src_img)
        tgt_img = self.transform(tgt_img)

        # Load pose maps
        src_pose = torch.from_numpy(np.load(src_pose_path)).float()
        tgt_pose = torch.from_numpy(np.load(tgt_pose_path)).float()

        return {
            "src_img": src_img,
            "tgt_img": tgt_img,
            "src_pose": src_pose,
            "tgt_pose": tgt_pose
        }
