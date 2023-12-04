# Autonomous Lane Following Robot

### Description

For self-driving cars as well as conventional computer vision, lane detection is a critical component. This project aims to identify lanes and steer the robot along the detected path. We will be using live camera feeds or video frames and different computer vision techniques to detect lanes algorithms on a ground robot.

### ROS - Robot Operating System

We learned about basic ROS commands and did some task to get familiar on how to move the turtlebot later in the project.

We learned:
* ROS Topics, Nodes, Messages
* Publisher & Subscriber
* ROS Services
* RQT Graphs

We used this knowledge to trace some basic shapes and other task on TurtleSim to get familiar on how to subscribe and publish from any ROS topic.

### Turtlesim

We did the following task in Turtlesim:

> Circle

<img src="https://user-images.githubusercontent.com/92629417/197455894-23a603e1-9239-4745-900d-45690bd41a75.gif" height="250"/>

> Square Spiral

<img src="https://user-images.githubusercontent.com/92629417/197455902-295241d9-73ad-4eab-867c-f90efeb2f81a.gif" height="250"/>

> Go to Goal

<img src="https://user-images.githubusercontent.com/92629417/197455887-3a734f2d-c62f-4995-972f-692ed789c3e1.gif" height="250"/>

> Follower

<img src="https://user-images.githubusercontent.com/92629417/197455890-ee2e2415-a235-4bce-951c-9727fa2afd20.gif" height="250"/>

### Lane Detection using OpenCV

We used OpenCV to process and identify the lane from the live camera feed. We used various image processing techniques to achieve this task namely HSV Color Selection, Canny Edge Detection Algorithm and Houghlines Transform.

> Original Image

<img src="https://user-images.githubusercontent.com/94111518/198004191-e4222642-ee36-42e1-aafd-c599593dd7ca.jpg" height="250"/>

> HSV Color Selection

<img src="https://user-images.githubusercontent.com/94111518/198001549-0056b271-222b-4551-a0af-c3b1ca7e307e.jpg" height="250"/>

> Canny Edge Detection

<img src="https://user-images.githubusercontent.com/94111518/198001680-d56a75e9-892d-43bd-8806-8a87439f33f3.jpg" height="250"/>

> Houghlines Transformation

<img src="https://user-images.githubusercontent.com/94111518/198001714-0f15a2bf-c1f8-4caf-94c4-2f6edb364674.jpg" height="250"/>

### Lane Detection Algorithm

Upon getting the two Houghlines:
* We calculated the inclination of both the lines and compute their average to find the direction in which its moving.
* Then from the direction we pass the linear velocity and angular velocity commands accordingly to move the robot.
* Robot continues to move till both the lanes are detected stops when they finish

<img src="https://user-images.githubusercontent.com/94111518/198004673-6b2c7bba-55d6-483a-8841-09249163dde6.gif" height="250"/>

### Result

Upon deploing our code on TurtleBot we got the following result:

<img src="https://user-images.githubusercontent.com/94111518/198002775-a191b201-838d-43d1-be3a-8490bc05382a.gif" height="250"/>

### Further Improvemens

* Make the robot move more accurately
* Move continously without jerking
