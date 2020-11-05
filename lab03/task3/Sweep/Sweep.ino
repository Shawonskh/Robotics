// Sweep
// by BARRAGAN <http://barraganstudio.com> 
// This example code is in the public domain.


#include <Servo.h> 
 
Servo myservo;  // create servo object to control a servo 
                // a maximum of eight servo objects can be created 
 
int pos = 0;    // variable to store the servo position 
int echoPin = 2;
int trigPin = 3;

void setup() 
{ 
  myservo.attach(11);  // attaches the servo on pin 9 to the servo object
  Serial.begin(9600);
  pinMode(echoPin, INPUT);
  pinMode(trigPin, OUTPUT);
} 
 
 
void loop() 
{ 
  for(pos = 0; pos < 45; pos += 45)  // goes from 0 degrees to 180 degrees 
  {                                  // in steps of 1 degree 
    myservo.write(pos);              // tell servo to go to position in variable 'pos' 
    delay(1000);                     // waits 15ms for the servo to reach the position 
  } 
  for(pos = 45; pos < 95; pos += 50)  // goes from 0 degrees to 180 degrees 
  {                                  // in steps of 1 degree 
    myservo.write(pos);              // tell servo to go to position in variable 'pos' 
    delay(1000);                     // waits 15ms for the servo to reach the position 
  } 
  for(pos = 95; pos < 155; pos += 60)  // goes from 0 degrees to 180 degrees 
  {                                  // in steps of 1 degree 
    myservo.write(pos);              // tell servo to go to position in variable 'pos' 
    delay(1000);                     // waits 15ms for the servo to reach the position 
  } 
  for(pos = 155; pos < 180; pos += 35)  // goes from 0 degrees to 180 degrees 
  {                                  // in steps of 1 degree 
    myservo.write(pos);              // tell servo to go to position in variable 'pos' 
    delay(1000);                     // waits 15ms for the servo to reach the position 
  } 
  for(pos = 180; pos>=1; pos-=5)     // goes from 180 degrees to 0 degrees 
  {                                
    myservo.write(pos);              // tell servo to go to position in variable 'pos' 
    delay(50);
 
  } 
} 
