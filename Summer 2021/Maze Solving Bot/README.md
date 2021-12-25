![GIF](https://user-images.githubusercontent.com/91662557/137117706-a665ca46-5b92-46c0-a31f-c21f3cda81f7.gif)
# Maze Solver
## Description 
- This project uses the Wall Follower algorithm to solve a Simply Connected Maze on a Gazebo environment using Robot Operating System (ROS) using the sahayak robot.

## Tools used 
- Ubuntu, ROS, Gazebo.

## Algorithm 
- The Wall Follower algorithm follows a particular wall (right or left) until it reaches the end of the maze. 

## Environment 
- Gazebo provides an ideal environment where we can launch the sahayak robot using the following command and build a maze using the building model editor option in gazebo.

Type the following command in the terminal to launch sahayak in gazebo environment : roslaunch sahayak teleop.launch

## Code 
- Develop a node which subscribes values of the distances from neighbouring objects from laser/scan node and publishes the velocities to the nodes of the wheels.
