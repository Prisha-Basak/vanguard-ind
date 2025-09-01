// Prisha Basak f2025A8PS1075H //

// Pin Connections
const int motorenable = 9;   // Enable 1 of L293D
const int motorin1    = 4;   // Input 1 of L293D
const int motorin2    = 5;   // Input 2 of L293D
const int potpin      = A0;  // Potentiometer input
const int temppin     = A1;  // Temperature sensor input
const int ledpin      = 8;   // Warning LED
const int buttonpin   = 7;   // Pushbutton


// Threshold temperature
const float tempthreshold = 40.0;
bool ledOverride = false;
bool lastButtonState = HIGH;

void setup() {
  pinMode(motorenable, OUTPUT);
  pinMode(motorin1, OUTPUT);
  pinMode(motorin2, OUTPUT);
  pinMode(ledpin, OUTPUT);
  pinMode(buttonpin, INPUT_PULLUP);  // internal pull-up

  Serial.begin(9600);
}

void loop() {
  // Motor Speed Control ---
  int potvalue = analogRead(potpin);       
  int motorspeed = map(potvalue, 0, 1023, 0, 255);
  analogWrite(motorenable, motorspeed);    

  // Fixed direction (forward)
  digitalWrite(motorin1, HIGH);
  digitalWrite(motorin2, LOW);

  // Temperature Reading 
  int rawtemp = analogRead(temppin);
  float voltage = (rawtemp / 1023.0) * 5.0;   
  float temperature = voltage * 100;        

  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.println(" °C");

  // Button Check 
  bool buttonState = digitalRead(buttonpin);
  if (lastButtonState == HIGH && buttonState == LOW) {
    ledOverride = !ledOverride;  
    delay(50);  
  }
  lastButtonState = buttonState;

  // LED Warning 
  if (temperature > tempthreshold && !ledOverride) {
    // Blink LED
    digitalWrite(ledpin, HIGH);
    delay(300);
    digitalWrite(ledpin, LOW);
    delay(300);
  } else {
    digitalWrite(ledpin, LOW);
    delay(50);
  }
}
