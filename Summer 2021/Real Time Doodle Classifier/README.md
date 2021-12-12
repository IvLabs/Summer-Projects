# Doodle-Classifier-CNN
The Doodle classifier is based on a Convolutional Neural Network which classifies the doodle input given by the user in 20 different classes.

![ezgif com-gif-maker (5)](https://user-images.githubusercontent.com/73688295/139387196-b6ac70a2-2aa8-489d-8060-89eaaf52d012.gif)

![ezgif com-gif-maker (6)](https://user-images.githubusercontent.com/73688295/139387379-9c6ae33a-145a-43a7-91e8-4a5022c3ea03.gif)


## Dataset
The Neural Network Model was trained on a dataset consisting of 2807037 images containing images of 20 differnt classes.Each image is of the size 28 x 28.
Dataset link: https://drive.google.com/file/d/1HS05bmAim7YRod3edsoMyQtXG_k1agJJ/view?usp=sharing

![data (1)](https://user-images.githubusercontent.com/73688295/137096046-372afdbc-a076-4c2f-ba7a-adc4fb8d9696.png)

## Approach
The preliminary stage involved studying and learning the basics of Machine Learning and Deep Learning algorithms.

For the better understanding of the topic, we first developed a Digit Classifier from scratch using the MNIST dataset using Numpy library. All the functions were build from scratch for the Forward as well as Backward propagation.

The CNN model is build with the help of PyTorch library for the convolution of image with filters along with maxpooling. After multiple convolutional layers, the input representation is flattened into a feature vector and passed through a dense neural network for the output.
A Drawing Pad is created using OpenCv for getting input from the user.
PySimpleGUI is used for implementing GUI.

## Libraries required
- PyTorch (For implementing Neural Network and its training)
- OpenCV (For creating drawing pad)
- Matplotlib (for plotting graphs and reading images)
- Numpy
- PySimpleGUI
## CNN Model
### Architecture 
Convolutional Layer
|Layer|Kernel size| Filters|Maxpool|Padding|
|---|--|--|--|--|
|Conv1| (5,5)|8|(2,2)|1|
|Conv2| (5,5)|16|(2,2)|1|
|Conv3|(3,3)|28|None|1|
|Conv4|(3,3)|48|None|1|


Fully Connected Layer
|Layer|Size|
|--|--|
|Fc layer1|(48 x 5 x 5,500)|
|Fc layer2|(500,250)|
|Fc layer3|(250,20)|

### Hyper parameters
|Parameters| Values|
|------|---|
| Learning rate|0.01|
|Epochs|100|
|Batch size|1200|
|Beta|0.9|
|Optimizer|SGD|
|Loss function|BCE Loss|

## Output of Model
The Loss Vs number of Epochs
![Screenshot (138)](https://user-images.githubusercontent.com/73688295/137258580-a812e140-cc36-4c8a-b44f-63c26c1a7600.png)


|Dataset|Accuracy | 
|----|----|
|Training dataset| 95.77 %|
| Testing dataset|  95.74 %|

## Final result

![ezgif com-gif-maker (2)](https://user-images.githubusercontent.com/73688295/139380623-b9614ad1-14ed-44f1-aa3b-c47591bf37df.gif)


![ezgif com-gif-maker](https://user-images.githubusercontent.com/73688295/139380411-fe981d78-9a1d-481b-a26e-c0e9bb768ec3.gif)







