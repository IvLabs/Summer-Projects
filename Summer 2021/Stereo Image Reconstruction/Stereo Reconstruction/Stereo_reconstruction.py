
"""
Values are modified for bike calibration
"""


#Importing libraries
import cv2 as cv ,numpy as np
from matplotlib import pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D

#Initializing matplotlib
figure = plt.figure()

#Taking Images as input (lef and right view)
img_on_Left=cv.imread('python\im0.png',0)
img_on_Right=cv.imread('python\im1.png',0)

#camera parameters 
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

#Creating Disparity Map
stereo =  cv.StereoSGBM_create(minDisparity = 23, numDisparities = 223, blockSize = 3, uniquenessRatio = 5, speckleWindowSize = 50, speckleRange = 2, disp12MaxDiff = 0, P1 = 8*3*window_size2, P2 = 32*3*window_size2)
dis = stereo.compute(img_on_Left,img_on_Right).astype(np.float32)/223
#applying gaussianblur on disparity map 
dis = cv.GaussianBlur(dis,(5,5),2,2)

#Projective matrix
Q = np.array([[1, 0, 0, -2964/2], [0, 1, 0, -2000/2],[0, 0, 0, f],[0, 0, -1/b, doffs/b]])
#obtaining 3D coordinates 
xyz = cv.reprojectImageTo3D(dis, Q)

img = cv.imread('python\im0.png')
#seperating coordinates 
x=xyz[:,:0]
y=xyz[:,:1]
z=xyz[:,:2]
pointpro=np.hstack((x,y,z))
col = img
#reshaping coordinates and color arrays
xyz = xyz.reshape(-1,3)
col = col.reshape(-1,3)
# stacking coordinates and its corresponding colors  in correct order (x,y,z,r,g,d)
xyz = np.hstack([xyz, col])


#creating PLY header and defining elements and its properties 
ply_header = '''ply
	format ascii 1.0
	element vertex %(vert_num)d
	property float x
	property float y
	property float z
	property uchar blue
	property uchar green
	property uchar red
	end_header
	'''
#opening ply file and saving  coordinates and their corresponding colors 
with open('bike.ply', 'w') as f:
	f.write(ply_header %dict(vert_num = len(xyz)))
	np.savetxt(f, xyz, '%f %f %f %d %d %d')

# print(x)
# print(y)
# print(z)
# loc=xyz[:,:3]
# locrgb=xyz[:,3:]
# ax = plt.axes(projection='3d')
# ax.scatter(loc[:,2],loc[:,1],loc[:,0] ,c = locrgb/255, s=0.040)
plt.imshow(dis,'jet')
# plt.imshow(dis,"jet")
plt.xticks([])
plt.yticks([])

plt.show()




"""
Commented code can be use for plotting in matplotlib
"""







