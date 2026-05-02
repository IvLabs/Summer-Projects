#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
#include <EEPROM.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

#define SERVOMIN 184
#define SERVOMAX 512

// Channels for the 3 joints of this leg
int channels[4][3] = {{2, 0, 6}, {3, 1, 5}, {12,15, 9}, {13, 14, 8}}; // Hip, Knee, Ankle, rf,lf,lb,rb

// Offsets to be stored in EEPROM
int offsets[4][3] = {{0, 150, 50}, {0, 150, 10}, {0, 150, 0}, {0, -150, 40}}; 

void writeAngle(int channel, int angle) {
  angle = constrain(angle, -180, 180);
  uint16_t pulse = map(angle, -180, 180, SERVOMIN, SERVOMAX);
  pwm.setPWM(channel, 0, pulse);
}

void loadOffsets() {
  int addr = 0;
  for(int i = 0; i < 4; i++){
    for (int j = 0; j < 3; j++) {
      EEPROM.get(addr, offsets[i][j]);
      addr += sizeof(int);
    }
  }
}

void setup() {
  Serial.begin(115200);

  Wire.begin();            // Arduino
  // Wire.begin(21,22);    // If ESP32

  pwm.begin();
  pwm.setPWMFreq(50);
  delay(200);

  // ✅ Load stored offsets (must have been saved at least once)
  loadOffsets();

  // ✅ Move leg to default offset pose
  for(int i = 0; i < 4; i++){
    for(int j = 0; j < 3; j++){
      writeAngle(channels[i][j], offsets[i][j]);
    }
  }
  delay(5);
}

float angles[100][2] = {
   {-1.3972  ,  0.5312},
   {-1.5566  ,  0.5687},
   {-1.7156  ,  0.6053},
   {-1.8742  ,  0.6410},
   {-2.0325  ,  0.6757},
   {-2.1903  ,  0.7096},
   {-2.3478  ,  0.7425},
   {-2.5048  ,  0.7745},
   {-2.6615  ,  0.8056},
   {-2.8177  ,  0.8357},
   {-2.9735  ,  0.8650},
   {-3.1290  ,  0.8933},
   {-3.2840  ,  0.9207},
   {-3.4386  ,  0.9472},
   {-3.5928  ,  0.9727},
   {-3.7466  ,  0.9974},
   {-3.9000  ,  1.0211},
   {-4.0530  ,  1.0439},
   {-4.2055  ,  1.0658},
   {-4.3577  ,  1.0868},
   {-4.5094  ,  1.1069},
   {-4.6607  ,  1.1260},
   {-4.8115  ,  1.1442},
   {-4.9620  ,  1.1616},
   {-5.1120  ,  1.1780},
   {-3.4345  ,  1.3969},
   {-3.6539  ,  1.8808},
   {-3.8638  ,  2.3573},
   {-4.0633  ,  2.8245},
   {-4.2515  ,  3.2806},
   {-4.4277  ,  3.7241},
   {-4.5910  ,  4.1532},
   {-4.7407  ,  4.5666},
   {-4.8760  ,  4.9626},
   {-4.9964  ,  5.3398},
   {-5.1011  ,  5.6970},
   {-5.1895  ,  6.0329},
   {-5.2611  ,  6.3462},
   {-5.3154  ,  6.6358},
   {-5.3519  ,  6.9007},
   {-5.3702  ,  7.1399},
   {-5.3699  ,  7.3526},
   {-5.3507  ,  7.5378},
   {-5.3122  ,  7.6950},
   {-5.2544  ,  7.8233},
   {-5.1768  ,  7.9223},
   {-5.0795  ,  7.9915},
   {-4.9623  ,  8.0305},
   {-4.8252  ,  8.0389},
   {-4.6680  ,  8.0164},
   {-4.4910  ,  7.9631},
   {-4.2940  ,  7.8787},
   {-4.0773  ,  7.7633},
   {-3.8410  ,  7.6169},
   {-3.5853  ,  7.4398},
   {-3.3104  ,  7.2322},
   {-3.0166  ,  6.9944},
   {-2.7041  ,  6.7268},
   {-2.3734  ,  6.4300},
   {-2.0247  ,  6.1044},
   {-1.6585  ,  5.7508},
   {-1.2752  ,  5.3698},
   {-0.8752  ,  4.9623},
   {-0.4591  ,  4.5290},
   {-0.0273  ,  4.0709},
   { 0.4197  ,  3.5891},
   { 0.8812  ,  3.0845},
   { 1.3568  ,  2.5584},
   { 1.8458  ,  2.0118},
   { 2.3475  ,  1.4461},
   { 2.8615  ,  0.8625},
   { 3.3870  ,  0.2624},
   { 3.9233  , -0.3528},
   { 4.4699  , -0.9817},
   { 5.0260  , -1.6227},
   { 4.8489  , -1.5476},
   { 4.6653  , -1.4706},
   { 4.4751  , -1.3919},
   { 4.2785  , -1.3115},
   { 4.0755  , -1.2296},
   { 3.8661  , -1.1462},
   { 3.6504  , -1.0617},
   { 3.4284  , -0.9760},
   { 3.2002  , -0.8894},
   { 2.9659  , -0.8020},
   { 2.7256  , -0.7139},
   { 2.4792  , -0.6253},
   { 2.2268  , -0.5363},
   { 1.9686  , -0.4472},
   { 1.7046  , -0.3581},
   { 1.4349  , -0.2692},
   { 1.1595  , -0.1806},
   { 0.8785  , -0.0926},
   { 0.5920  , -0.0052},
   { 0.3001  ,  0.0812},
   { 0.0029  ,  0.1665},
   {-0.2996  ,  0.2505},
   {-0.6071  ,  0.3330},
   {-0.9198  ,  0.4138},
   {-1.2373  ,  0.4927},
};

void loop(){

  for (int i=0 ; i<25 ; i++)

    {
      writeAngle(6, 40);
      writeAngle(8, 30);
      writeAngle(5, 0);
      writeAngle(9, 0);
      delay(10);
      //
      float hip_1 = (-2*(angles[i][0] )+0);
      writeAngle(channels[0][0], hip_1);

      float knee_1 = (((angles[i][1])*(2))-150);
      writeAngle(channels[0][1], knee_1);

      delay(10);

      float hip_2 = (2*(angles[i][0] )+30);
      writeAngle(channels[1][0], hip_2);
    
      float knee_2 = (((angles[i][1])*(-2))+150);
      writeAngle(channels[1][1], knee_2);

      delay(10);

      float hip_3 = (((angles[i][0] )*(-2))+90);
      writeAngle(channels[2][0], hip_3);
    
      float knee_3 = (((angles[i][1])*(2))-150);
      writeAngle(channels[2][1], knee_3);

      delay(10);

      float hip_4 = (2*(angles[i][0] )-20);
      writeAngle(channels[3][0], hip_4);
    
      float knee_4 = (((angles[i][1])*(2))-150);
      writeAngle(channels[3][1], knee_4);
      delay(10);
    }
    
    for (int i = 25; i < 75; i++) {
    float hip_1 = (-2*(angles[i][0] )+0);
      writeAngle(channels[0][0], hip_1);

      float knee_1 = (((angles[i][1])*(2))-150);
      writeAngle(channels[0][1], knee_1);

    writeAngle(channels[0][2], offsets[0][2]);
    writeAngle(6, 40);
    writeAngle(8, 30);
    writeAngle(5, 0);
    writeAngle(9, 0);
    delay(10);
  }

  for (int i = 25; i < 75; i++) {
    float hip_2 = (2*(angles[i][0] )+30);
      writeAngle(channels[1][0], hip_2);
    
      float knee_2 = (((angles[i][1])*(-2))+150);
      writeAngle(channels[1][1], knee_2);
    writeAngle(channels[1][2], offsets[1][2]);
    writeAngle(6, 40);
    writeAngle(8, 30);
    writeAngle(5, 0);
    writeAngle(9, 0);

    delay(10);
  }

  for (int i = 25; i < 75; i++) {
    float hip_3 = (((angles[i][0] )*(-2))+90);
      writeAngle(channels[2][0], hip_3);
    
      float knee_3 = (((angles[i][1])*(2))-150);
      writeAngle(channels[2][1], knee_3);

    writeAngle(channels[2][2], offsets[2][2]);
    writeAngle(6, 40);
    writeAngle(8, 30);
    writeAngle(5, 0);
    writeAngle(9, 0);

    delay(10);
  }

  for (int i = 25; i < 75; i++) {
    float hip_4 = (2*(angles[i][0] )-20);
      writeAngle(channels[3][0], hip_4);
    
      float knee_4 = (((angles[i][1])*(2))-150);
      writeAngle(channels[3][1], knee_4);

    writeAngle(channels[3][2], offsets[3][2]);
    writeAngle(6, 40);
    writeAngle(8, 30);
    writeAngle(5, 0);
    writeAngle(9, 0);

    delay(10);
  }
  for (int i=75 ; i<100 ; i++)

    {
      writeAngle(6, 40);
      writeAngle(8, 30);
      writeAngle(5, 0);
      writeAngle(9, 0);
      delay(10);
      //lf
      float hip_1 = (-2*(angles[i][0] )+0);
      writeAngle(channels[0][0], hip_1);

      float knee_1 = (((angles[i][1])*(2))-150);
      writeAngle(channels[0][1], knee_1);

      delay(10);

      float hip_2 = (2*(angles[i][0] )+30);
      writeAngle(channels[1][0], hip_2);
    
      float knee_2 = (((angles[i][1])*(-2))+150);
      writeAngle(channels[1][1], knee_2);

      delay(10);

      float hip_3 = (((angles[i][0] )*(-2))+90);
      writeAngle(channels[2][0], hip_3);
    
      float knee_3 = (((angles[i][1])*(2))-150);
      writeAngle(channels[2][1], knee_3);

      delay(10);

      float hip_4 = (2*(angles[i][0] )-20);
      writeAngle(channels[3][0], hip_4);
    
      float knee_4 = (((angles[i][1])*(2))-150);
      writeAngle(channels[3][1], knee_4);
      delay(10);
    }
}