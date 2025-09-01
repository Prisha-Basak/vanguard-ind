// Transmitter (Arduino + nRF24)

// include the libraries needed for the nRF24L01 module
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

// Create a radio object
// CE pin is connected to Arduino pin 7
// CSN pin is connected to Arduino pin 8
RF24 radio(7, 8);

// Address for communication (like a channel name)
// Must be the same on both transmitter and receiver
byte address[6] = "00001";

void setup() {
  // Start the radio
  radio.begin();

  // Choose the address (same must be on the receiver)
  radio.openWritingPipe(address);

  // Set the power level (low so it works on breadboard without too much noise)
  radio.setPALevel(RF24_PA_MIN);

  // Tell the radio we are only SENDING (not listening)
  radio.stopListening();
}

void loop() {
  // Message we want to send
  char message[] = "Hello World";

  // Send the message
  radio.write(&message, sizeof(message));

  // Wait 1 second before sending again
  delay(1000);
}

// Receiver (Arduino + nRf24)

// include the libraries needed for the nRF24L01 module
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

// Create a radio object
// CE pin is connected to Arduino pin 7
// CSN pin is connected to Arduino pin 8
RF24 radio(7, 8);

// Address for communication (must match the transmitter)
byte address[6] = "00001";

void setup() {
  // Start serial monitor (to see messages on the computer)
  Serial.begin(9600);

  // Start the radio
  radio.begin();

  // Open a "reading pipe" using the same address as transmitter
  radio.openReadingPipe(0, address);

  // Set power level (low so it works fine on breadboard)
  radio.setPALevel(RF24_PA_MIN);

  // Tell the radio we are only LISTENING (not sending)
  radio.startListening();
}

void loop() {
  // Check if any message came in
  if (radio.available()) {
    char message[32] = "";   // storage space for incoming message

    // Read the message into 'message'
    radio.read(&message, sizeof(message));

    // Print the received message on the serial monitor
    Serial.println(message);
  }
}
