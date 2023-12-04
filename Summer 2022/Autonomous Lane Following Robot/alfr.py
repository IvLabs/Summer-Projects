import cv2
import numpy as np
import math

video=cv2.VideoCapture("output.mp4")
while True:
    ret,frame=video.read()

    if ret == True:
        img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        lower_red = np.array([34, 28, 0])
        upper_red = np.array([179,255,255])
        img_red_mask = cv2.inRange(img_hsv, lower_red, upper_red)

        img_canny = cv2.Canny(img_red_mask, 50, 150)

        lines = cv2.HoughLinesP(img_canny, 1, np.pi/180,60,maxLineGap=500,minLineLength=100)

        # removing extra lines
        x_bottom_pos = []
        x_upper_pos = []
        x_bottom_neg = []
        x_upper_neg = []

        y_bottom = 540
        y_upper = 0


        for line in lines:
            for x1,y1,x2,y2 in line:
                if x1==x2:
                    continue
                m=(y2-y1)/(x2-x1)
                b=y1-(m*x1)

                if m>0:
                    x_bottom_pos.append((y_bottom - b)/m)
                    x_upper_pos.append((y_upper - b)/m)
                elif m<0:
                    x_bottom_neg.append((y_bottom - b)/m)
                    x_upper_neg.append((y_upper - b)/m)

        a1=np.mean(x_bottom_pos)
        a2=np.mean(x_upper_pos)
        a3=np.mean(x_bottom_neg)
        a4=np.mean(x_upper_neg)
        a1=int(a1)
        a2=int(a2)
        a3=int(a3)
        a4=int(a4)
        lines_average=np.array([[a1,y_bottom,a2,y_upper],[a3,y_bottom,a4,y_upper]])   
        
        theta = 0
        
        for i in range(len(lines_average)):
            cv2.line(frame,(lines_average[i, 0], lines_average[i, 1]), (lines_average[i, 2], lines_average[i, 3]),[0,255,0],3)
            theta=theta+math.atan2((y2-y1),(x2-x1))

        threshold=5
        if(theta>threshold):
            print("Go left")
        if(theta<-threshold):
            print("Go right")
        if(abs(theta)<threshold):
            print("Go straight")
        
        cv2.imshow("final",frame)


        k = cv2.waitKey(60) & 0xff
        if k == 27:
            break
        else:
            cv2.imwrite(chr(k)+".jpg",frame)
    else:
        break
cv2.destroyAllWindows()
video.release()
