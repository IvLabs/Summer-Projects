# Speaker-Recognition
Speaker recognition is the process of automatically recognizing who is speaking on the basis of individual information included in speech waves.

![image](https://user-images.githubusercontent.com/92499855/137593881-06a6708a-43bf-4cec-bb01-7f21da458ae5.png)

### Workflow of project:
1) Pre-processing of input audio signal
2) Feature extraction (MFCC OR LPC)
3) Feature matching with LBG
4) Training 
5) Testing 
### Data
* The eight speakers data set were taken from [CSTR VCTK Corpus](https://datashare.ed.ac.uk/handle/10283/3443)
* In every audio file speakers utter "Please call stella".

### Mel frequency cepstral coefficients
* MFCCs are derived from a type of cepstral representation of the audio clip.  
* In MFCC the frequency bands are equally spaced on the mel scale, which approximates the human auditory system's response.  
* We have chosen MFCCs for feature extraction because they shows more significant variation from speaker to speaker since they are derived on logarithmic scale.
### Linear prediction coefficients
* LPCs are another popular feature for speaker recognition. To understand LPCs, we must first understand the Autoregressive model of speech.  
* Speech can be modelled as a pth order AR process. These coefficients give characteristics of input audio signal.
### LBG(Linde-Buzo-Gray)algorithm
* Linde-Buzo-Gray (LBG) Algorithm is used for designing of Codebook efficiently which has minimum distortion and error.  
* It is an iterative procedure and the basic idea is to divide the group of training vectors and use it to find the most representative vector from one group. 
* These representative vectors from each group are gathered to form the codebook. 
* Since codebook derived from LBG shows minimum distortion we have chosen this.


### Training and Testing
Model is trained over data sets (finding codebooks).  
Feed the model with testing data sets and find out which speakers from training data sets are matching with testing data sets respectively. 

### Results
Accuracy for model is 100 % for both mfccs and lpcs on CSTR VCTK Corpus data set.
### Note
Model show errors for a audio signal containing a silent part.
### References
1) Introduction to [speaker recognition project](https://minhdo.ece.illinois.edu/teaching/speaker_recognition/speaker_recognition.html)
2) [MFCC](http://www.practicalcryptography.com/miscellaneous/machine-learning/guide-mel-frequency-cepstral-coefficients-mfccs/)
3) [Pre processing and MFCC code reference](https://aadityachapagain.com/2020/08/asr-mfcc-filterbanks/)
4) [LPC reference slides](https://docs.google.com/presentation/d/1hBIF-j9fH92bnA72nzNQhTr5RXCcIK7AA-e6LIHX4Hw/edit#slide=id.gf4f26d30c1_0_13)
5) [K means clustering](https://github.com/CihanBosnali/Machine-Learning-without-Libraries/blob/master/K-Means-Clustering/K-Means-Clustering-without-ML-libraries.ipynb)
6) [complete project code reference](https://ccrma.stanford.edu/~orchi/Documents/speaker_recognition_report.pdf)
7) [Basics of signal processing videos](https://youtube.com/playlist?list=PLJ-OcUCIty7evBmHvYRv66RcuziszpSFB)
















