
# 2 Degree-Of-Freedom Handheld Gimbal

## Description

This project showcases a two degree-of-freedom gimbal system with independent control over each axis. The primary purpose of this gimbal system is to provide a stable platform for various applications, such as camera stabilization. 

![Gimbal](https://github.com/user-attachments/assets/10fecac1-9516-43e6-a66e-f77ad13e4df2)

## Tech Stack

**Softwares:** Arduino IDE, Python, Autodesk Fusion 360

**Python libraries:** Numpy, Matplotlib, Serial

**Arduino IDE libraries:** Adafruit_MPU6050, Adafruit_Sensor, Wire, Servo

## Components

| Type | Model     | Quantity                |
| :-------- | :------- | :------------------------- |
| Microcontroller Development Board | Arduino UNO | 1 |
| Inertial Measurement Unit (IMU) | MPU-6050 | 1 |
| Servo Motors | MG996R | 2 |



## Roadmap

- [Cruise Control](#cruise-control)

- [IMU and Servo Simulation](#imu-and-servo-simulation)

- [Polar Plot of IMU-Measured Angles](#polar-plot-of-imu-measured-angles)

- [Designing the 3-D Model of the Gimbal](#designing-the-3-D-model-of-the-gimbal)
## Cruise Control

**Aim:** Use Python to develop a Cruise Control for a car for a fixed set-point velocity.

The complete problem statement can be viewed [here](https://drive.google.com/file/d/13-e7mE6L7H6tf8J_iWNPkJWwlDUzuDqa/view?usp=sharing).

This task provided insights into the fundamentals of PID control and control systems. It demonstrates how PID parameters impact rise time, overshoot, steady-state error and settling time in our plot.

**Results:**

- Plot of Error over Time

![Error](https://github.com/user-attachments/assets/6d21b559-be45-4b01-a497-3096752444d0)

- Plot of Velocity over Time

![Velocity](https://github.com/user-attachments/assets/af51075d-1a6b-4f99-903e-70c51cffdb1b)

- Plot of Engine Force over Time

![Engine force](https://github.com/user-attachments/assets/2d4b9411-4359-4592-85a2-35c185c9e426)

## IMU and Servo Simulation

**Aim:** To simulate an IMU and map the change in angles onto two servos using PID. 

We used [Wokwi](https://wokwi.com/projects/371127545545264129) for simulation.

Here, our goal was to simulate the hardware environment before transitioning to the actual hardware components.

**Results:**

- Smooth changes in servo motor 1 shaft angle in response to IMU-Detected angle variations along the X axis

- Smooth changes in servo motor 2 shaft angle in response to IMU-Detected angle variations along the Y axis

https://github.com/user-attachments/assets/1a073bbd-720a-4a35-8dfc-b19c606130b2

## Polar Plot of IMU-Measured Angles

**Aim:** To create a polar plot in Python using the Matplotlib library, based on angle data obtained from the gyroscope within the IMU.

We learned how to establish serial communication between Arduino IDE and Python to import data from an Arduino. This allowed us to plot the changing angle from the IMU as it moves.

**Results:**

- Serial communication between Arduino IDE and Python without acquiring data from the IMU

https://github.com/user-attachments/assets/d157aaee-4eb1-4400-be2c-ea73b0982c2f

- Serial communication between Arduino IDE and Python with acquisition of data from the IMU

https://github.com/user-attachments/assets/17194a0c-a8ce-4f74-ab2a-49c1b4627774

## Designing the 3-D Model of the Gimbal

**Aim:** To create a 3D model of the gimbal with 2 degrees of freedom (DoF).

We created a 3D model of our gimbal using Autodesk Fusion 360. The model included two axes of rotation and a platform where the mobile phone and IMU were mounted.

**Results:**

https://github.com/user-attachments/assets/642365b4-85d7-40be-a47b-739ac4d9a51d

## Results

- We constructed a prototype using a metal framework to test the algorithm as shown below:

https://github.com/user-attachments/assets/c9a20e7a-f702-4368-ab20-9f0f2d926df7

- Upon deploying our code on the 3-D printed gimbal, we obtained the following results:

https://github.com/user-attachments/assets/96b0cb0c-0665-41ef-9e15-122bdcddc965

## Potential Further Improvements

- Adding a third degree of freedom to the system

- Utilizing OpenCV to achieve stabilization through visual parameters
## Authors

- [Aiden Ross D'souza](https://github.com/Aiden-Ross-Dsouza) [![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/aiden-dsouza/)
- [Shubham Pandere](https://github.com/ShubhamPandere) [![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/shubham-pandere-72b240259/)
- [Premansu Pradhan](https://github.com/premansupradhan) [![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/premansu-pradhan-82956425b/)
- [Manthan Gala](https://github.com/manthan451) [![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/manthan-gala/)
- [Asmit Panigrahi](https://github.com/Hack-asmit) [![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/asmit-panigrahi-6242b9278/)
- [Prathamesh Lakhotiya](https://github.com/DarkDestr0yer32) [![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/prathamesh-lakhotiya-925824258/)

## Mentors

- [Kishore P Chandra](https://github.com/k1sh0re) [![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/k1sh0re)
- [Pratyush Chakraborty](https://github.com/Pratyush-Chakraborty) [![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/pratyush-chakraborty-42b8a7236/)
