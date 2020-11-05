// Ultrasonic sensor
int echoPin = A4;
int trigPin = A5;

// Line sensor
int ls1 = 2;
int ls2 = 3;
int ls3 = 4;
int ls4 = 5;
int ls5 = 6;
int clp = 7;
int near = 8;

void setup() {
  Serial.begin(9600);
  pinMode(echoPin,INPUT);
  pinMode(trigPin,OUTPUT);
}

long getUS1(){
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  long duration = pulseIn(echoPin, HIGH, 12500);
  return (duration/2) / 2.91; // get distance in mm
}

void printJSON(int us1){ //Print all the sensor data to serial as JSON
  Serial.print("{\"us1\":");
  Serial.print(us1);
  Serial.print(", \"ls1\":");
  Serial.print(digitalRead(ls1));
  Serial.print(", \"ls2\":");
  Serial.print(digitalRead(ls2));
  Serial.print(", \"ls3\":");
  Serial.print(digitalRead(ls3));
  Serial.print(", \"ls4\":");
  Serial.print(digitalRead(ls4));
  Serial.print(", \"ls5\":");
  Serial.print(digitalRead(ls5));
  Serial.print(", \"CLP\":");
  Serial.print(digitalRead(clp));
  Serial.print(", \"near\":");
  Serial.print(digitalRead(near));
  Serial.println("}");
}

void loop() {

  while(!Serial.available()); //Wait until it is signaled that new data is needed
  while(Serial.available()) Serial.read(); //Read everything from serial

  int us1 = getUS1(); //Get distance from wall with ultrasonic sensor

  printJSON(us1);   //Print data to serial.
}
