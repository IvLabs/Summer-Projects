#!/usr/bin/env python3

import rospy
import cv2
from sensor_msgs.msg import Image, CameraInfo
from cv_bridge import CvBridge, CvBridgeError
from cv2 import aruco
import numpy as np
from std_msgs.msg import String

class camFeed():
    def __init__(self):
            rospy.init_node("camFeed", anonymous=True)
            # print("node initialised")
            self.pub=rospy.Publisher("aruco",String,queue_size=10)
            self.s=String()
            self.sub2 = rospy.Subscriber("/camera/rgb/camera_info", CameraInfo, self.globaler)
            self.sub1 = rospy.Subscriber("/camera/rgb/image_raw", Image, self.callback)
            self.mat = None
            self.dist = None
            

    def my_estimatePoseSingleMarkers(self,corners, marker_size):
        # estimatePoseSingleMarkers no longer exists as of version 4.7. replaced the function for you using SolvePnP
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
            nada, R, t = cv2.solvePnP(
                marker_points, corners[i], self.mat, self.dist, False, cv2.SOLVEPNP_IPPE_SQUARE
            )
            rvecs.append(R)
            tvecs.append(t)
            trash.append(nada)
        return rvecs, tvecs, trash


    def raveled(self,corners):
        (topLeft, topRight, bottomRight, bottomLeft) = corners
        return (topLeft.ravel(), topRight.ravel(), bottomRight.ravel(), bottomLeft.ravel())

    def published(self):
            self.s.data=str(self.pubber)
            self.pub.publish(self.s)
            print(">>>",self.s)
            self.pubber=[]

    def callback(self,data):
        dist=self.dist
        self.pubber=[]
        print("callback CAlled")
        try:
            bridge = CvBridge()
            frame = bridge.imgmsg_to_cv2(data, desired_encoding="rgb8")
        except CvBridgeError as e:
            print(e)
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        MARKER_SIZE = 4  # centimeters

        marker_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
        param_markers = aruco.DetectorParameters()
        detector = aruco.ArucoDetector(marker_dict, param_markers)
        marker_corners, IDs, reject = detector.detectMarkers(gray)
        
        print(marker_corners)
        if len(marker_corners) > 0 :
            print("GOt Aruco")
            rVec, tVec, _ = self.my_estimatePoseSingleMarkers(marker_corners, MARKER_SIZE)

            print("New Marker")
            for ids, corners, i in zip(IDs, marker_corners, range(0, (IDs).size)):
                cv2.polylines(frame, [corners.astype(np.int32)], True, (0, 255, 255), 4)
                corners = corners.reshape((4, 2)).astype((np.int32))
                (topLeft, topRight, bottomRight, bottomLeft) = self.raveled(corners)

                distance = np.sqrt(
                    float(tVec[i][2] ** 2) + float(tVec[i][0] ** 2) + float(tVec[i][1] ** 2)
                )
                
                # Draw the pose of the marker
                point = cv2.drawFrameAxes(frame, self.mat, self.dist, rVec[i], tVec[i], 6, 4)
                cv2.putText(
                    frame,
                    f"id: {ids[0]} Dist: {round(distance, 2)}",
                    topRight,
                    cv2.FONT_HERSHEY_PLAIN,
                    1.3,
                    (0, 0, 255),
                    2,
                    cv2.LINE_AA,
                )
                cv2.putText(
                    frame,
                    f"x:{round(float(tVec[i][0]),1)} y: {round(float(tVec[i][1]),1)} ",
                    bottomRight,
                    cv2.FONT_HERSHEY_PLAIN,
                    1.0,
                    (0, 0, 255),
                    2,
                    cv2.LINE_AA,
                )
                self.pubber.append([ids[0],distance,round(float(tVec[i][0]),1),round(float(tVec[i][1]),1),round(float(tVec[i][2]),1)])
            self.published()
            
        else:
            print("No Markers")
            self.published([])    

        cv2.imshow("image", frame)
        cv2.waitKey(1)


    def globaler(self,data):
        self.mat = np.float32(data.K ).reshape((3,3))
        self.dist = data.D
        


if __name__ == "__main__":
    cf = camFeed()
    rospy.spin()
    cv2.destroyAllWindows()
