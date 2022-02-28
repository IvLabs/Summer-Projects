# MNIST-FashionMNIST-Image-Denoising-Autoencoder-Using-CNN
Implementation of Image-Denoising Autoencoder on MNIST/FashionMNIST by using Pytorch and CNN
## Table Of Contents:
1. [MNIST/FashionMNIST-Dataset](#mnist-fashionmnist-dataset)


2. [Architecture](#architecture)
3. [Adding Noise](#adding-noise)
4. [Hyperparameters](#hyperparameters)
5. [Training With Flowchart](#training-with-flowchart)
6. [Loss plots of iterations](#loss-plots-of-iterations)
7. [Results and Outputs](#results-and-outputs)
8. [Resources](#resources)



## MNIST-FashionMNIST-Dataset
The [MNIST](http://yann.lecun.com/exdb/mnist/) and [Fashion MNIST](https://github.com/zalandoresearch/fashion-mnist) datasets are used. These datasets contain 60,000 training samples and 10,000 test samples. Each sample in the MNIST dataset is a 28x28 pixel grayscale image of a single handwritten digit between 0 & 9, whereas each sample in the Fashion MNIST dataset is a 28x28 grayscale image associated with a label from 10 types of clothing.

 

![](https://i.imgur.com/FhAVzAp.png)









## Hyperparameters

| Hyperparaeter |value          |
| ------------- | ------------- |
| Batch-Size    | 64            |
| Learning-rate | 0.001         |
| Weight-decay  | 0.00001       |
| num of Epochs | 10            |
|  Loss         |  MSE LOSS     |
|  Optimizer    | Adam Optimizer|

## Adding Noise
* ```torch.randn``` is used to create a noisy tensor of the same size as the input. The amount of Gaussian noise can be changed by changing the multiplication factor.
 
 ![](https://i.imgur.com/xeT9wzT.png)


## Architecture 

```   python
      #Encoder
      self.encoder = nn.Sequential(
            nn.Conv2d(1, 16, 3, stride=2, padding=1), # -> N, 16, 14, 14
            nn.ReLU(),
            nn.Conv2d(16, 32, 3, stride=2, padding=1), # -> N, 32, 7, 7
            nn.ReLU(),
            nn.Conv2d(32, 64, 7) # -> N, 64, 1, 1
        )
        
      #Decoder
      self.decoder = nn.Sequential(
            nn.ConvTranspose2d(64, 32, 7), # -> N, 32, 7, 7
            nn.ReLU(),
            nn.ConvTranspose2d(32, 16, 3, stride=2, padding=1, output_padding=1), # N, 16, 14, 14 (N,16,13,13 without output_padding)
            nn.ReLU(),
            nn.ConvTranspose2d(16, 1, 3, stride=2, padding=1, output_padding=1), # N, 1, 28, 28  (N,1,27,27 without output_padding)
            nn.Sigmoid()
        )
      
        
 ```
## Training with flowchart
![](https://i.imgur.com/2YV6uPE.png)

In denoising autoencoder some noise is introduced to the input images. The encoder network downsamples the data into a lower-dimensional latent space and then the decoder reconstructs the original data from the lower-dimensional representation. MSE loss between the original image and the reconstructed image is calculated and is backpropagated. Value of the parameters is updated using Adam optimization to reduce the reconstruction error.

## Loss plots of iterations
![](https://i.imgur.com/Nv85Rrv.png)


## Results and Outputs
![](https://i.imgur.com/5TNsDG0.png)
![AutoencoderMnistCNN ipynb - Colaboratory - Google Chrome 10-10-2021 11_44_01 (3)](https://user-images.githubusercontent.com/87975841/136731685-6dc4a90e-e016-424e-bbba-a91ef1a5d4fa.png)


## Resources
- [Coursera Deep learning](https://www.coursera.org/specializations/deep-learning?)
- [Pytorch Documentation](https://pytorch.org/)
- [Denoising AE](https://lilianweng.github.io/lil-log/2018/08/12/from-autoencoder-to-beta-vae.html)
- [Notes for deep learning](https://aman.ai/coursera-dl/)
- [Autoencoder basic understanding](https://www.youtube.com/watch?v=q222maQaPYo&t=104s)

Thanks to all contributors for providing great resources for learning


