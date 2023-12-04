
#include <Servo.h>
Servo s;
const float kp = 5;
const float kd = 10;
const float ki = 0;

const int echo = 2;
const int trig = 3;
const int servo = 6;

float d = 0;
float t = 0;
float angle = 0;
float u = 0;
float e = 0;
float ei = 0;
float ed = 0;
float eo = 0;
const float r = 20;
const float dt = 0.1;

void setup() {
  pinMode(echo, INPUT);
  pinMode(trig, OUTPUT);
  s.attach(servo);
  Serial.begin(9600);
}

void loop() {
  digitalWrite(trig, LOW);
  delayMicroseconds(1);
  digitalWrite(trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig, HIGH);
  t = pulseIn(echo, HIGH);
  d = t * 0.017;
  if (d > 34) {
    d = 34;
  }
  if (d < 6) {
    d = 6;
  }

  e = r - d;
  ei = ei + (e * dt);
  ed = (e - eo) / dt;
  u = kp * e + ki * ei + kd * ed;
  //Serial.println(angle)

  if (d <= 17 or d >= 20) {
    angle = map(u, 1460 * 1.5, -1460 * 1.5, 25, 85);
  }
  else if (d > 17 or d < 20) {
    angle = map(u, 1460 * 2.5, -1460 * 2.5, 25, 85);
  }

  if (angle < 25) {
    angle = 25;
  }
  if (angle > 85) {
    angle = 85;
  }

  s.write(angle);


}
