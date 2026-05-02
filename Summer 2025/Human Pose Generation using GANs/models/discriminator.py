# models/discriminator.py

import torch
import torch.nn as nn
import torch.nn.functional as F

class PatchDiscriminator(nn.Module):   #Instead of classifying the whole image as real/fake,  this model classifies small patches of the image.
                                       #It focuses on local realism — texture, skin, lighting, fabric, etc.
    """
    PatchGAN discriminator that inputs image + pose, and outputs patch realism map.((it slides a small window (patch) across the image)).
    """ 
    def _init_(self, in_ch_img=3, pose_ch=18, base_channel=64, n_layers=4):
        super()._init_()
        # input channels = img + pose
        ch = base_channel
        layers = []
        layers.append(nn.Conv2d(in_ch_img + pose_ch, ch, kernel_size=4, stride=2, padding=1))
        layers.append(nn.LeakyReLU(0.2, inplace=True))

        curr_ch = ch
        for n in range(1, n_layers):
            next_ch = min(curr_ch * 2, base_channel * 8)
            layers.append(nn.Conv2d(curr_ch, next_ch, kernel_size=4, stride=2, padding=1, bias=False))
            layers.append(nn.InstanceNorm2d(next_ch))
            layers.append(nn.LeakyReLU(0.2, inplace=True))
            curr_ch = next_ch

        # After downsampling, one more conv with stride=1
        layers.append(nn.Conv2d(curr_ch, curr_ch * 2, kernel_size=4, stride=1, padding=1, bias=False))
        layers.append(nn.InstanceNorm2d(curr_ch * 2))
        layers.append(nn.LeakyReLU(0.2, inplace=True))

        # final output layer
        layers.append(nn.Conv2d(curr_ch * 2, 1, kernel_size=4, stride=1, padding=1))
        # No sigmoid — we'll use LSGAN or hinge loss directly on output

        self.main = nn.Sequential(*layers)

    def forward(self, img, pose):
        """
        img: (B, 3, H, W)
        pose: (B, P, H, W)
        returns: patch score map (B, 1, H', W')
        """
        x = torch.cat([img, pose], dim=1)
        return self.main(x)
