#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import time
from std_srvs.srv import Empty
import cv2
import numpy as np

x=0
y=0
yaw=0

def poseCallback(pose_message):
    global x
    global y, yaw
    x= pose_message.x
    y= pose_message.y
    yaw = pose_message.theta






# hand gesture movement

if __name__ == '__main__':
    try:
        
        rospy.init_node('turtlebot_motion_pose', anonymous=True)

        #declare velocity publisher
        cmd_vel_topic= '/cmd_vel'
        pub = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)
        rate = rospy.Rate(10) # 10hz
        
        # position_topic = "/turtle1/pose"
        # pose_subscriber = rospy.Subscriber(position_topic, Pose, poseCallback) 
        # time.sleep(2)

        move = Twist()

        # n = float(input("Enter the number"))
        move.linear.x = 0
        move.angular.z = 0
        acc = 0
        # while not rospy.is_shutdown():
        #     #hello_str = "hello world %s" % rospy.get_time()
        #     #rospy.loginfo(hello_str)
        #     pub.publish(move)
        #     rate.sleep()

        cap = cv2.VideoCapture(0)
        while not rospy.is_shutdown():
            # Take each frame
            _, frame = cap.read()

            # region of interest
            d_reg = frame[100:400,100:400]

            cv2.rectangle(frame,(100,100),(400,400),(0,255,0),1)
            
            
            # # Convert BGR to HSV
            hsv_image = cv2.cvtColor(d_reg, cv2.COLOR_BGR2YCR_CB)
            # convert to gray
            gray = cv2.cvtColor(d_reg, cv2.COLOR_BGR2GRAY)
            # Thresholding
            ret , threshold = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
            
            
            # Dilation + erosion
            kernel = np.ones((3,3),np.uint8)
            mask = cv2.dilate(threshold,kernel,iterations = 4)
            mask = cv2.erode(mask,kernel,iterations = 2)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            

            # median Blur
            mask = cv2.medianBlur(mask,5)
            
            
            # detecting hand by skin color
            lower_skin = np.array([0,58,30])
            upper_skin = np.array([33,255,255])
            filter_ = cv2.inRange(hsv_image, lower_skin, upper_skin)
            filter_ = cv2.erode(filter_,kernel,iterations = 1)
            
            # Finding combination of filter and mask
            comb = cv2.bitwise_or(filter_,mask)

            # cv2.imshow('comb', comb)


            # Finding Contours
            contours, hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            

            # Convex Hull
            if contours == []:
                pass
            else:
                # Finding max Contour
                cnt = max(contours, key = lambda x: cv2.contourArea(x))
                
                # Finding solidity
                hull = cv2.convexHull(cnt)
                area = cv2.contourArea(cnt)
                hull_area = cv2.contourArea(hull)
                solidity = float(area)/hull_area
                #print(solidity)

                # Finding extent
                area = cv2.contourArea(cnt)
                x,y,w,h = cv2.boundingRect(cnt)
                rect_area = w*h
                extent = float(area)/rect_area
                #print(extent)

                # Finding Aspect ratio
                x,y,w,h = cv2.boundingRect(cnt)
                aspect_ratio = float(w)/h
                #print(aspect_ratio)

                #print(solidity,'  ', extent, '  ', aspect_ratio)
                
                # Drawing Contours
                cv2.drawContours(d_reg, [hull], 0, (0,255,0), 2)
                
                # hull for finding defects
                hull = cv2.convexHull(cnt, returnPoints=False)
                defects = cv2.convexityDefects(cnt, hull)
                count_defects = 0
                count_defects2 = 0

                # Defects
                try:
                    for i in range(defects.shape[0]):
                        s,e,f,d = defects[i,0]
                        start = tuple(cnt[s][0])
                        end = tuple(cnt[e][0])
                        far = tuple(cnt[f][0])
                        a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
                        b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
                        c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)

                        s = (a+b+c)/2
                        ar = math.sqrt(s*(s-a)*(s-b)*(s-c))
                        d=(2*ar)/a
                        
                        # apply cosine rule here
                        angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
                        
                    
                        # ignore angles > 90 and ignore points very close to convex hull(they generally come due to noise)
                        if angle <= 90 and d>30:
                            count_defects += 1
                            cv2.circle(d_reg, far, 3, [255,0,0], -1)
                        
                        
                        # Finding angles greater than 90
                        if angle >= 90 and d>30:
                            count_defects2 += 1
                            cv2.circle(d_reg, far, 3, [0,0,255], -1)
                except:
                    print("no defect")


            # Detecting sign on basis of ratios obtained
            try:
                if count_defects == 0 :
                    if solidity > 0.94:
                        
                        move.linear.x = 0.1 + acc
                        acc += 0.01
                        move.angular.z = 0
                        print("accelarating at v = {}".format(move.linear.x))
                        cv2.putText(frame,'9-Accelarating',(100,99), cv2.FONT_HERSHEY_SIMPLEX, 2,(255,255,255),2,cv2.LINE_AA)
                        
                    elif solidity > 0.85 and solidity < 0.94:
                        cv2.putText(frame,'0-Stationary',(100,99), cv2.FONT_HERSHEY_SIMPLEX, 2,(255,255,255),2,cv2.LINE_AA)
                        move.linear.x = 0
                        move.angular.z = 0
                        acc = 0
                        print("Turtle Stationary")
                    elif solidity < 0.85:
                        cv2.putText(frame,'1-moving forward',(100,99), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2,cv2.LINE_AA)
                        move.linear.x = 0.15
                        move.angular.z = 0
                        print("moving forward")
                
                
                if count_defects == 1:
                    cv2.putText(frame,'2-moving backward',(100,99), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2,cv2.LINE_AA)
                    move.linear.x = -0.15
                    move.angular.z = 0
                    print("moving backward")
                
                if count_defects == 2:
                    cv2.putText(frame,'3-turn right',(100,99), cv2.FONT_HERSHEY_SIMPLEX, 2,(255,255,255),2,cv2.LINE_AA)
                    move.angular.z = -0.8
                    move.linear.x = 0
                    print("rotating right")
                
                if count_defects == 3:
                    cv2.putText(frame,'4-turn left',(100,99), cv2.FONT_HERSHEY_SIMPLEX, 2,(255,255,255),2,cv2.LINE_AA)
                    move.angular.z = 0.8
                    move.linear.x = 0
                    print("rotating left")
                
                if count_defects == 4:
                    cv2.putText(frame,'5-BOOST!!!',(100,99), cv2.FONT_HERSHEY_SIMPLEX, 2,(255,255,255),2,cv2.LINE_AA)
                    
                    move.linear.x = 0.5
                    move.angular.z = 0
                    print("Boost 3x speed")
            except:
                cv2.putText(frame,"-",(200,450),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2,cv2.LINE_AA)
                move.linear.x = 0
                move.angular.z = 0
            
            cv2.imshow('frame',frame)

            cv2.imshow('mask',mask)
            
            pub.publish(move)
            rate.sleep()
            # cv2.imshow('res',res)
            i = 0
            k = cv2.waitKey(25) & 0xFF
            if k == 27:
                break
        cv2.destroyAllWindows()


       
    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated.")