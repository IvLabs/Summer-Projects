# utils/metrics.py

import torch
import numpy as np
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import peak_signal_noise_ratio as psnr
from torchvision.transforms import functional as TF
from PIL import Image

def compute_psnr(img1: np.ndarray, img2: np.ndarray, data_range=255.0):
    """
    img1, img2: uint8 arrays, shape (H, W, C) or (C, H, W)
    Returns PSNR value
    """
    return psnr(img1, img2, data_range=data_range)

def compute_ssim(img1: np.ndarray, img2: np.ndarray, multichannel=True, data_range=255.0):
    """
    Returns SSIM between two images
    """
    return ssim(img1, img2, multichannel=multichannel, data_range=data_range)

def tensor_to_numpy_img(tensor: torch.Tensor):
    """
    Convert a tensor in [-1,1] to uint8 numpy (H, W, C)
    """
    arr = tensor.detach().cpu().clamp(-1, 1).numpy()
    # (C, H, W) → (H, W, C)
    arr = np.transpose(arr, (1, 2, 0))
    arr = ((arr + 1.0) / 2.0) * 255.0
    return arr.astype(np.uint8)

def evaluate_batch_metrics(preds: torch.Tensor, targets: torch.Tensor):
    """
    Compute average PSNR / SSIM over a batch.
    preds, targets: (B, 3, H, W) in [-1,1]
    Returns dict {'psnr': avg_psnr, 'ssim': avg_ssim}
    """
    batch_size = preds.size(0)
    psnr_vals = []
    ssim_vals = []
    for i in range(batch_size):
        p = tensor_to_numpy_img(preds[i])
        t = tensor_to_numpy_img(targets[i])
        psnr_vals.append(compute_psnr(p, t))
        ssim_vals.append(compute_ssim(p, t))
    return {
        'psnr': float(np.mean(psnr_vals)),
        'ssim': float(np.mean(ssim_vals))
    }
