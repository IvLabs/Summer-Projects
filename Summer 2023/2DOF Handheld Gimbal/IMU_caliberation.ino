// Drift error: Although the IMU was kept stationary, it recorded a non-zero constant angular velocity. 
// To address this error, we calculated the average angular velocity while the IMU was held steady.
// We then subtracted this average value from every IMU reading as a calibration step in our project.

#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include <Servo.h>
Adafruit_MPU6050 mpu;
Servo sx;
Servo sy;

float w_x = 0; //angular velocity in x-direction
float w_y = 0; //angular velocity in y-direction
float w_x_c = 0; //caliberated angular velocity in x-direction
float w_y_c = 0; //caliberated angular velocity in y-direction
float w_x_sum = 0; //sum of angular velocities in x-direction
float w_y_sum = 0; //sum of angular velocities in y-direction

int delay_time=50;
int count = 0;

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

}

void loop() {
  count += 1;
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  w_x = g.gyro.z * (180/3.14);
  w_y = g.gyro.y * (180/3.14);

  w_x_sum += w_x;
  w_y_sum += w_y;

  w_x_c = w_x_sum/count; //Calculate average of angular velocities in x-direction
  w_y_c = w_y_sum/count; //Calculate average of angular velocities in y-direction

  Serial.print(w_x_c);
  Serial.print(", ");
  Serial.print(w_y_c);
  Serial.print("\n");

  delay(delay_time);
}