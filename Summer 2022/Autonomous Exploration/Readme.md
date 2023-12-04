



# Autonomous Exploration using Turtlebot <img src="https://user-images.githubusercontent.com/92629417/197411798-d35da8fb-9153-4104-9faa-556a2e9cdeab.gif" width="35" height="32" />  <img src="https://user-images.githubusercontent.com/92629417/197412192-87d76ad9-b654-4701-9e0f-12b7c35552b6.gif" width="35" height="32" /> 

## Table of Contents 
- [Description](#description-robot)
- [Turtlesim](#turtlesim-turtle)
- [Turtlebot3 Simulation and Mapping](#turtlebot3-simulation-and-mapping)
- [Docker](#docker-)
- [Results](#results)
  - [Avoiding Obstacles](#avoiding-obstacles--)
  - [Maps](#maps-of-a-corner-of-lab--)
- [Looking Forward to](#looking-forward-to--)

## Description :robot:

<img src="https://user-images.githubusercontent.com/92629417/197410812-79a8e4d7-0d01-465a-ab1f-d3432ba14ab7.gif" width="795" height="400" />

This project uses Robot Operating System(ROS) to move Turtlebot autonomously in an unexplored area with the help of [LiDAR](https://www.ydlidar.com/products/view/5.html) and at the same time create a map of the area. 

## Turtlesim :turtle:

To understand some basic functionalities of [rospy](http://wiki.ros.org/rospy) library which is used throughout this project and velocity control of a robot, Turtlesim node is used.

Tracing some common shapes - 

| <img src="https://user-images.githubusercontent.com/92629417/197455894-23a603e1-9239-4745-900d-45690bd41a75.gif" width="240" height="240" /> | <img src="https://user-images.githubusercontent.com/92629417/197455897-aa6f057d-232e-444d-80ae-d93939ea146e.gif" width="240" height="240" /> | <img src="https://user-images.githubusercontent.com/92629417/197455902-295241d9-73ad-4eab-867c-f90efeb2f81a.gif" width="240" height="240" /> |
|:--:|:--:|:--:|
| Circle | Square | Square Spiral | 

Applying P controller to control the turtles - 

| <img src="https://user-images.githubusercontent.com/92629417/197455887-3a734f2d-c62f-4995-972f-692ed789c3e1.gif" width="240" height="240" /> | <img src="https://user-images.githubusercontent.com/92629417/197455890-ee2e2415-a235-4bce-951c-9727fa2afd20.gif" width="240" height="240" /> | <img src="https://user-images.githubusercontent.com/92629417/197455895-86bd9a2a-42df-4db1-8d2a-657670bb71f1.gif" width="240" height="240" /> |
|:--:|:--:|:--:|
| Go-to-goal | Leader Follower | Formation Control |

## Turtlebot3 Simulation and Mapping
We first performed teleoperation(operating manually through keyboard) and both mapping techniques in simulation and then we implemented the same on hardware.  

### Teleoperation - 

<img src="https://user-images.githubusercontent.com/92629417/197505977-3fdeaa08-2800-4817-8a8e-3d43cf1e60b4.gif" width="775" height="450" />

### Hector mapping - 

<img src="https://user-images.githubusercontent.com/92629417/197514237-3412ad9a-a43d-4632-84fe-2f55bfd28662.gif" width="775" height="450" />

In hector-slam, it uses previous scan results to estimate the current state of the system. So a drift from the beginning will be recorded and results in a random rotation and translation of the map frame against other ground truth frames

### Gmapping -

<img src="https://user-images.githubusercontent.com/92629417/197510766-f0a685ce-dfee-46c4-8dbf-706d42d9e39b.gif" width="775" height="450" />

## Docker <img src="https://user-images.githubusercontent.com/92629417/197572181-a6bd28c5-6a82-4978-990f-806e2162290a.png" width="33" height="23" />

To run the code on Turtlebot2, we used ROS melodic installed in a Docker container.

To setup the Docker Container and connect to Turtlebot2  
- Install [Docker](https://docs.docker.com/engine/install/) on your device
- Extract the Turtlebot2.zip file, provided in this repository, and open it in VsCode
- Build the container and try resolving the errors, if any 
- In new Terminal, Run the command ``` bash .devcontainer/post_create_commands.sh``` 
- Connect the Kobuki cable to your pc and in new terminal run ``` roslaunch turtlebot_bringup minimal.launch```

## Results
We finally deployed our code on Turtlebot2 and, after facing some issues and refactoring the code, we got the following results - 

### Avoiding Obstacles - 

<img src="https://user-images.githubusercontent.com/92629417/197415431-5d706210-aaee-475d-a602-25d47e0e69dd.gif" width="380" height="420" /> <img src="https://user-images.githubusercontent.com/92629417/197417790-4b180820-5ce3-470d-84f3-7ccb0ca5a69d.gif" width="390" height="420" /> 

The ranges' list in LiDAR [data](http://docs.ros.org/en/melodic/api/sensor_msgs/html/msg/LaserScan.html) has a length of 720. Central region is defined in first 40 values and last 40 values which would correspond to 20 degrees left and right of the normal line to the robot. Left and Right regions are defined by next 140 values from beginning and end of the list respectively. Average value of range is found in each of these regions and if found less than the safe distance of robot from an obstacle, in any region then move or turn or move in some other direction.

As we used only one sensor in this project, which is LiDAR, only hector mapping was possible.

### Maps of some parts of Lab - 
<img src="https://user-images.githubusercontent.com/92629417/197415489-86161f30-7bc2-4045-9f5c-5765d663839a.PNG" width="380" height="350" /> <img src="https://user-images.githubusercontent.com/92629417/197415484-4bcf2629-d223-4d5b-bb7f-dd3a98e8d82f.PNG" width="380" height="350" />

### Map of a corridor area - 
<img src="https://user-images.githubusercontent.com/92629417/222418513-fca783fb-a0e7-4f95-924b-bf75f6c68bfb.png" width="350" height="300" /> <img src="https://user-images.githubusercontent.com/92629417/222419563-e5fb1856-b53d-4476-a55b-8d44fe5022a9.png" width="410" height="300" />

## Looking Forward to -
- [ ] Removing Distortions in the maps
- [ ] Applying Path Planning [Algorithms](https://en.wikipedia.org/wiki/Motion_planning#Algorithms)
