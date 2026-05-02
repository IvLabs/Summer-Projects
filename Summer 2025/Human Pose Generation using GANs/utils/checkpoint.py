# utils/checkpoint.py

import os
import torch

def save_checkpoint(state: dict, checkpoint_dir: str, filename: str = "checkpoint.pth"):
    """
    Save checkpoint state dictionary to disk.
    state typically includes:
      {
        'epoch': ...,
        'netG': netG.state_dict(),
        'netD': netD.state_dict(),
        'optimG': optimG.state_dict(),
        'optimD': optimD.state_dict(),
        ...
      }
    """
    os.makedirs(checkpoint_dir, exist_ok=True)
    path = os.path.join(checkpoint_dir, filename)
    torch.save(state, path)#$$$$$$$$$$$$$$$$$$$$$$
    print(f"Saved checkpoint: {path}")

def load_checkpoint(checkpoint_path: str, device: torch.device = None):
    """
    Load checkpoint. Returns the checkpoint dict.
    If device is specified, map to that device.
    """
    if not os.path.isfile(checkpoint_path):
        raise FileNotFoundError(f"Checkpoint not found: {checkpoint_path}")
    if device is None:
        ckpt = torch.load(checkpoint_path)
    else:
        ckpt = torch.load(checkpoint_path, map_location=device)
    print(f"Loaded checkpoint: {checkpoint_path}")
    return ckpt

def load_models_from_checkpoint(ckpt: dict, netG: torch.nn.Module, netD: torch.nn.Module,
                                optimG: torch.optim.Optimizer = None, optimD: torch.optim.Optimizer = None):
    """
    Load net and optimizer states from checkpoint dict.
    """
    if 'netG' in ckpt:
        netG.load_state_dict(ckpt['netG'])
    if 'netD' in ckpt:
        netD.load_state_dict(ckpt['netD'])
    if optimG is not None and 'optimG' in ckpt:
        optimG.load_state_dict(ckpt['optimG'])
    if optimD is not None and 'optimD' in ckpt:
        optimD.load_state_dict(ckpt['optimD'])
    epoch = ckpt.get('epoch', None)
    return epoch
