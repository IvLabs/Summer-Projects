import cv2 as cv
from cv2 import aruco
import numpy as np
calib_data_path = "../calib_data/MultiMatrix.npz"
calib_data = np.load(calib_data_path)
print(calib_data.files)
cam_mat = calib_data["camMatrix"]
dist_coef = calib_data["distCoef"]
r_vectors = calib_data["rVector"]
t_vectors = calib_data["tVector"]
MARKER_SIZE = 8  # centimeters
marker_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50) 
param_markers = aruco.DetectorParameters()
cap = cv.VideoCapture(0)
mat=None
dist=None


def my_estimatePoseSingleMarkers(corners, marker_size):
        
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
        mat = calib_data["camMatrix"]
        dist = calib_data["distCoef"]
        for c in corners:
            nada, R, t = cv.solvePnP(
                marker_points, corners[i],mat, dist, False, cv.SOLVEPNP_IPPE_SQUARE
            )
            rvecs.append(R)
            tvecs.append(t)
            trash.append(nada)
        return rvecs, tvecs, trash
while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    detector = cv.aruco.ArucoDetector(marker_dict,param_markers)
    (marker_corners, marker_IDs, rejected)=detector.detectMarkers(gray_frame)
    if marker_corners:
        rVec, tVec, trash = my_estimatePoseSingleMarkers(marker_corners, MARKER_SIZE)
        total_markers = range(0, marker_IDs.size)
        for ids, corners, i in zip(marker_IDs, marker_corners, total_markers):
            cv.polylines(
                frame, [corners.astype(np.int32)], True, (0, 255, 255), 4, cv.LINE_AA
            )
            corners = corners.reshape(4, 2)
            corners = corners.astype(int)
            top_right = corners[0].ravel()
            top_right = tuple(top_right)
            top_left = corners[1].ravel()
            bottom_right = corners[2].ravel()
            bottom_right = tuple(bottom_right)
            bottom_left = corners[3].ravel()
            print(tVec[i][2])

            # Since there was mistake in calculating the distance approach point-outed in the Video Tutorial's comment
            # so I have rectified that mistake, I have test that out it increase the accuracy overall.
            # Calculating the distance
            distance = np.sqrt(
                tVec[i][2][0]**2 + tVec[i][0][0]**2 + tVec[i][1][0]**2
            
            )
            # Draw the pose of the marker
            
            point = cv.drawFrameAxes(frame, cam_mat, dist_coef, rVec[i], tVec[i], 4, 4)
            cv.putText(
                frame,
                
            
                
                f"id: {ids[0]} Dist: {round(distance, 2)}",
                top_right,
                cv.FONT_HERSHEY_PLAIN,
                1.3,
                (0, 0, 255),
                2,
                cv.LINE_AA,
            )
            cv.putText(
                frame,
                f"x:{round(tVec[i][0][0],1)} y: {round(tVec[i][1][0],1)} ",
                bottom_right,
                cv.FONT_HERSHEY_PLAIN,
                1.0,
                (0, 0, 255),
                2,
                cv.LINE_AA,
            )
            # print(ids, "  ", corners)
    cv.imshow("frame", frame)
    key = cv.waitKey(1)
    if key == ord("q"):
        break
cap.release()
cv.destroyAllWindows()
