# evaluate.py

import torch
from utils.metrics import evaluate_batch_metrics

def evaluate_model(netG, dataloader, device):
    """
    Evaluate netG on dataloader, computing PSNR / SSIM (or other metrics).
    Returns: dict with average metrics
    """
    netG.eval()
    total_psnr = 0.0
    total_ssim = 0.0
    total_samples = 0

    with torch.no_grad():
        for batch in dataloader:
            src = batch['src_img'].to(device)
            tgt = batch['tgt_img'].to(device)
            sp = batch['src_pose'].to(device)
            tp = batch['tgt_pose'].to(device)

            fake, _ = netG(src, sp, tp)
            metrics = evaluate_batch_metrics(fake, tgt)
            batch_size = src.size(0)
            total_psnr += metrics['psnr'] * batch_size
            total_ssim += metrics['ssim'] * batch_size
            total_samples += batch_size

    avg = {
        'psnr': total_psnr / total_samples,
        'ssim': total_ssim / total_samples
    }
    print(f"Eval: PSNR = {avg['psnr']:.4f}, SSIM = {avg['ssim']:.4f}")
    return avg
