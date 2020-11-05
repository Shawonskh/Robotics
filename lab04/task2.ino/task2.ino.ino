int Pin = A0;
int Value = 0;
long previousMillis = 0;  // will store last time LED was updated
const long interval = 500;  // interval at which to blink (milliseconds)
int ledPin = 9;  // LED connected to digital pin 9


void setup() {
  Serial.begin(9600);
}

void loop() {
    // check to see if it's time to blink the LED; that is, if the difference
  // between the current time and last time you blinked the LED is bigger than
  // the interval at which you want to blink the LED.
  long currentMillis = millis();

  Value = analog(Pin);

  if(currentMillis - previousMillis >= interval) { 
    // save the last time you blinked the LED
    previousMillis = currentMillis;
    if(Value < 10){
      Serial.print("No light " );
    } else if(Value >= 10 && Value < 700){
      Serial.print("Classroom lights ");
    } else {
      Serial.print("Bright light ");
    }

    Serial.println(Value);
  }
  int fadeValue = map(Value, 0, 1023, 0, 255); //map an analog value to 8 bits (0 to 255)
  // sets the value (range from 0 to 255):
  analogWrite(ledPin, 255-fadeValue); 
}
