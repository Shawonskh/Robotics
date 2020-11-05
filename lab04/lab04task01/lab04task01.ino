const int pirPin = 5;         // passive infrared sensor pin
int state = 0;                // 0 - no motion, 1 - motion detected

void setup(){
  Serial.begin(9600);         // initialize serial with 9600 baud rate
  pinMode(pirPin, INPUT);     // set pin #5 as an input from PIR
}

void loop(){
  if(digitalRead(pirPin) == HIGH  &&  state == 0){
    Serial.println("Motion detected!");
    state = 1;
  }
  if(digitalRead(pirPin) == LOW  &&  state == 1){
    Serial.println("No movement anymore");
    state = 0;
  }
}
