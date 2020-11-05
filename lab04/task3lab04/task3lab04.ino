#include <Servo.h>

Servo myservo;

int pos = 0;

void setup() {
  myservo.attach(7); //the number of the pin that the servo is attached to
}

void loop() {
  myservo.writeMicroseconds(1500); // set servo to mid-point
  delay(3000);
  myservo.writeMicroseconds(1690);
  delay(2000);
  myservo.writeMicroseconds(1510);
  delay(2000);
  myservo.writeMicroseconds(1490);
  delay(2000);
  myservo.writeMicroseconds(1310);
  delay(2000);
}
