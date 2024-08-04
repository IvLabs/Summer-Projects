#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image,CameraInfo
from cv_bridge import CvBridge
from std_msgs.msg import String
import cv2 as cv
import numpy as np
from cv2 import aruco

class camera():
    def __init__(self):
        print("Initiated")
        rospy.init_node('camera',anonymous=True)
        self.pub = rospy.Publisher('aruco',String,queue_size=10)
        self.rate = rospy.Rate(10)
        print("Publisher started")
        self.marker_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
        self.param_markers = aruco.DetectorParameters_create()
        self.a = String()
        calib_data_path = "src/rosscans/src/MultiMatrix.npz"

        calib_data = np.load(calib_data_path)
        print(calib_data.files)
        
        self.r_vectors = calib_data["rVector"]
        self.t_vectors = calib_data["tVector"]
        self.mat =  calib_data["camMatrix"]
        self.dist = calib_data["distCoef"]
        self.cam_sub = cv.VideoCapture(2)
        
        while True:
            print("cam")
            ret, self.img=self.cam_sub.read()
            if not ret:
                break
            (ids,distance,centroids) = self.detection(self.img)
            print((ids,distance,centroids))
            self.publisher(ids,distance,centroids)
            cv.imshow('cv_image',self.img)
            self.rate.sleep()
            k=cv.waitKey(100)
            if k==ord('q'):
                self.cam_sub.release()
                cv.destroyAllWindows()
                break

        #self.cam_info_sub = rospy.Subscriber("/camera/rgb/camera_info", CameraInfo, self.globaler)
        

    '''def estimatePoseSingleMarkers(self,corners, marker_size):
        marker_points = np.array(
            [
                [-marker_size / 2, marker_size / 2, 0],
                [marker_size / 2, marker_size / 2, 0],
                [marker_size / 2, -marker_size / 2, 0],
                [-marker_size / 2, -marker_size / 2, 0],
            ],
            dtype=np.float32,
        )
        trash = []
        rvecs = []
        tvecs = []
        i = 0
        for c in corners:
            nada, R, t = cv.solvePnP(
                marker_points, corners[i], self.mat, self.dist, False, cv.SOLVEPNP_IPPE_SQUARE
            )
            rvecs.append(R)
            tvecs.append(t)
            trash.append(nada)
        return rvecs, tvecs, trash'''
    
    def callback(self,msg):
        print("callbacked")
        bridge = CvBridge()
        cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding='rgb8')
        (ids,distance,centroids) = self.detection(cv_image)
        self.publisher(ids,distance,centroids)
        cv.imshow('cv_image',cv_image)
        k=cv.waitKey(1)
        


    def globaler(self,data):
        self.mat = np.float32(data.K).reshape((3,3))
        self.dist = data.D

    def detection(self,image):
        print("detection started")
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        MARKER_SIZE = 10# centimeters
        dist = 0
        aruco_ids = []
        distance = []
        centroids = []
        #detector = cv.aruco.ArucoDetector(self.marker_dict,self.param_markers)
        corners, ids, reject = aruco.detectMarkers(
        gray, self.marker_dict, parameters=self.param_markers
    )
        if corners:
            print("detected")
            rVec, tVec, _ = aruco.estimatePoseSingleMarkers(
            corners, MARKER_SIZE, self.mat, self.dist
        )
            total_markers = range(0,ids.size)
            for ids, corners,i in zip(ids,corners,total_markers):
                
                aruco_ids.append(ids[0])
                cv.polylines(image, [corners.astype(np.int32)], True, (0, 255, 255), 4, cv.LINE_AA)
                corners = corners.reshape(4, 2)
                corners = corners.astype(int)
                top_right = corners[0].ravel()
                top_left = corners[1].ravel()
                bottom_right = corners[2].ravel()
                bottom_left = corners[3].ravel()
                centroids.append([top_left[0]+((top_right[0]-top_left[0])/2),top_left[1]+((bottom_left[1]-top_left[1])/2)])
                dist = np.sqrt(
                                tVec[i][0][2] ** 2 + tVec[i][0][0] ** 2 + tVec[i][0][1] ** 2
                            )
                distance.append(dist)
                point = cv.drawFrameAxes(self.img,self.mat, self.dist, rVec[0], tVec[0], 6, 4)
                #point = cv.drawFrameAxes(frame, cam_mat, dist_coef, rVec[i], tVec[i], 4, 4)
                cv.putText(
                    self.img,
                    "",
                    #"id: "+str(ids[0])+" Dist:"+str(round(distance, 2)),
                    tuple(top_right),
                    cv.FONT_HERSHEY_PLAIN,
                    1.3,
                    (0, 0, 255),
                    2,
                    cv.LINE_AA,
                )
                cv.putText(
                    self.img,
                    "",
                    #f"x:{round(tVec[i][0][0],1)} y: {round(tVec[i][0][1],1)} ",
                    tuple(bottom_right),
                    cv.FONT_HERSHEY_PLAIN,
                    1.0,
                    (0, 0, 255),
                    2,
                    cv.LINE_AA,
                )
            print(aruco_ids,centroids)
            return aruco_ids,distance,centroids
        else:
            aruco_ids, distance, centroid = [-1],[0],[[0,0]]
            return aruco_ids,distance, centroid

    def publisher(self,id,d,centre):
        self.a.data=str([id,d,centre])
        self.pub.publish(self.a)

if __name__=='__main__':
 try:
    print("Started")
    camera = camera()
    rospy.spin()  
 except rospy.ROSInterruptException:
    rospy.loginfo("node_terminated")
   

