# ﻿Indoor Navigation using ArUco Markers

## Description

In our project, we've employed Turtlebot for autonomous indoor navigation which involves using marker-based localization, like ArUco. These markers act as crucial reference points for the robot's autonomous movement within unfamiliar indoor spaces. This approach is cost-effective, simply requiring the deployment of marker patterns and protective measures. For the completion of this project, we also made use of ROS, OpenCV, and Gazebo simulation, enabling us to navigate, control, and process data for various robotic applications, which could include warehouse management

## Methodology

- **Turtlesim**

We performed simple tasks on turtlesim node to get practical knowledge about ROS.
How to write code in ROS, implement different publisher and subscriber nodes.


| <img src="https://github.com/shreyaskkk12/Indoor-Navigation-IvLabs/assets/128238705/0b62366a-62af-420b-8637-6cbe254db07c" width="width_of_img" height="height" /> | <img src="https://github.com/shreyaskkk12/Indoor-Navigation-IvLabs/assets/128238705/ac06461e-3083-4cb3-99f0-d0db776115a3" width="width_of_img2" height="height2" /> |
| :--: | :--: |
| Circle | Spiral |

| <img src="https://github.com/shreyaskkk12/Indoor-Navigation-IvLabs/assets/128238705/829176c4-1675-45ef-821f-0036aa4a9588" width="width_of_img" height="height" /> | <img src="https://github.com/shreyaskkk12/Indoor-Navigation-IvLabs/assets/128238705/cf1a9fab-80ef-4ff1-b149-fcc0a4eb88d7" width="width_of_img2" height="height2" /> |
| :--: | :--: |
| Go To Goal | Follower |



- **SLAM - Hector and G-mapping**

Hector SLAM and Gmapping are both algorithms used for mapping and localization in robotics. Hector SLAM is a laser-based algorithm that can only afford indoor use, as the map created is small, while Gmapping can be used both indoors and outdoors. Hector SLAM is more efficient than Gmapping in terms of map drawing, but it has a limit on the size of the map it can create. On the other hand, Gmapping has no such limit and is more versatile than Hector SLAM

| <img src="https://github.com/shreyaskkk12/Indoor-Navigation-IvLabs/assets/128238705/460920a5-6d15-4d2b-b6ef-1b3d86b5347e" width="width_of_img" height="height" /> | <img src="https://github.com/shreyaskkk12/Indoor-Navigation-IvLabs/assets/128238705/46dbf6e9-b57e-4bb1-a68d-d7ee38f8ce56" width="width_of_img2" height="height2" /> |
| :--: | :--: |
| Hector Mapping | GMapping |


- **Camera Calibration** 

The process of estimating the parameters of a camera is called camera calibration. This includes recovering two kinds of parameters 

1. **Internal parameters** of the camera/lens system. E.g. focal length, optical center, and radial distortion coefficients of the lens                                                                 
2. **External parameters**: This refers to the orientation (rotation and translation) of the camera with respect to some world coordinate system                                                               We used a checkerboard for the calibration of the camera as its pattern is easy to detect in an image, also its corners have a sharp gradient in two directions, so it is easy to detect the corners. 

![Callibration](https://github.com/shreyaskkk12/Indoor-Navigation-IvLabs/assets/128238705/425b5acf-4fb0-4b32-b460-c4220e20e297)



- **Aruco Detection and Pose Estimation**

We used OpenCV’s aruco library for the detection and pose estimation of aruco markers.

![ArucoDetection](https://github.com/shreyaskkk12/Indoor-Navigation-IvLabs/assets/128238705/e2f04d65-2a48-43ef-8ab9-ec74e880b834)


- **Gazebo Simulation**

We used two nodes for navigation. The camera node detects the markers and publishes data about markers like their IDs and distance. Nav node subscribes data from the camera node and publishes velocity commands to turtlebot. 
We used turtlebot’s ‘waffle_pi’ model for simulation as it comes with a camera. To get camera information we created a subscriber in the camera node.

Working :
Nav node publishes velocity commands so turtlebot moves in a square loop until it finds any marker.  After finding the marker bot will do a task assigned to that ID. We assign a simple task to each ID. The bot should go towards markers up to a certain distance and then again start searching for another marker. 

![ezgif com-video-to-gif](https://github.com/shreyaskkk12/Indoor-Navigation-IvLabs/assets/128238705/a21c4525-08ee-471b-933f-c309023ac8c0)


- **Implementation on Hardware**

Our turtlebot model was “burger”, which requires ‘ros-melodic’. So we require docker to create a ros-melodic workspace.
We also had to change our Cam node code such that it takes video input from a webcam instead of a subscriber.


## Requirements

Software:

- Ubuntu 20.04
- Python3
- ROS-Noetic
- Docker Image for ROS-Melodic
- OpenCV 4.8.x (Noetic)
- OpenCV 4.2.x (Melodic)
- Gazebo simulation package 

Hardware:

- TurtleBot Burger Model [Kobuki]
- Webcam
- YdLidar

## How to use the Project
### <a name="_q09s3zjlqn8o"></a>**For Simulation**
1. Create a catkin package
   1. Go to `cd ~/catkin_ws/src`
   1. Do `catkin_create_pkg indoor_nav rospy turtlesim geometry_msgs sensor_msgs std_msgs`
   1. Go back to `cd ~/catkin_ws` 
   1. Do `catkin_make`
1. Put camFeed.py, velcmds.py and markers.launch (or any gazebo world) in your catkin package and make them executable files.
1. In your terminal, run the following code:
   1. `roslaunch indoor_nav markers.launch`
   1. `rosrun indoor_nav cam.py`
   1. `rosrun indoor_nav navi.py`

### <a name="_wwhunr977nm1"></a>**For Hardware**
1. Create a catkin package in **both**, your docker container (ROS-melodic) as well as your main device (ROS-noetic)
   1. Go to `cd ~/catkin_ws/src`
   1. Do `catkin_create_pkg indoor_nav rospy turtlesim geometry_msgs sensor_msgs std_msgs`
   1. Go back to `cd ~/catkin_ws `
   1. Do `catkin_make`
1. Put lidar_data.py code in your ROS-Noetic package and camera.py, MultiMatrix.npz, and navi.py code as well as a lidar_data.txt file in your ROS-melodic package, and make these all executable files.
1. Make sure to change calib_data_path in camera.py to MultiMatrix.npz path. Also, change lidar_data_path in lidar.py to the relative path of lidar_data.txt to your ROS-noetic terminal, and in navi.py to the relative path to your container.
1. Connect your TurtleBot to your device and run the following code in your container:
   1. `bash .devcontainer/post_create_commands.sh`
   1. `roslaunch turtlebot_bringup minimal.launch`
1. In your ROS-noetic terminal, run the following code:
   1. `roscore`
   1. `rosrun lidar_data.py`
1. In your container, run the following code:
   1. `roscore`
   1. `rosrun camera.py`
   1. `rosrun navi.py`

## Results

![output](assets/output.gif)
