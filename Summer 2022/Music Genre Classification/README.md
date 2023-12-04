# MUSIC GENRE CLASSIFICATION


The main aim of the project is to identify the genre of the music clips.This is done using GTZAN dataset. With the help of PyTorch , Convolutional neural network is made of 3 convolutional and 4 linear layers . ReLu activation function and SGD optimizer with learning rate =0.0005 is used .

**BASIC FLOW :**


```mermaid
flowchart TD;
    DATASET-->SPECTOGRAM ;
    SPECTOGRAM -->CNN;
    CNN--> GENRE_CLASSIFICATION ;
```


For the input the spectograms were generated which were then passed to the convolutional neural network and with the help of genre as labels the classification was done.

**Genres:**

- Blues

- Classical

- Country

* Disco

* Hiphop

* Jazz

* Metal

* Pop

* Reggae

* Rock


## Accuracy 


Train set : 100 %


Test set : 65 %




Accuracy plot :

![image](https://github.com/coderhetal/Music-genre-classification-/assets/109482222/44b80a01-0bf1-4fae-b347-41177fd9b28b)



Loss plot :

![image](https://github.com/coderhetal/Music-genre-classification-/assets/109482222/072fd3b7-e578-4849-8dbe-72ea8a40598e)




## By using pretrained (ResNet18 Architecture )
### Accuracy 


Train set : 100 %


Test set : 100 %






Accuracy plot :

![image](https://github.com/coderhetal/Music-genre-classification-/assets/109482222/a0efde6d-af8b-4c9b-ab22-8746be1bcae0)


Loss plot :

![image](https://github.com/coderhetal/Music-genre-classification-/assets/109482222/8d6fb38b-5629-42fb-8e8c-e4f7b393291c)


