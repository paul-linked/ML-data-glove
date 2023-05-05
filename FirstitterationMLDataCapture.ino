// Replace with your button pin
#define buttonPin 15

void setup() {
  //pinMode(buttonPin, INPUT_PULLUP);
  Serial.begin(9600);
}

void loop() {
  int buttonState = digitalRead(buttonPin);

  // Invert the button state because it's pulled up
  // buttonState = !buttonState;

  // Send button state over Serial
  Serial.println(buttonState);

  // Add a small delay to avoid flooding the Serial connection
  delay(100);
}
