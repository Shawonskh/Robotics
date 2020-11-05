int echoPin = 2;
int trigPin = 3;
int delay_us = 50; // <--- YOU HAVE TO FIND THE CORRECT VALUE FROM THE DATASHEET
long distance_mm = 0;
long duration_us = 10; // pulsi tagasi saamise aeg

#include <Servo.h>
Servo myservo;  // create servo object to control a servo
                // a maximum of eight servo objects can be created

int pos = 0;    // variable to store the servo position

void setup() {
  // put your setup code here, to run once:
  myservo.attach(11);  // attaches the servo on pin 9 to the servo object
  Serial.begin(9600);
  pinMode(echoPin, INPUT);
  pinMode(trigPin, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(delay_us);
  digitalWrite(trigPin, LOW);
  duration_us = pulseIn(echoPin, HIGH);
  distance_mm = ((duration_us / 2) / 29.1) * 10; // 2= edasi-tagasi 29.1=helikiirus

    for (pos = 0; pos < 180; pos += 5) // goes from 0 degrees to 180 degrees
    { // in steps of 1 degree
      myservo.write(pos);              // tell servo to go to position in variable 'pos'
      delay(50);  // waits 15ms for the servo to reach the position
      digitalWrite(trigPin, HIGH);
      delayMicroseconds(delay_us);
      digitalWrite(trigPin, LOW);
      duration_us = pulseIn(echoPin, HIGH);
      distance_mm = ((duration_us / 2) / 29.1) * 10;
      if (distance_mm < 300)
       {
        Serial.print("STOP");
        Serial.println(distance_mm, DEC);
        pos-=5;
       }
      else if (distance_mm >= 300)
       {
         myservo.write(pos);              // tell servo to go to position in variable 'pos'
         delay(50);
       }
    }
    
    for (pos = 180; pos >= 1; pos -= 5) // goes from 180 degrees to 0 degrees
    {
      myservo.write(pos);              // tell servo to go to position in variable 'pos'
      delay(50);

      digitalWrite(trigPin, HIGH);
      delayMicroseconds(delay_us);
      digitalWrite(trigPin, LOW);
      duration_us = pulseIn(echoPin, HIGH);
      distance_mm = ((duration_us / 2) / 29.1) * 10;
      
      if (distance_mm < 300)
      {
        Serial.print("STOP");
        Serial.println(distance_mm, DEC);
        pos+=5;
      }
     
      else if (distance_mm >= 300)
      {
        myservo.write(pos);              // tell servo to go to position in variable 'pos'
        delay(50);
      }

    }
  delay(100);
}
