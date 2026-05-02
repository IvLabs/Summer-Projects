# models/warping.py

import torch
import torch.nn as nn
import torch.nn.functional as F

# Import helpers (to be implemented in warp_utils)
from utils.warp_utils import warp_feature # pyright: ignore[reportMissingImports]

class DeformableSkipConnection(nn.Module):
    """
    A skip connection that warps the encoder feature map to align with target pose, then merges into decoder.
    """
    def _init_(self, feat_ch, pose_ch, offset_hidden=64):
        """
        feat_ch: number of feature map channels from encoder
        pose_ch: number of pose map channels (input pose representation)
        offset_hidden: hidden channels for offset prediction
        """
        super()._init_()
        # A small network to predict offsets given encoder features + pose maps
        # You may choose more layers / vary architecture
        self.offset_net = nn.Sequential(
            nn.Conv2d(feat_ch + pose_ch * 2, offset_hidden, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(offset_hidden, 2, kernel_size=3, padding =1)#horizontal, vertical displacement
            # output: (batch, 2, H, W) — flow offsets in x,y directions
        )

    def forward(self, feat_src, src_pose, tgt_pose):
        B, C, Hf, Wf = feat_src.size()
        # resize pose maps
        src_pose_resized = F.interpolate(src_pose, size=(Hf, Wf), mode='bilinear', align_corners=False)
        tgt_pose_resized = F.interpolate(tgt_pose, size=(Hf, Wf), mode='bilinear', align_corners=False)
        x = torch.cat([feat_src, src_pose_resized, tgt_pose_resized], dim=1)
        offsets = self.offset_net(x)
        warped = warp_feature(feat_src, offsets)
        return warped, offsets


class MultiScaleDeformSkip(nn.Module):
    """
    If you want to predict offsets at multiple scales / pyramid levels,
    you may stack several DeformableSkipConnection modules.
    """
    def _init_(self, feat_channels_list, pose_ch, offset_hidden=64):
        """
        feat_channels_list: list of feat channels at different scales (from coarse to fine)
        e.g. [512, 256, 128, 64]
        """
        super()._init_()
        self.deform_skips = nn.ModuleList([
            DeformableSkipConnection(c, pose_ch, offset_hidden=offset_hidden)
            for c in feat_channels_list  #example#e4: 512 channels (lowest resolution)
                                        #e3: 256 channels
                                        #e2: 128 channels
                                        #e1: 64  channels (highest resolution)
        ])

    def forward(self, feat_list, src_pose, tgt_pose):
        """
        feat_list: list of encoder features from multiple levels (coarse->fine)
        Returns: list of warped features aligned with target pose
        """
        warped_feats = []
        offsets_all = []
        for feat, ds in zip(feat_list, self.deform_skips):
            w, off = ds(feat, src_pose, tgt_pose)
            warped_feats.append(w)
            offsets_all.append(off)
        return warped_feats, offsets_all
