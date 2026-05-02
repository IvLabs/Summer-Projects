SINGLE LEG:

#include <Servo.h>
#include <math.h>

// Link lengths (mm)
float L1 = 100;
float L2 = 80;

// Servo objects
Servo hipServo;
Servo kneeServo;

void setup() {
  Serial.begin(9600);
  hipServo.attach(10);   // Hip joint
  kneeServo.attach(9); // Knee joint
}

void loop() {
  // ---------- 1) Forward swing (semi-circle) ----------
  for (int i = 0; i <= 180; i += 5) {
    float t = i * M_PI / 180.0;    // convert to radians

    float px = 50 + (t / M_PI) * 50;   // forward x path
    float py = 50 * sin(t);            // swing arc y path

    moveLeg(px, py);
    delay(150);
  }

  // ---------- 2) Backward move (straight line along ground) ----------
  for (int i = 0; i <= 50; i += 2) {
    float px = 100 - i;  // move back from 100 → 50
    float py = 0;        // keep foot at ground level

    moveLeg(px, py);
    delay(150);
  }
}

// --------- Inverse kinematics function ----------
void moveLeg(float px, float py) {
  float r = sqrt(px*px + py*py);
  if (r > (L1 + L2)) {
    Serial.println("Point outside workspace!");
    return;
  }

  float cos_theta2 = (px*px + py*py - L1*L1 - L2*L2) / (2 * L1 * L2);
  cos_theta2 = constrain(cos_theta2, -1.0, 1.0);
  float theta2 = acos(cos_theta2);

  float const1 = atan2(py, px);
  float const2 = atan2(L2*sin(theta2), L1 + L2*cos(theta2));
  float theta1 = const1 - const2;

  // Convert radians → degrees
  float degHip  = theta1 * 180.0 / M_PI;
  float degKnee = theta2 * 180.0 / M_PI;

  // Debug print
  Serial.print("Target (");
  Serial.print(px); Serial.print(", ");
  Serial.print(py); Serial.print(") -> Hip=");
  Serial.print(degHip); Serial.print(", Knee=");
  Serial.println(degKnee);

  // Move servos (offsets may need tuning for your hardware)
  hipServo.write(degHip + 90);  // add offset so hip starts centered
  kneeServo.write(degKnee);
}