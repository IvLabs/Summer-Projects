# utils/warp_utils.py

import torch
import torch.nn.functional as F

def make_base_grid(batch_size, height, width, device):
    """
    Construct base sampling grid in normalized coordinates [-1,1].
    Return grid of shape (batch_size, height, width, 2), where last dim is (x, y) coords.
    """
    # coordinates in range [-1,1]
    xs = torch.linspace(-1.0, 1.0, width, device=device)
    ys = torch.linspace(-1.0, 1.0, height, device=device)
    # create meshgrid: ys first (rows), then xs (cols)
    grid_y, grid_x = torch.meshgrid(ys, xs, indexing='ij')
    # grid_x, grid_y are (H, W)
    base = torch.stack((grid_x, grid_y), dim=2)  # (H, W, 2)
    base = base.unsqueeze(0).repeat(batch_size, 1, 1, 1)  # (B, H, W, 2)
    return base  # in normalized [-1,1] space (output???

def offsets_to_flow_grid(offsets, height, width):
    """
    Convert offsets (in absolute pixel units or normalized) to normalized grid displacement.
    Assumes offsets shape (B, 2, H, W).
    We convert to shape (B, H, W, 2) as (dx_norm, dy_norm).
    offsets are in pixel units: dx, dy relative to current pixel.
    Then normalized_offset_x = dx * 2 / (W - 1), and similarly for y.
    """
    B, _, H, W = offsets.size()# (B,C,H,W)-(0,1,2,3),,, offset aya model.py se
    # permute to (B, H, W, 2)
    offs = offsets.permute(0, 2, 3, 1).contiguous() # contiguous??
    # normalize
    # because normalized coordinate range is [-1,1] of width W → span = (W-1) in pixel
    dx = offs[..., 0] * 2.0 / float(W - 1)#[..., 0] YE HAI X ka offset of pixel
    dy = offs[..., 1] * 2.0 / float(H - 1)
    flow = torch.stack([dx, dy], dim=-1)
    return flow

def warp_feature(feat: torch.Tensor, offsets: torch.Tensor, mode: str = 'bilinear', padding_mode: str = 'border'):
    """
    Warp feature map feat using offsets (flow) from offsets.
    feat: (B, C, H, W)
    offsets: (B, 2, H, W) — dx, dy in pixel units
    Returns the warped feature map (B, C, H, W).
    """
    B, C, H, W = feat.size()
    device = feat.device

    # base grid
    base_grid = make_base_grid(B, H, W, device)  # (B, H, W, 2)
    # convert offsets into normalized displacements
    flow = offsets_to_flow_grid(offsets, H, W)   # (B, H, W, 2)

    # combine
    sampling_grid = base_grid + flow  # (B, H, W, 2)
    # grid_sample expects grid in (B, H, W, 2), with order (x, y) normalized
    warped = F.grid_sample(feat, sampling_grid, mode=mode, padding_mode=padding_mode, align_corners=True) #grid_sample = stretches the sheet along the arrows → new image.
    return warped
