
# Ball And Plate System

## Objective

To balance a ball at any desired position on a plate using PID control.



## Workflow
 

### 1. Ball and Beam
First, we designed a Ball and Beam system where our goal was to balance the ball at any desired position on the beam.

The system was initially implemented in Python with the following results.
* Rise time =  1.71 seconds.
* Maximum overshoot = 3.57%

![babs](https://user-images.githubusercontent.com/109210914/196035822-4ff42dd6-65d2-43a9-8a1d-1faabdf6e566.png)



The system was later built with the following specifications and the desired results were obtained. 
* An ultrasonic sensor to get the position of the ball.
* An arduino UNO for the controller
* A servo to control the angle of the beam.



![ball_and_beam](https://user-images.githubusercontent.com/109210914/196095834-43c094b6-9f8e-4d77-b6de-a9d98c597ba4.gif)

#

### 2. Ball and Plate

Next, we implemented ball and plate system in Python with the following results.

* Rise time along x-axis is 1.86 seconds.
* Rise time along y-axis is 1.22 seconds.
* Maximum overshoot is less than 5% in both directions.

![bap1](https://user-images.githubusercontent.com/109210914/196409465-f74777ee-7f4e-4404-b855-240165e4a5ff.png)

![bap2](https://user-images.githubusercontent.com/109210914/196409503-cc0d28aa-3f67-4aa6-98da-6dec8ec10c6a.png)



The trajectory the ball will follow can be seen below.

![bap3](https://user-images.githubusercontent.com/109210914/196409553-19f59c7b-14b8-4831-a710-97be6a6b4acf.png)





