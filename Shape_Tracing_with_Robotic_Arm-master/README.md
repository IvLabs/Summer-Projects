# Shape Tracing with Robotic Arm

## Description


In this project, we have created a manipulator of 3 Degree of Freedom which moves in X-Y plane within its workspace and draw shapes accordingly.

<p align="center">
<image src="https://user-images.githubusercontent.com/108993449/197596223-350a1840-f1d7-459b-b260-47adfec11647.png" width="350" height="250">
  </p>

For our 3 DoF manipulator arm ,we studied and implemented the following-

- Forward Kinematics 
- Inverse Kinematics
- Trajectory Generation


##  Forward Kinematics
Forward kinematics is frequently used to know the position of end effector when we know the joint angles (theta1, theta2, and theta3).To calculate forward kinematics we can use trignometry or Denavit-Hartenberg parameters.
For this project we have used D-H paramters and following steps were taken-

- Found the D–H parameters of 3 DoF manipulator arm.
- Using SymPy (Symbolic python) created generalised homogeneous matrix and then substituited DH parameters to obtain the transformation from frame 3 to frame 0.
- Obtained the equations of x and y in terms of joint angles and other parameters which will be further used for inverse kinematics.
<p align="center">
<image align="centre" src="https://user-images.githubusercontent.com/108993449/197388420-f2e78226-776f-4065-b925-2b68d35d149c.png" width ="500" height="300" >
  </p>
  
## Inverse Kinematics

Inverse kinematics is about calculating the angles of joints (i.e. angles of the servo motors on the arm) that will cause the end effector of a manipulator arm to reach some given desired position (x, y, z) in 3D space.
To do that, we approximated the angles using Newon-Raphson method.

- Used the two equations obtained from Forward kinematics and third equation regarding the orientation of the end effector.
- Initial guesses were made for theta1, theta2, and theta3.
- Using appropriate first guess and the Newton-Raphson equation, the function value matrix and Jacobian matrix were obtained and hence obtaining joint angle values for a specific coordinate.
  
 Following are the results we obtained
  
   <p float="left">
  <image src="https://user-images.githubusercontent.com/108993449/197811121-ad1f64e9-3854-4908-a465-049475868b55.png" width="350" height="300" />
  <image src="https://user-images.githubusercontent.com/108993449/197811059-eb77233b-4949-4b29-91eb-9f2f60a66e84.png" width="350" height="300" />
  </p>





## Trajectory Generation
Trajectory planning is moving from point A to point B while avoiding collisions over time. This can be computed in both discrete and continuous methods.
Generating a trajectory is a crucial step in drawing shapes.


A desired trajectory is defined by some parameters, usually

• Initial and final point (point-to-point control). 

• Finite sequence of points along the path (motion through sequence of points) 


Inverse kinematics is calculated for these sequence of points to get trajectory of a line.
The trajectory for various shapes such as square, rectangle, and ellipse can be calculated using the same methodology as the line.

## Results
  Following Results were obtained 
  
  - Tracing a Line 
  <p float="left">
  <image src="https://user-images.githubusercontent.com/108993449/197814044-d463bc68-66a5-4228-83be-ac1eca8b7280.gif" width="350" height="300" />
  <image src="https://user-images.githubusercontent.com/108993449/197770862-09606c4b-78ee-4f71-bd50-0889e7a02df7.png" width="350" height="300" />
  </p>
  
  - Tracing a Rectangle
  <p float="left">
  <image src="https://user-images.githubusercontent.com/108993449/197806583-c9955128-aab8-4acd-9d82-a9241e00960f.gif" width="350" height="300" />
  <image src="https://user-images.githubusercontent.com/108993449/197806092-1db77428-1a5b-4b84-a474-aaedc0168a7d.png" width="350" height="300" />
  </p>
  
  - Tracing a Ellipse

<p float="left">
  <image src="https://user-images.githubusercontent.com/108993449/197807668-5c0c62b9-a8f3-44a7-b249-16c622de3707.gif" width="350" height="300" />
  <image src="https://user-images.githubusercontent.com/108993449/197809988-c352a60b-c43c-4a04-9a98-c9e1481790e3.png" width="350" height="300" />
  </p>
  
  - Tracing IvLabs
  <p align="center">
  <image align="centre" src="https://user-images.githubusercontent.com/108993449/197814860-974e0c4e-571a-4105-8171-3eaf3165e893.gif" width ="400" height="400" >
   </p>
  
