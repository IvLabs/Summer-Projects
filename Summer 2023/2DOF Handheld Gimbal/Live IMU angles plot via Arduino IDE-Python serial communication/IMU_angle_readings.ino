#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
Adafruit_MPU6050 mpu;

float w_x = 0; //angular velocity x-direction
float w_y = 0; //angular velocity y-direction
float w_x_c = -0.29; //angular velocity x-direction calibration
float w_y_c = 1.80; //angular velocity y-direction calibration
float r_x = 0; //angle rotated in x-direction
float r_y = 0; //angle rotated in y-direction

int delay_time=50;
void setup() {
  Serial.begin(115200);

  // Establish connection with the IMU
  if (!mpu.begin()) {
    while (1) {
      delay(10);
    }
  }
}

void loop() {
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  //Obtain angular velocity readings from the IMU
  w_x = g.gyro.x * (180/3.14);
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

  Serial.print(r_x);
  Serial.print(",");
  Serial.print(r_y);

  delay(delay_time); 
}
