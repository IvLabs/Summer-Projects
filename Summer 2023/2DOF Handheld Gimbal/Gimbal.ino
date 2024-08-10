#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include <Servo.h>
Adafruit_MPU6050 mpu;
Servo sx;
Servo sy;

float w_x = 0; //angular velocity in x-direction
float w_y = 0; //angular velocity in y-direction
float w_x_c = 0.12; //angular velocity in x-direction calibration
float w_y_c = -3.65; //angular velocity in y-direction calibration
float r_x = 90; //angle rotated in x-direction
float r_y = 90; //angle rotated in y-direction
float w_x_p = 0, w_y_p = 0; //previous iteration angular velocities in x and y directions
float a_x = 0, a_y; //angular acceleration in x and y directions

float kp = 10; //proportional gain
float kd = 1; //derivative gain
float ex,ey; //error in x and y directions
float epx = 0, epy = 0; //previous iteration error values in x and y directions
int delay_time=50; //time taken for each iteration
float anglex,angley; //inputs to both servo motors
float ux,uy; //PD controller output

void setup() {
  Serial.begin(9600);
  while (!Serial)
    delay(10);

  // Establish connection with the IMU
  if (!mpu.begin()) {
    while (1) {
      delay(10);
    }
  }

  //Attach servo motors to pins 9 and 10 of the Arduino UNO
  sx.attach(9);
  sy.attach(10);

}

void loop() {
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  //Obtain angular velocity readings from the IMU
  w_x = g.gyro.z * (180/3.14);
  w_y = g.gyro.y * (180/3.14);

  //Calibrate the readings to eliminate drift error
  w_x -= w_x_c;
  w_y -= w_y_c;

  //Calculate angular acceleration
  a_x = (w_x - w_x_p)/delay_time;
  a_y = (w_y - w_y_p)/delay_time;

  //Calculate angular rotation
  r_x += (w_x * delay_time * 0.001) + (0.5*a_x*(delay_time * 0.001)*(delay_time * 0.001));
  r_y += (w_y * delay_time * 0.001) + (0.5*a_y*(delay_time * 0.001)*(delay_time * 0.001));

  //Calculate error
  ex = r_x;
  ey = r_y;

  //Apply PD control
  ux = kp*ex +kd*(ex-epx);
  uy = kp*ey +kd*(ey-epy);

  //Display PD controller output on Serial Monitor
  Serial.print(ux);
  Serial.print(", ");
  Serial.print(uy);
  Serial.print("\n");

  //Map PD controller outputs to PWM values to control servo motors
  anglex =  map(ux,80,1700,0,180);
  angley =  map(uy,100,1700,0,180);

  //Resolve the issue of servo motors not rotating for PWM values within the range of 85-97.
  if(anglex>=85 && anglex<88){
    sx.write(85);
    
  }
  else if(anglex>=88 && anglex<=92){
    sx.write(90);
  }
  else if(anglex>92 && anglex<=97){
    sx.write(97);
  }
  else {
    sx.write(anglex);
  }
  if(angley>=85 && angley<88){
    sy.write(85);
    
  }
  else if(angley>=88 && angley<=92){
    sy.write(90);
  }
  else if(angley>92 && angley<=97){
    sy.write(97);
  }
  else {
    sy.write(angley);
  }

  epx=ex;
  epy=ey;
  w_x_p = w_x;
  w_y_p = w_y;

  delay(delay_time);
}