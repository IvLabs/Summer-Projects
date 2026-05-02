# utils/visualization.py

import os
from PIL import Image
import numpy as np
import torch
import torchvision.utils as vutils

def tensor_to_image(tensor: torch.Tensor):
    """
    Convert a torch.Tensor in [-1,1] to a uint8 numpy image in [0,255].
    Input: tensor shape (3, H, W) or (B, 3, H, W)
    Returns: numpy array
    """
    if tensor.dim() == 4:
        # batch of images
        imgs = []
        for i in range(tensor.size(0)):
            imgs.append(tensor_to_image(tensor[i]))
        return np.stack(imgs, axis=0)
    # single image
    img = tensor.detach().cpu().clamp(-1, 1).numpy()
    # from (C, H, W) to (H, W, C)
    img = (img + 1.0) / 2.0  # [0,1]
    img = (img * 255.0).astype(np.uint8)
    img = np.transpose(img, (1, 2, 0))
    return img

def save_tensor_images(grid_tensor: torch.Tensor, fname: str, nrow: int = 4):#fname = file path (e.g., "output/grid.png")
    """
    Save a grid of images stored in a Batch tensor to disk.
    grid_tensor: shape (B, C, H, W) with values in [-1,1]
    fname: output filepath (.png etc.)
    """
    os.makedirs(os.path.dirname(fname), exist_ok=True)
    # transform from [-1,1] to [0,1]
    normed = (grid_tensor + 1.0) / 2.0
    vutils.save_image(normed, fname, nrow=nrow)

def make_comparison_grid(src_imgs: torch.Tensor,
                         tgt_imgs: torch.Tensor,
                         pose_maps: torch.Tensor,
                         generated: torch.Tensor,
                         nrow: int = 4):
    """
    Make a combined grid: [src | pose | generated | tgt] per example horizontally.
    Inputs: each is (B, C, H, W) or pose_maps is (B, P, H, W)
    Return: a grid tensor (B, C_total, H, W)
    """
    B = src_imgs.size(0)
    # we want to stack along width dimension
    # Convert pose maps to 3-channel RGB (for visualization) by e.g. taking first 3 channels, or summing/joint overlay.
    # For simplicity, we repeat or reduce to 3 channels:
    # If pose_maps has P channels, we can sum or pick first 3:
    P = pose_maps.size(1)
    if P >= 3:
        pose_vis = pose_maps[:, :3, :, :]
    else:
        # pad zeros
        pad = torch.zeros(B, 3 - P, pose_maps.size(2), pose_maps.size(3), device=pose_maps.device)
        pose_vis = torch.cat([pose_maps, pad], dim=1)

    # Now each of src_imgs, pose_vis, generated, tgt_imgs have 3 channels
    # Concatenate along width (dim=3)
    concat = torch.cat([src_imgs, pose_vis, generated, tgt_imgs], dim=3)
    return concat  # shape (B, 3, H, 4W)

def save_comparison_grid(src, tgt, pose, generated, fname, nrow=4):
    """
    Combines and saves comparison grid to file.
    """
    grid = make_comparison_grid(src, tgt, pose, generated, nrow=nrow)
    save_tensor_images(grid, fname, nrow=1)  # since we already concatenated horizontally
