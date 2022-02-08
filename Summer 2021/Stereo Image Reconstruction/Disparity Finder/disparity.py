import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt


img_on_Left=cv.imread('python\im0.png',0)
img_on_Right=cv.imread('python\im1.png',0)



doffs=124.343
b=193.001
f=3979.911
window_size2=5 
width=2964
height=2000
ndisp=270
isint=0
vmin=23
vmax=245
dyavg=0
dymax=0

stereo =  cv.StereoSGBM_create(minDisparity = 23, numDisparities = 223, blockSize = 3, uniquenessRatio = 5, speckleWindowSize = 50, speckleRange = 2, disp12MaxDiff = 0, P1 = 8*3*window_size2, P2 = 32*3*window_size2)
dis = stereo.compute(img_on_Left,img_on_Right).astype(np.float32)/223
dis = cv.GaussianBlur(dis,(5,5),2,2)
plt.imshow(dis,"jet")
plt.show()
