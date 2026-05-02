#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
#include <EEPROM.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

#define SERVO_MIN 154
#define SERVO_MAX 528
#define NUM_LEGS 4
#define DOF 3

// --- Each servo's zero offset angle ---
int servoZero[NUM_LEGS][DOF] = {
  {0, -10, -85},
  {40, 70, 0},
  {0, -45, -105},
  {-10, -40, 100}
};

// --- PCA9685 channel mapping ---
uint8_t servoChannels[NUM_LEGS][DOF] = {
  {6, 2, 0},   // leg 1
  {7, 3, 1},   // leg 2
  {8, 13, 14}, // leg 3
  {9, 12, 15}  // leg 4
};

// Convert angle to PWM
int angleToPulse(float angle) {
  return map(round(angle), -90, 90, SERVO_MIN, SERVO_MAX);
}

// --- EEPROM Functions ---
void saveZeroPositions() {
  int addr = 0;
  for (int i = 0; i < NUM_LEGS; i++) {
    for (int j = 0; j < DOF; j++) {
      EEPROM.put(addr, servoZero[i][j]);
      addr += sizeof(int);
    }
  }
  Serial.println("✅ Zero positions saved to EEPROM!");
}

void loadZeroPositions() {
  int addr = 0;
  for (int i = 0; i < NUM_LEGS; i++) {
    for (int j = 0; j < DOF; j++) {
      EEPROM.get(addr, servoZero[i][j]);
      addr += sizeof(int);
    }
  }
  Serial.println("✅ Zero positions loaded from EEPROM!");
}

// --- Servo Movement Functions ---
void writeServoAngle(int leg, int joint, int angle) {
  uint16_t pulselen = angleToPulse(angle);
  pwm.setPWM(servoChannels[leg][joint], 0, pulselen);
}

void moveServoToZero(int leg, int joint) {
  writeServoAngle(leg, joint, servoZero[leg][joint]);
}

void standStillAtZero() {
  for (int i = 0; i < NUM_LEGS; i++) {
    for (int j = 0; j < DOF; j++) {
      moveServoToZero(i, j);
    }
  }
}

void flushSerial() {
  while (Serial.available()) Serial.read();
}

void setup() {
  Serial.begin(115200);
  Serial.println("🐾 Quadruped Servo Calibration Mode 🐾");

  pwm.begin();
  pwm.setPWMFreq(50);
  delay(100);

  // Load EEPROM offsets
  loadZeroPositions();
  standStillAtZero();

  Serial.println("Format: <leg> <joint> <angle>");
  Serial.println("Example: 1 2 30  → move leg1 joint2 to +30° and return");
  Serial.println("Example: 1 2 999 → save current zero for leg1 joint2");
}

void loop() {
  if (Serial.available() > 0) {
    int leg, joint, angle;

    // Read 3 numbers (leg joint angle)
    leg = Serial.parseInt();
    joint = Serial.parseInt();
    angle = Serial.parseInt();

    flushSerial(); // clear junk like \n

    // basic input check
    if (leg < 1 || leg > NUM_LEGS || joint < 1 || joint > DOF) {
      Serial.println("❌ Invalid leg or joint index");
      return;
    }

    leg -= 1;   // convert to array index
    joint -= 1;

    if (angle == 999) {
      // Save current zero to EEPROM
      saveZeroPositions();
      Serial.print("💾 Saved zero positions for leg ");
      Serial.print(leg + 1);
      Serial.print(" joint ");
      Serial.println(joint + 1);
      return;
    }

    if (angle < -90 || angle > 90) {
      Serial.println("❌ Invalid angle range (-90 to 90 only)");
      return;
    }

    // Move servo to given angle
    writeServoAngle(leg, joint, angle);
    delay(800);

    // Return ONCE to zero
    moveServoToZero(leg, joint);
    Serial.print("✅ Returned to zero of leg ");
    Serial.print(leg + 1);
    Serial.print(", joint ");
    Serial.println(joint + 1);
  }
}
