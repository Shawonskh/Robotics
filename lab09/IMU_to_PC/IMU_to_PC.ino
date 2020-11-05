#include <Wire.h>
#include <LSM303.h>
#include <L3G.h>

#define LED 13

//You will need to find your own magnetometer calibration values, use the sample code that came with the LSM303 library!!!
//You will need to change these values both here and in the Python code!!

//TASK 1
#define MAG_X_MIN -2805
#define MAG_Y_MIN -2476
#define MAG_Z_MIN -2394
#define MAG_X_MAX +2941
#define MAG_Y_MAX +2550
#define MAG_Z_MAX +2726
//TASK 1 END


#define ROLL_LIMIT 90.0f
#define PITCH_LIMIT 180.0f
#define YAW_LIMIT 180.0f

char report[64];
char inByte;
unsigned long currentTime, lastTime, newTime;
unsigned long dT;
float roll, pitch, yaw;                   // Roll and pitch calculated from accelerometer, yaw from magnetometer
float gyroXangle, gyroYangle, gyroZangle; // Angle calculated with gyroscope
float gyroXrate, gyroYrate, gyroZrate;    // Gyroscope movement rate, in degrees per second
int gyroCalibrationX, gyroCalibrationY, gyroCalibrationZ; //The average of 50 measurements after init will be taken as the bias of gyro.
int i = 0;
unsigned long sum = 0;

LSM303 compass;
L3G gyro;

void setup() {
  pinMode(LED, OUTPUT);

  Serial.begin(250000);
  Wire.begin();
  Wire.setClock(400000L);

  compass.init();
  compass.enableDefault();
  // Set accelerometer data rate to 800Hz
  // 0b10010111 = 0x97
  compass.writeReg(0x20, 0x97);
  // Set magnetometer data rate to 100Hz
  // 0b01110100 = 0x74
  compass.writeReg(0x24, 0x74);
  // Calibrate magnetometer with given values
  compass.m_min = (LSM303::vector<int16_t>) {
    MAG_X_MIN, MAG_Y_MIN, MAG_Z_MIN
  };
  compass.m_max = (LSM303::vector<int16_t>) {
    MAG_X_MAX, MAG_Y_MAX, MAG_Z_MAX
  };

  if (!gyro.init())
  {
    Serial.println("Failed to autodetect gyro type!");
    while (1);
  }
  gyro.enableDefault();
  // Set gyro data rate to 800Hz
  // 0b11111111 = 0xFF
  gyro.writeReg(0x20, 0xFF);

  lastTime = micros();
  compass.read();


  //Gyro bias calculation
  uint8_t gyroCalibrationBuffer = 50;

  int gyroX[gyroCalibrationBuffer];
  int gyroY[gyroCalibrationBuffer];
  int gyroZ[gyroCalibrationBuffer];

  for (int j = 0; j < gyroCalibrationBuffer; j++) {
    gyro.read();
    gyroX[j] = gyro.g.x;
    gyroY[j] = gyro.g.y;
    gyroZ[j] = gyro.g.z;
  }

  gyroCalibrationX = average(gyroX, gyroCalibrationBuffer);
  gyroCalibrationY = average(gyroY, gyroCalibrationBuffer);
  gyroCalibrationZ = average(gyroZ, gyroCalibrationBuffer);

}

void loop() {
  currentTime = micros();
  
  compass.read();
  gyro.read();

  // dT is in seconds
  dT = (currentTime - lastTime);// / 1000000.0f;
  lastTime = currentTime;

  if (Serial.available()) respondToSerial();
}

//Calculates the average of an array
int average (int * data_array, int len)  // assuming array is int.
{
  long sum = 0L ;  // sum will be larger than an item, long for safety.
  for (int i = 0 ; i < len ; i++)
    sum += data_array [i] ;
  return  sum / len ;
}

void respondToSerial() {
  //  digitalWrite(LED, !digitalRead(LED));
  inByte = Serial.read();
  if (inByte == 'g') {
    snprintf(report, sizeof(report), "%d:%d:%d:%d:%d:%d:%d:%d:%d:%u",
             compass.a.x, compass.a.y, compass.a.z,
             compass.m.x, compass.m.y, compass.m.z,
             gyro.g.x - gyroCalibrationX, gyro.g.y - gyroCalibrationY, gyro.g.z - gyroCalibrationZ, dT);
    Serial.println(report);
  }
}
