# Image-Colorisation-Project
## Table of Contents
* [Description](#description "Goto Description")
* [Dataset](#dataset "Goto Dataset")
* [Methods](#methods "Goto Methods ")
* [Model Architecture](#model-architecture "Goto Model Architecture")
* [Hyperparameters](#hyperparameters "Goto Hyperparameters")
* [Results](#results "Goto Results")
## Description
In this project we have used autoencoder to train the network to colorise the grayscale images.
## Dataset
Dataset used for this project is torch.torchvision.datasets.Flowers102 which consists of RGB images of various types of flowers.
## Methods
* Autoencoder:We have used autoencoder in this project.Autoencoder is a neural network which is composed of encoder,bottleneck latent space and a decoder.
 
* Transfer Learning: Transfer learning is the reuse of a pre-trained model on a new problem. In transfer learning, a machine exploits the knowledge gained from a previous task to improve   generalization about another.

* ResNet 18 Gray: Deep neural networks are hard to train as their depth increases. This increase in depth comes with many problems such as vanishing and exploding gradient descent . Residual Networks or ResNets are a solution to such problems.
In this project we have used Resnet 18 Gray which is a pretrained Convolutional neural network that is 18 layers deep,but we have used just first 6 layers of this    network.ResNet 18 Gray is pretrained on grayscale images, therefore it is used to extract features from the grayscale image. Hence we utilized transfer learning in the encoder block of autoencoder.

* LAB Color Space: We have used LAB Color Space in this project as by separating out the lightness component, the neural network only has to learn the remaining two channels which contain the information for colorization.

## Model Architecture
![Arcitecture](https://cdn.discordapp.com/attachments/993239385891942421/1030118698071101500/unknown.png)
## Hyperparameters 
|Hyperparameter |Description|
|-----|--------|
| Optimiser|Adam Optimiser      |
|Learning rate  | 0.001      |
| Loss Function | MSE loss |
| Batch size | 60 |

## Results
![image](https://user-images.githubusercontent.com/107758088/201471166-0cb44295-4a02-4b37-ab5f-e9d5c7444419.png)
