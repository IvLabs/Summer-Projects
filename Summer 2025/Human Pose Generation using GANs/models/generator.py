# models/generator.py

import torch
import torch.nn as nn
import torch.nn.functional as F
from .block import DownsampleBlock, ResidualBlock, UpsampleBlock
from .warping import MultiScaleDeformSkip

class DeformableGenerator(nn.Module):
    def _init_(self, in_ch=3, pose_ch=18, ngf=64):
        super()._init_()

        # ---------- Encoder ----------
        self.enc1 = DownsampleBlock(in_ch, ngf, norm=None)      # -> 64x64
        self.enc2 = DownsampleBlock(ngf, ngf * 2)                # -> 32x32
        self.enc3 = DownsampleBlock(ngf * 2, ngf * 4)            # -> 16x16
        self.enc4 = DownsampleBlock(ngf * 4, ngf * 8)            # -> 8x8
        self.res_blocks = nn.Sequential(
            ResidualBlock(ngf * 8),
            ResidualBlock(ngf * 8)
        )

        # ---------- Deformable skip connections ----------
        self.deform_skips = MultiScaleDeformSkip(
            feat_channels_list=[ngf, ngf * 2, ngf * 4, ngf * 8],
            pose_ch=pose_ch
        )

        # Decoder
        self.ups = nn.ModuleList([
            UpsampleBlock(512, 256),  # stage 0: input from res_blocks
            UpsampleBlock(512, 128),  # stage 1: input from merge_conv[0] output
            UpsampleBlock(256, 64),   # stage 2: input from merge_conv[1] output
            UpsampleBlock(128, 32)    # stage 3: input from merge_conv[2] output
        ])

        self.merge_convs = nn.ModuleList([
            nn.Conv2d(256 + 512, 512, kernel_size=1),  # stage 0
            nn.Conv2d(128 + 256, 256, kernel_size=1),  # stage 1
            nn.Conv2d(64 + 128, 128, kernel_size=1),   # stage 2
            nn.Conv2d(32 + 64, 64, kernel_size=1)      # stage 3
        ])

        # ---------- Final output conv ----------
        self.final_conv = nn.Sequential(
            nn.Conv2d(ngf, in_ch, kernel_size=3, stride=1, padding=1),
            nn.Tanh()
        )

    def forward(self, src_img, src_pose, tgt_pose):
        # ----- Encoder -----
        e1 = self.enc1(src_img)   # [B, 64, H/2, W/2]
        e2 = self.enc2(e1)        # [B, 128, H/4, W/4]
        e3 = self.enc3(e2)        # [B, 256, H/8, W/8]
        e4 = self.enc4(e3)        # [B, 512, H/16, W/16]
        x = self.res_blocks(e4)

        # ----- Deformable skips -----
        feats = [e1, e2, e3, e4]
        warped_feats, offsets = self.deform_skips(feats, src_pose, tgt_pose)

        # ----- Decoder -----
        for i, up in enumerate(self.ups):
            x = up(x)

            # get corresponding warped skip
            skip_feat = warped_feats[-(i + 1)]#we pair from deepest → shallowest:$$$$$$$$$

            # Resize skip to match decoder feature spatially
            if x.shape[2:] != skip_feat.shape[2:]:
                skip_feat = F.interpolate(skip_feat, size=x.shape[2:], mode='bilinear', align_corners=False)

            # Concatenate and reduce with merge conv
            x = torch.cat([x, skip_feat], dim=1)
            x = self.merge_convs[i](x)

        out = self.final_conv(x)
        return out, offsets
