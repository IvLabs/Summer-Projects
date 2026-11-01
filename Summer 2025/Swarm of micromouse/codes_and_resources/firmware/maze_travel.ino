#include <Arduino.h>

// ================= User Tunables =================
#define TICKS_FOR_90_DEG_TURN_LEFT  505
#define TICKS_FOR_90_DEG_TURN_RIGHT -505
const long TICKS_FOR_180_DEG_TURN = TICKS_FOR_90_DEG_TURN_RIGHT * 2;

// Cell travel (avg encoder ticks for ONE cell)  <<< CALIBRATE
const long TICKS_PER_CELL = 950;

// Wall thresholds (cm)
#define WALL_DETECT_CM      4    // front is considered blocked if <= this
#define WALL_SIDE_OPEN_CM   8    // side is considered open if > this
#define SIDE_VALID_MAX_CM   18   // ignore side readings above this as unreliable
#define SIDE_TARGET_CM      5    // desired side clearance when hugging/centering

// Forward alignment PID (wall-centering while moving)
const uint8_t BasePWM = 215;     // your working base speed
const uint8_t MIN_PWM  = 60;     // do not go below to avoid stall
const float FW_KP = 35.0;        // wall-centering P
const float FW_KD = 3.0;       // wall-centering D
const float SYNC_KP = 0.6;       // encoder speed sync P 0.6

// Controller sample
const int SampleTime = 20;       // ms
const unsigned long CELL_SETTLE_MS = 500; // wait at cell center

// ================= Pinout (your mapping) =================
// --- Motor A (RIGHT MOTOR) ---
const int IN1 = 13, IN2 = 23, EN1 = 32; // Right Motor
const uint8_t encoder_A_A = 19, encoder_A_B = 21; // Right Encoder

// --- Motor B (LEFT MOTOR) ---
const int IN3 = 27, IN4 = 26, EN2 = 33; // Left Motor
const uint8_t encoder_B_A = 18, encoder_B_B = 22; // Left Encoder

// --- PID for turn (as you had) ---
double Kp_turn = 1.5, Ki_turn = 0.0, Kd_turn = 0.0;
double Kp_sync = 0.0, Ki_sync = 0.0, Kd_sync = 0.0;

// ================= State =================
// A = Right Motor, B = Left Motor
volatile long encoderCountA = 0; // Right Encoder Count
volatile long encoderCountB = 0; // Left Encoder Count
long prevCountA = 0;
long prevCountB = 0;
float integralError = 0;
unsigned long prevMillis = 0;

// --- Simple orientation & cell indexing (optional) ---
int orient = 0; // 0=N,1=E,2=S,3=W

// --- Sensor Struct (as you had) ---
typedef struct{
  int trigPin;
  int echopin;
  int dist;
} Sensor;

Sensor sensor[3] = {{4,15,0},{4,12,0},{4,14,0}}; // {Left, Front, Right}

// ================= Helpers =================
static inline int clampInt(int v, int lo, int hi){ return v<lo?lo:(v>hi?hi:v); }
static inline bool validSide(int cm){ return (cm > 1 && cm < SIDE_VALID_MAX_CM); }

// -------- ENCODER ISRs (Mapped to new pins) -------- //
// (ICACHE_RAM_ATTR works; IRAM_ATTR is the ESP32-native name)
void IRAM_ATTR encoderISR_A() { // RIGHT Motor ISR
  if (digitalRead(encoder_A_B) == digitalRead(encoder_A_A)) {
    encoderCountA++;
  } else {
    encoderCountA--;
  }
}
void IRAM_ATTR encoderISR_B() { // LEFT Motor ISR
  if (digitalRead(encoder_B_B) != digitalRead(encoder_B_A)) {
    encoderCountB++;
  } else {
    encoderCountB--;
  }
}

// -------- MOTOR HELPERS (your wiring preserved) -------- //
void moveForward(int pwmRight, int pwmLeft) {
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW); // Right Fwd
  digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW); // Left Fwd
  analogWrite(EN1, clampInt(pwmRight, 0, 255));
  analogWrite(EN2, clampInt(pwmLeft,  0, 255));
}

void turnLeft(int pwmRight, int pwmLeft) { // CCW: Right Fwd, Left Rev
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW); // Right Fwd
  digitalWrite(IN3, LOW);  digitalWrite(IN4, HIGH); // Left Rev
  analogWrite(EN1, clampInt(pwmRight, 0, 255));
  analogWrite(EN2, clampInt(pwmLeft,  0, 255));
}

void turnRight(int pwmRight, int pwmLeft) { // CW: Right Rev, Left Fwd
  digitalWrite(IN1, LOW);  digitalWrite(IN2, HIGH); // Right Rev
  digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW);  // Left Fwd
  analogWrite(EN1, clampInt(pwmRight, 0, 255));
  analogWrite(EN2, clampInt(pwmLeft,  0, 255));
}

void stopMotors() {
  digitalWrite(IN1, LOW); digitalWrite(IN2, LOW); analogWrite(EN1, 0); // Right Stop
  digitalWrite(IN3, LOW); digitalWrite(IN4, LOW); analogWrite(EN2, 0); // Left Stop
}

// -------- SENSOR FUNCTIONS -------- //
long readUltrasonic(int echoPin, int trigPin) {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  long duration = pulseIn(echoPin, HIGH, 25000); // 25ms timeout
  if (duration == 0) return 999;
  return duration * 0.034 / 2;
}

void readAllSensors() {
  for(int i = 0; i < 3; i++){
    sensor[i].dist = readUltrasonic(sensor[i].echopin, sensor[i].trigPin);
    delay(15);
  }
  // Debug
  Serial.print("L:"); Serial.print(sensor[0].dist);
  Serial.print(" F:"); Serial.print(sensor[1].dist);
  Serial.print(" R:"); Serial.println(sensor[2].dist);
}

// -------- TURN BY TICKS (PID) -------- //
void turnTicksPID(long targetTicks) {
  if (targetTicks == 0) return;

  double integral_turn = 0, lastError_turn = 0;
  double integral_sync = 0, lastError_sync = 0;
  
  noInterrupts();
  encoderCountA = 0; // Right
  encoderCountB = 0; // Left
  interrupts();

  while (true) {
    long currentA = encoderCountA; // Right
    long currentB = encoderCountB; // Left
    
    long avgEncoderProgress = (abs(currentA) + abs(currentB)) / 2;
    double turnError = abs(targetTicks) - avgEncoderProgress;

    integral_turn += turnError;
    double derivative_turn = turnError - lastError_turn;
    double baseSpeed = (Kp_turn * turnError) + (Ki_turn * integral_turn) + (Kd_turn * derivative_turn);
    lastError_turn = turnError;

    double syncError = currentA + currentB;
    integral_sync += syncError;
    double derivative_sync = syncError - lastError_sync;
    double correction = (Kp_sync * syncError) + (Ki_sync * integral_sync) + (Kd_sync * derivative_sync);
    lastError_sync = syncError;

    int pwmRight = clampInt(baseSpeed - correction, 0, 255);
    int pwmLeft  = clampInt(baseSpeed + correction, 0, 255);

    if (abs(turnError) < 10) { stopMotors(); break; }

    if (targetTicks > 0) { turnLeft(pwmRight, pwmLeft); }  // + => left turn
    else                 { turnRight(pwmRight, pwmLeft); } // - => right turn
    
    delay(10);
  }
}

// -------- WRAPPERS -------- //
void turn90Right() {
  Serial.println("--- Turning 90 Right ---");
  turnTicksPID(TICKS_FOR_90_DEG_TURN_RIGHT);
  orient = (orient + 1) & 3;
  Serial.println("Done.");
}
void turnAround() {
  Serial.println("--- Turning Around ---");
  turnTicksPID(TICKS_FOR_180_DEG_TURN);
  orient = (orient + 2) & 3;
  Serial.println("Done.");
}
void turn90Left() {
  Serial.println("--- Turning 90 Left ---");
  turnTicksPID(TICKS_FOR_90_DEG_TURN_LEFT);
  orient = (orient + 3) & 3;
  Serial.println("Done.");
}

// ================== NEW: move exactly one cell with alignment ==================
void moveOneCellAlign() {
  // Reset encoders
  noInterrupts();
  encoderCountA = 0; // Right
  encoderCountB = 0; // Left
  interrupts();

  long prevA = 0, prevB = 0;
  float prevWallErr = 0;

  while (true) {
    // 1) Sensor reads
    int dL = readUltrasonic(sensor[0].echopin, sensor[0].trigPin);
    delay(5);
    int dF = readUltrasonic(sensor[1].echopin, sensor[1].trigPin);
    delay(5);
    int dR = readUltrasonic(sensor[2].echopin, sensor[2].trigPin);

    // 2) Encoder progress
    long A = encoderCountA; // Right
    long B = encoderCountB; // Left
    long avg = (abs(A) + abs(B)) / 2;

    // Early protection if a wall appears very close ahead
    if (dF <= WALL_DETECT_CM && dF > 1) {
      stopMotors();
      break;
    }

    // Stop condition: reached next cell
    if (avg >= TICKS_PER_CELL) {
      stopMotors();
      break;
    }

    // 3) Wall-centering error
    // Prefer using both walls if valid; else single wall; else 0 (encoder sync only)
    float err = 0.0;
    bool vl = validSide(dL);
    bool vr = validSide(dR);

    if (vl && vr) {
      // Center between walls: want dL ~= dR
      err = (float)dR - (float)dL; // + => too close to left (dR>dL), steer right
    } else if (vr) {
      // Right-wall follow: want dR ~= SIDE_TARGET_CM
      err = (float)(SIDE_TARGET_CM - dR); // + => too close to wall (dR small)
    } else if (vl) {
      // Left-wall follow: want dL ~= SIDE_TARGET_CM
      err = (float)(dL - SIDE_TARGET_CM); // + => too far from wall
    } else {
      err = 0.0; // no wall info, rely on sync only
    }

    float derr = err - prevWallErr;
    prevWallErr = err;

    // 4) Encoder sync (keep wheel speeds matched)
    long dA = A - prevA;
    long dB = B - prevB;
    prevA = A; prevB = B;
    float syncErr = (float)dA - (float)dB; // + => right faster than left

    // 5) Compute PWMs
    float wallCorr = FW_KP * err + FW_KD * derr;
    float syncCorr = SYNC_KP * syncErr;

    // Apply opposite corrections to each side
    int pwmRight = (int)(BasePWM - wallCorr - syncCorr);
    int pwmLeft  = (int)(BasePWM + wallCorr + syncCorr);

    pwmRight = clampInt(pwmRight, MIN_PWM, 255);
    pwmLeft  = clampInt(pwmLeft,  MIN_PWM, 255);

    moveForward(pwmRight, pwmLeft);
    delay(SampleTime);
  }

  // Hard stop at cell center
  stopMotors();
}

// ================== SETUP ==================
void setup() {
  Serial.begin(115200);
  delay(1000);

  // Motor A (Right)
  pinMode(IN1, OUTPUT); pinMode(IN2, OUTPUT); pinMode(EN1, OUTPUT);
  // Motor B (Left)
  pinMode(IN3, OUTPUT); pinMode(IN4, OUTPUT); pinMode(EN2, OUTPUT);

  // Encoders
  pinMode(encoder_A_A, INPUT_PULLUP);
  pinMode(encoder_A_B, INPUT_PULLUP);
  pinMode(encoder_B_A, INPUT_PULLUP);
  pinMode(encoder_B_B, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(encoder_A_A), encoderISR_A, CHANGE); // Right
  attachInterrupt(digitalPinToInterrupt(encoder_B_A), encoderISR_B, CHANGE); // Left

  // Sensor Pins
  for (int i = 0; i < 3; i++){
    pinMode(sensor[i].trigPin, OUTPUT);
    pinMode(sensor[i].echopin, INPUT);
  }

  Serial.println("Setup Complete. Starting Loop.");
  stopMotors();
}

// ================== MAIN LOOP ==================
// Cell-by-cell: decide (R/F/L/B) -> turn if needed -> move one cell w/ alignment -> stop, read, wait
void loop() {
  // 1) Read sensors at cell center
  readAllSensors();

  // 2) Decide by Right-Hand Rule (use your thresholds)
  bool openRight = (sensor[2].dist > WALL_SIDE_OPEN_CM && sensor[2].dist < 100);
  bool openFront = (sensor[1].dist > WALL_DETECT_CM);
  bool openLeft  = (sensor[0].dist > WALL_SIDE_OPEN_CM && sensor[0].dist < 100);

  char action = 'B';
  if (openRight) action = 'R';
  else if (openFront) action = 'F';
  else if (openLeft) action = 'L';
  else action = 'B';

  Serial.print("Decision -> ");
  Serial.println(action);

  // 3) Execute turn if needed
  if (action == 'R') {
    turn90Right();
  } else if (action == 'L') {
    turn90Left();
  } else if (action == 'B') {
    turnAround();
  } // 'F' -> no turn

  // Reset matcher memory after turning
  noInterrupts();
  prevCountA = encoderCountA;
  prevCountB = encoderCountB;
  interrupts();
  integralError = 0;

  // 4) Move one cell while aligning continuously
  moveOneCellAlign();

  // 5) Stop, read sensors, and wait 0.5 s at cell center
  stopMotors();
  readAllSensors();
  delay(CELL_SETTLE_MS);
}
