import numpy as np,cv2 as cv 
from matplotlib import pyplot as plt

def nothing(x):
    pass


img_on_left = cv.imread('python\im0.png',0)
img_on_right = cv.imread('python\im1.png',0)
cv.namedWindow('disp',cv.WINDOW_NORMAL)
cv.resizeWindow('disp',300,300)
cv.namedWindow('img',cv.WINDOW_NORMAL)
cv.resizeWindow('img',600,600)

cv.createTrackbar('numDisparities','disp',1,17,nothing)
cv.createTrackbar('blockSize','disp',5,50,nothing)
cv.createTrackbar('preFilterType','disp',1,1,nothing)
cv.createTrackbar('preFilterSize','disp',2,25,nothing)
cv.createTrackbar('preFilterCap','disp',5,62,nothing)
cv.createTrackbar('textureThreshold','disp',10,100,nothing)
cv.createTrackbar('uniquenessRatio','disp',15,100,nothing)
cv.createTrackbar('speckleRange','disp',0,100,nothing)
cv.createTrackbar('speckleWindowSize','disp',3,25,nothing)
cv.createTrackbar('disp12MaxDiff','disp',5,25,nothing)
cv.createTrackbar('minDisparity','disp',5,25,nothing)

stereo = cv.StereoBM_create()


while True:

    numDisparities = cv.getTrackbarPos('numDisparities','disp')*16
    blockSize = cv.getTrackbarPos('blockSize','disp')*2 + 5
    preFilterType = cv.getTrackbarPos('preFilterType','disp')
    preFilterSize = cv.getTrackbarPos('preFilterSize','disp')*2 + 5
    preFilterCap = cv.getTrackbarPos('preFilterCap','disp')
    textureThreshold = cv.getTrackbarPos('textureThreshold','disp')
    uniquenessRatio = cv.getTrackbarPos('uniquenessRatio','disp')
    speckleRange = cv.getTrackbarPos('speckleRange','disp')
    speckleWindowSize = cv.getTrackbarPos('speckleWindowSize','disp')*2
    disp12MaxDiff = cv.getTrackbarPos('disp12MaxDiff','disp')
    minDisparity = cv.getTrackbarPos('minDisparity','disp')
            
    stereo.setNumDisparities(numDisparities)
    stereo.setBlockSize(blockSize)
    stereo.setPreFilterType(preFilterType)
    stereo.setPreFilterSize(preFilterSize)
    stereo.setPreFilterCap(preFilterCap)
    stereo.setTextureThreshold(textureThreshold)
    stereo.setUniquenessRatio(uniquenessRatio)
    stereo.setSpeckleRange(speckleRange)
    stereo.setSpeckleWindowSize(speckleWindowSize)
    stereo.setDisp12MaxDiff(disp12MaxDiff)
    stereo.setMinDisparity(minDisparity)



    # stereo = cv.StereoBM_create(numDisparities, blockSize)
    disparity = stereo.compute(img_on_left,img_on_right)
    disparity = disparity.astype(np.float32)
    disparity = (disparity/20.0 - minDisparity)/numDisparities
    cv.imshow("img",disparity)
    if cv.waitKey(1) == 27:
        break