/* Sweep
 by BARRAGAN <http://barraganstudio.com>
 This example code is in the public domain.

 modified 8 Nov 2013
 by Scott Fitzgerald
 http://www.arduino.cc/en/Tutorial/Sweep
*/

#include <Servo.h> 
 
Servo myservo;  // create servo object to control a servo 
                // a maximum of eight servo objects can be created 
int measurment = 0;
int echoPin = 3;
int trigPin = 2;
int delay_us = 60;
float distance_mm = 0;
long duration_us;
int pos = 0;  // variable to store the servo position

void setup()  {
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
}

void loop(){
   // Read the pulse HIGH state on echo pin
  // the length of the pulse in microseconds 
  digitalWrite(trigPin, LOW);
  delayMicroseconds(delay_us);
  digitalWrite(trigPin, HIGH);
  duration_us = pulseIn(echoPin, HIGH);
  distance_mm = duration_us/58.2 * 10;
  
  if (distance_mm > 300) {
    if (measurment == 0) {
      pos += 2; // in steps of 1 degree
      if (pos == 180) {
        measurment += 1;
      }
    }  
    if (measurment == 1) {
      pos -= 2;
      if (pos == 0) {
        measurment -= 1;
      }
    }  
    myservo.write(pos);   // tell servo to go to position in variable 'pos'
  }
  else {
    Serial.println(distance_mm);
  }
  delay(20);
  
}
