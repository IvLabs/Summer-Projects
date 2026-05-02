# train.py

import os
import time
import torch
from losses.losses import DeformGANLoss, GANLoss, NearestNeighborLoss, PerceptualLoss
from utils.checkpoints import save_checkpoint
from utils.visualization import save_comparison_grid

def train_model(netG, netD, train_loader, val_loader,
                device,
                num_epochs=100,
                lr=2e-4,
                betas=(0.5, 0.999),
                lambda_nn=1.0,
                lambda_p=0.1,
                lambda_off=0.1,
                use_perceptual=True,
                checkpoint_dir="outputs/ckpts",
                sample_dir="outputs/samples",
                num_gen_updates = 1):
    """
    Train the generative model.
    Args:
        netG, netD: models already moved to device
        train_loader, val_loader: PyTorch DataLoader objects
        device: torch.device
        num_epochs, lr, etc: hyperparameters
        lambda_nn, lambda_p, lambda_off: loss weights
        use_perceptual: whether to include perceptual loss
        checkpoint_dir, sample_dir: output dirs
    """
    os.makedirs(sample_dir, exist_ok=True)
    os.makedirs(checkpoint_dir, exist_ok=True)

    # Setup loss / optimizers
    gan_loss = GANLoss(use_hinge=False)  # or True for hinge
    nn_loss = NearestNeighborLoss(patch_size=3, stride=1)
    perceptual_loss = PerceptualLoss() if use_perceptual else None
    loss_manager = DeformGANLoss(gan_loss, nn_loss, perceptual_loss,
                                 lambda_nn=lambda_nn,
                                 lambda_perceptual=lambda_p,
                                 lambda_offset_smooth=lambda_off)

    optimG = torch.optim.Adam(netG.parameters(), lr=lr, betas=betas)
    optimD = torch.optim.Adam(netD.parameters(), lr=lr, betas=betas)

    for epoch in range(num_epochs):
        netG.train()
        netD.train()
        epoch_start = time.time()

        for i, batch in enumerate(train_loader):# CRAZYYY BUT NAHI SMJA
            src_img = batch['src_img'].to(device)
            tgt_img = batch['tgt_img'].to(device)
            src_pose = batch['src_pose'].to(device)
            tgt_pose = batch['tgt_pose'].to(device)

            # 1. Generate
            fake_img, offsets = netG(src_img, src_pose, tgt_pose)

            # 2. Discriminator update
            optimD.zero_grad()
            real_logits = netD(tgt_img, tgt_pose)
            fake_logits_D = netD(fake_img.detach(), tgt_pose)
            loss_D, dis_logs = loss_manager.compute_discriminator_loss(real_logits, fake_logits_D)
            loss_D.backward()
            optimD.step()

            # 3. Generator update
      
            for g_step in range(num_gen_updates):
                optimG.zero_grad()
                fake_img, offsets = netG(src_img, src_pose, tgt_pose)  # regenerate fake
                fake_logits_G = netD(fake_img, tgt_pose)
                loss_G, gen_logs = loss_manager.compute_generator_loss(
                    fake_logits_G, fake_img, tgt_img, offsets
                )
                loss_G.backward()
                optimG.step()

            if (i % 50) == 0:
                print(f"[Epoch {epoch}/{num_epochs}] Step {i}/{len(train_loader)} | "
                      f"D: {dis_logs['loss_d']:.4f} | G: {gen_logs['loss_g']:.4f}, nn: {gen_logs['loss_nn']:.4f}, "
                      f"p: {gen_logs['loss_p']:.4f}, off: {gen_logs['loss_off']:.4f}")

        # At end of epoch: sample / checkpoint / validation sample
        netG.eval()
        with torch.no_grad():
            val_batch = next(iter(val_loader))
            vs = val_batch['src_img'].to(device)
            vt = val_batch['tgt_img'].to(device)
            sp = val_batch['src_pose'].to(device)
            tp = val_batch['tgt_pose'].to(device)
            fake_v, _ = netG(vs, sp, tp)
            sample_fname = os.path.join(sample_dir, f"epoch_{epoch}.png")
            save_comparison_grid(vs, vt, tp, fake_v, sample_fname, nrow=vs.size(0))

        # Save checkpoint
        ckpt = {
            'epoch': epoch,
            'netG': netG.state_dict(),
            'netD': netD.state_dict(),
            'optimG': optimG.state_dict(),
            'optimD': optimD.state_dict(),
        }
        save_checkpoint(ckpt, checkpoint_dir, filename=f"ckpt_epoch_{epoch}.pth")
        save_checkpoint(ckpt, checkpoint_dir, filename="checkpoint_latest.pth")

        epoch_time = time.time() - epoch_start
        print(f"Epoch {epoch} done in {epoch_time:.2f} sec")

    print("Training finished.")
