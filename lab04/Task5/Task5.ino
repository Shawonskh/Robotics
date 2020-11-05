#include <Wire.h>
#include <LPS.h>
#include <L3G.h>
#include <LSM303.h>

L3G gyro;
LPS ps;
LSM303 compass;
char report[80];

void setup() {
Serial.begin(9600);
  Wire.begin();

  if (!ps.init())
  {
    Serial.println("Failed to autodetect pressure sensor!");
    while (1);
  }

  ps.enableDefault();

 if (!gyro.init())
  {
    Serial.println("Failed to autodetect gyro type!");
    while (1);
  }

  gyro.enableDefault();

  Serial.begin(9600);
  Wire.begin();
  compass.init();
  compass.enableDefault();
}

void loop() {
  //thermometer
  //temp,air pressure and height
  float pressure = ps.readPressureMillibars();
  float altitude = ps.pressureToAltitudeMeters(pressure);
  float temperature = ps.readTemperatureC();
  
  Serial.print("Air pressure: ");
  Serial.print(pressure);
  Serial.print("mbar  Altitude: ");
  Serial.print(altitude);
  Serial.print("m  Temperature: ");
  Serial.print(temperature);
  Serial.println("°C");
  
  //Gyroscope
  gyro.read();

  Serial.print("Gyroscope: ");
  Serial.print("X: ");
  Serial.print((((int)gyro.g.x)*8.75)/1000);
  Serial.print("dps");
  Serial.print(" Y: ");
  Serial.print((((int)gyro.g.y)*8.75)/1000);
  Serial.print("dps");
  Serial.print(" Z: ");
  Serial.print((((int)gyro.g.z)*8.75)/1000);
  Serial.println(" dps");
 
 //accelerometer and a compass
  compass.read();

  Serial.print("accelerometer: ");
  Serial.print("X: ");
  Serial.print((((int)compass.a.x)*0.061));
  Serial.print("m/s²");
  Serial.print(" Y: ");
  Serial.print((((int)compass.a.y)*0.061));
  Serial.print("m/s²");
  Serial.print(" Z: ");
  Serial.print((((int)compass.a.z)*0.061));
  Serial.println(" m/s²");
 
  compass.read();

  Serial.print("magnetometer: ");
  Serial.print("X: ");
  Serial.print((((int)compass.m.x)*0.080));
  Serial.print("mgauss");
  Serial.print(" Y: ");
  Serial.print((((int)compass.m.y)*0.080));
  Serial.print("mgauss");
  Serial.print(" Z: ");
  Serial.print((((int)compass.m.z)*0.080));
  Serial.println(" mgauss");

  delay(500);
}
