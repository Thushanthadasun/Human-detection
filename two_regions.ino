// Define LED pins
const int leftLED = 2;
const int rightLED = 3;

void setup() {
  // Initialize serial communication
  Serial.begin(9600);

  // Set LED pins as output
  pinMode(leftLED, OUTPUT);
  pinMode(rightLED, OUTPUT);
}

void loop() {
  // Check if data is available from the serial port
  if (Serial.available() > 0) {
    char command = Serial.read();

    // Turn on/off LEDs based on the received command
    switch (command) {
      case '1':
        digitalWrite(leftLED, HIGH);  // Turn on left LED
        break;
      case '2':
        digitalWrite(rightLED, HIGH); // Turn on right LED
        break;
      case '3':
        digitalWrite(leftLED, LOW);   // Turn off left LED
        break;
      case '4':
        digitalWrite(rightLED, LOW);  // Turn off right LED
        break;
    }
  }
}