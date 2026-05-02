# losses/losses.py 

import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models

class GANLoss:
    """
    Generic adversarial loss. Supports:
      - hinge loss (default)
      - LSGAN (mean-square)
    """
    def __init__(self, use_hinge=True):
        self.use_hinge = use_hinge

    def d_loss(self, real_logits, fake_logits):
        """
        Discriminator loss:
        real_logits: D(x_real) (before activation)
        fake_logits: D(G(...))
        """
        if self.use_hinge:
            # hinge loss: max(0, 1 - real) + max(0, 1 + fake)
            loss_real = torch.mean(F.relu(1.0 - real_logits))
            loss_fake = torch.mean(F.relu(1.0 + fake_logits))
            return loss_real + loss_fake
        else:
            # LSGAN: (D(real) - 1)^2 + (D(fake))^2
            loss_real = torch.mean((real_logits - 1.0) ** 2)
            loss_fake = torch.mean(fake_logits ** 2)
            return 0.5 * (loss_real + loss_fake)

    def g_loss(self, fake_logits):
        """
        Generator adversarial loss: encourages D(G) to be “real”
        """
        if self.use_hinge:
            # hinge version: -E[D(G)]
            return -torch.mean(fake_logits)
        else:
            # LSGAN: (D(fake) - 1)^2
            return 0.5 * torch.mean((fake_logits - 1.0) ** 2)


class NearestNeighborLoss(nn.Module):
    """
    Nearest-neighbor patch-based loss (feature / pixel) as in Deformable GAN paper.
    For each patch in generated image, find nearest patch in target, compute squared difference.
    Implementation is approximate via sliding-window matching.
    """

    def __init__(self, patch_size=3, stride=1):
        """
        patch_size: spatial size of patch (odd integer)
        stride: stepping between patch centers
        """
        super().__init__()
        self.ps = patch_size
        self.stride = stride

    def forward(self, fake: torch.Tensor, target: torch.Tensor):
        """
        fake, target: (B, C, H, W), assumed normalized
        Returns: scalar loss
        """
        B, C, H, W = fake.shape
        # Pad so that patches near edges are handled
        pad = self.ps // 2
        fake_padded = F.pad(fake, (pad, pad, pad, pad), mode='reflect')
        target_padded = F.pad(target, (pad, pad, pad, pad), mode='reflect')

        # Extract patches via unfold
        # For target: we want all sliding patches
        tgt_patches = target_padded.unfold(2, self.ps, 1).unfold(3, self.ps, 1)
        # shape: (B, C, H, W, ps, ps)
        # reshape to (B, H*W, C * ps * ps)
        tgt_patches = tgt_patches.contiguous().view(B, C * self.ps * self.ps, H * W).permute(0, 2, 1)
        # Similarly extract patches from fake
        fake_patches = fake_padded.unfold(2, self.ps, 1).unfold(3, self.ps, 1)
        fake_patches = fake_patches.contiguous().view(B, C * self.ps * self.ps, H * W).permute(0, 2, 1)

        # Now for each spatial location (i) in fake, we have feature vector f_i,
        # and candidate vectors in target patches (for same spatial loc). But the original paper
        # matches within a local window; here for simplicity, we match only same-spatial-position patches.

        # Compute L2 distances between fake_patches and target patches (at same positions)
        # This is just difference between fake_patches and tgt_patches
        diff = fake_patches - tgt_patches  # (B, N = H*W, D)
        # square and mean over D
        d2 = torch.mean(diff * diff, dim=2)  # (B, N)
        loss = torch.mean(d2)
        return loss


class PerceptualLoss(nn.Module):
    """
    VGG-based perceptual loss (feature reconstruction) + style loss optional.
    """
    def __init__(self, layers=('relu1_2', 'relu2_2', 'relu3_3', 'relu4_3'), weights=None, use_style=False):
        super().__init__()
        self.vgg = VGGFeatureExtractor(layers)
        self.use_style = use_style
        if weights is None:
            # equal weighting
            self.weights = {l: 1.0 for l in layers}
        else:
            self.weights = weights

    def forward(self, fake: torch.Tensor, target: torch.Tensor):
        """
        fake, target: (B, 3, H, W), in [0,1] or [-1,1]? We assume normalized to [0,1]
        """
        device = fake.device
        self.vgg = self.vgg.to(device)
        f_fake = self.vgg(fake)
        f_tgt = self.vgg(target)
        loss = 0.0
        for l in f_fake.keys():
            loss += self.weights.get(l, 1.0) * F.l1_loss(f_fake[l], f_tgt[l])
        # optional style loss: Gram matrix matching
        if self.use_style:
            for l in f_fake.keys():
                Gf = self.gram_matrix(f_fake[l])
                Gt = self.gram_matrix(f_tgt[l])
                loss += F.l1_loss(Gf, Gt)
        return loss

    @staticmethod
    def gram_matrix(feat: torch.Tensor):
        B, C, H, W = feat.size()
        feat_flat = feat.view(B, C, H * W)
        G = torch.bmm(feat_flat, feat_flat.transpose(1, 2)) / (C * H * W)
        return G


class VGGFeatureExtractor(nn.Module):
    """
    Simple wrapper around pretrained VGG-19 or VGG-16 to extract intermediate activations.
    """
    def __init__(self, target_layers):
        super().__init__()
        vgg_pretrained = models.vgg19(pretrained=True).features
        # freeze
        for p in vgg_pretrained.parameters():
            p.requires_grad = False

        self.target_layers = target_layers
        self.model = vgg_pretrained
        # mapping from layer indices to names
        self.layer_name_mapping = {
            '3': 'relu1_2',
            '8': 'relu2_2',
            '17': 'relu3_3',
            '26': 'relu4_3',
            # you can add more if needed
        }

    def forward(self, x: torch.Tensor):
        """
        Forward pass, record outputs at target layers.
        Returns dict {layer_name: activation}
        """
        out = {}
        for name, module in self.model._modules.items():
            x = module(x)
            if name in self.layer_name_mapping:
                layer = self.layer_name_mapping[name]
                if layer in self.target_layers:
                    out[layer] = x
        return out


def offset_smoothness_loss(offsets: torch.Tensor, weight: float = 1.0):
    """
    Encourage smooth offsets (flow fields), penalize large gradients.
    offsets: (B, 2, H, W)
    Returns scalar loss * weight.
    """
    dx = torch.abs(offsets[:, :, :, 1:] - offsets[:, :, :, :-1])
    dy = torch.abs(offsets[:, :, 1:, :] - offsets[:, :, :-1, :])
    return weight * (dx.mean() + dy.mean())

# Combine into a full loss manager / wrapper

class DeformGANLoss:
    def __init__(self,
                 gan_loss: GANLoss,
                 nn_loss: NearestNeighborLoss,
                 perceptual_loss: PerceptualLoss = None,
                 lambda_nn=1.0,
                 lambda_perceptual=0.1,
                 lambda_offset_smooth=0.1):
        self.gan_loss = gan_loss
        self.nn_loss = nn_loss
        self.perceptual_loss = perceptual_loss
        self.lambda_nn = lambda_nn
        self.lambda_p = lambda_perceptual
        self.lambda_off = lambda_offset_smooth

    def compute_generator_loss(self, fake_logits, fake_img, real_img, offsets=None):
        """
        fake_logits: D(fake) output
        fake_img, real_img: image tensors
        offsets: optional offset fields for smoothness regularization
        Returns: total gen loss, plus a dict of components
        """
        loss_g = self.gan_loss.g_loss(fake_logits)
        loss_nn = self.nn_loss(fake_img, real_img)
        loss = loss_g + self.lambda_nn * loss_nn

        if self.perceptual_loss is not None:
            loss_p = self.perceptual_loss(fake_img, real_img)
            loss = loss + self.lambda_p * loss_p
        else:
            loss_p = torch.tensor(0.0, device=loss.device)

        if offsets is not None:
            if isinstance(offsets, list):
                # choose last offset (or stack/mean if you prefer)
                offsets = offsets[-1]  # assuming each item is (B, 2, H, W)
            
            loss_off = offset_smoothness_loss(offsets)
            loss = loss + self.lambda_off * loss_off
        else:
            loss_off = torch.tensor(0.0, device=loss.device)

        return loss, {
            'loss_g': loss_g.item(),
            'loss_nn': loss_nn.item(),
            'loss_p': loss_p.item() if isinstance(loss_p, torch.Tensor) else 0.0,
            'loss_off': loss_off.item() if isinstance(loss_off, torch.Tensor) else 0.0
        }

    def compute_discriminator_loss(self, real_logits, fake_logits):
        """
        Returns discriminator loss (scalar) and dict
        """
        loss_d = self.gan_loss.d_loss(real_logits, fake_logits)
        return loss_d, {'loss_d': loss_d.item()}
