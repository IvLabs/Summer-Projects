# HAND-GESTURE-CONTROLLED-ROBOT
________________________________
This project is about controlling robot motion with hand gestures which have commands like rotate, move forward and backward, accelarate and stop.The project have two parts ➡
 1) Detection of Hand_Gesture using opencv library.
 2) Integrating Hand_Gesture to publish commands to robot.

# DEPENDENCIES/PACKAGES
________________________
 1) Image processing library opencv 
 2) ROS(Robot operating system , version-noetic)
 3) Gazebo (if not installed along with ROS)
 4) pakages :-
   - ros_controll {To be cloned in catkin_ws}
   - Join_state_controller (if not included in ros_controll) {To be cloned in src folder of catkin_ws}
   - Turtlebot3 pakage - (https://emanual.robotis.com/docs/en/platform/turtlebot3/simulation/#gazebo-simulation) {To be cloned in src folder of catkin_ws}
         


# ALGORITHM
____________

 # ALGORITHM FOR DETECTION OF HAND_GESTURE
   1) Seperate out the skin color from the input frame using HSV or other color format with upper and lower bound for skin color as per range. Removal of noise from image via Morphological Transformation, and applying filters to smooothen the image.Finding the contour of the mask and finding its convex-hull.
   2) Using the various properties for seperation various Hand_Gestures(In this project we will use Indian-sign-language as Hand_Gesture- 1,2,3..) like- convexity defects along with contour properties like solidity, extent and aspect ratio of respective gesture.

 # ALGORITHM FOR ROBOT
   For this project we used ROS noetic, turtlesim and turtlebot3.
   1) We used gazebo for simulation.
   2) We used ros-topic /cmd_vel for publishing velocity message to robot in gazebo simulation.
 
 # INTEGRATION
   Finally we publish angular and linear velocity as per motion we want on specific Hand_Gesture.
   
# HOW TO RUN THE CODE 
________________________
  1) git clone https://github.com/ash-S26/Hand_Gesture_Controlled_Robot.git
  2) export TURTLEBOT3_MODEL=burger  {as per requirement burger/waffle/empty}
  3) roslaunch turtlebot3_gazebo turtlebot3_empty_world.launch
  4) python3 Hand_Gestur_Controlled_Robot.py {Finally run the code by navigating to directory where you cloned and then to where is code Hand_Gestur_Controlled_Robot.py}
  5) Or you can run code from any code editor.
  
# RESULTS 
______________________________________
  HAND_GESTURE_DETECTION :-
  
  ![](https://github.com/ash-S26/Hand_Gesture_Controlled_Robot/blob/main/Results/hand_detection.gif)
  
  _________________________________
  
  CONTROLLING ROBOT IN EMPTY WORLD WITH HAND :-
  
  ![](https://github.com/ash-S26/Hand_Gesture_Controlled_Robot/blob/main/Results/hand_gesture_control_robot_empty_world.gif)
  
  _________________________________
  
  CONTROLLING ROBOT IN WAFFLE WORLD WITH HAND :-
  
  ![](https://github.com/ash-S26/Hand_Gesture_Controlled_Robot/blob/main/Results/hand_gesture_control_robot_waffle_world.gif)
  
  ________________________________________
  
