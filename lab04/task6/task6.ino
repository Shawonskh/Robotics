#include <Wire.h>
#include <LSM303.h>
#include <Servo.h>

LSM303 compass;
Servo myservo;

char report[80];

void setup() {
  Serial.begin(9600);
  Wire.begin();
  compass.init();

  compass.enableDefault();
  myservo.attach(7);
}

void loop() {
  compass.read();

  //Serial.println("Accelometere (in mg) and magnetometer (in mgauss)");
  Serial.print("accelerometer: ");
  Serial.print("X: ");
  Serial.print((((int)compass.a.x)*0.061));
  Serial.print("mg");
  Serial.print(" Y: ");
  Serial.print((((int)compass.a.y)*0.061));
  Serial.print("mg");
  Serial.print(" Z: ");
  Serial.print((((int)compass.a.z)*0.061));
  Serial.println(" mg");
 
  compass.read();

  Serial.print("magnetometer: ");
  Serial.print("X: ");
  Serial.print((((int)compass.m.x)*0.160));
  Serial.print("mgauss");
  Serial.print(" Y: ");
  Serial.print((((int)compass.m.y)*0.160));
  Serial.print("mgauss");
  Serial.print(" Z: ");
  Serial.print((((int)compass.m.z)*0.160));
  Serial.println(" mgauss");
  int motorvalue = map(((compass.a.x)*0.160), -1100, 1460, 1400, 1600);
  myservo.writeMicroseconds(motorvalue);

  //delay(500);
}
