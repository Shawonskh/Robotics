
void setup()  {
  Serial.begin(9600);
  Serial.println("Hello!");
  Serial.println("Please enter a number and press ENTER.");

}
void loop() {
  if (Serial.available() > 0) 
  {
    long incomingByte = Serial.parseInt();
    if (incomingByte < 300)
    {
      Serial.print("STOP");
      Serial.println(incomingByte, DEC);
     }
    
    else if (incomingByte > 300)
    {
      Serial.print("GO");
      Serial.println(incomingByte, DEC);
    }
  }
  // YOUR CODE GOES HERE
}
