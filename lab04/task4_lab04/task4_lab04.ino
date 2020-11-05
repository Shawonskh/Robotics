#include <Servo.h>

Servo myservo;

int pos = 0;

void setup() {
  myservo.attach(7);
  Serial.begin(9600);
  Serial.println("Enter between 1300 and  1700 ");
}

void loop() {
  if (Serial.available()) {
    int incomingByte = Serial.parseInt();
    
    myservo.writeMicroseconds(incomingByte);
    
  }
}
