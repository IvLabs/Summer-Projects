# Cruise Control
## Objective
To develop a cruise control for a car which needs to move at a fixed set-point velocity.

## PID Controller
PID control stands for proportional integral derivative control and is one of the most popular control method used in robotics.

Working of the PID controller:

1. The Proportional component is used to bring the process variable close to the set point and depends on the difference between the set point and the process variable, it is given by :  $e(t) = S.P - P.V$
3. Integral component is used to remove the steady state error by taking into account the past values of error and suming it over time, it is given by : $e_i(t) =  \int_{0}^{t} e(t) dt$
4. The Derivative component is used to reduce the overshoot and is proportional to the rate of change of error, it is given by : $e_d(t) = \dfrac{de(t)}{dt}$ 

The overall equation for a pid controller is given by:

$u(t) = K_pe(t) + K_i \int_{0}^{t} e(t) dt + K_d \dfrac{de(t)}{dt}$

## Workflow 
The equation of motion for the motion of the car was found to be : $mv'+bv = u$
Where u is the input force provided by the engine and b is the drag coefficient.

Our goal was to apply a PID controller on the system and to satify the follow conditions:
* The rise time for the system should be less than 10 seconds.
* The maximum overshoot should be less than 5%

The system was implemented in Python with the following results.
* Rise time  = 1.09 seconds.
* Maximum overshoot = 1.35%

![cruise](https://user-images.githubusercontent.com/109210914/196035804-36c04ede-36d8-4b54-bc71-bb0aad3f6c71.png)



#
