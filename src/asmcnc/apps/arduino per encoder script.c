// Rotary Encoder Inputs
//  interrupt pins available: 2, 3, 18, 19, 20, 21

// Pulse encoder pins
#define CLK 2 // pin 2

// Left pulses
int counter = 0;
int currentStateCLK;
int lastStateCLK;

// buffer to feed info to serial
char output_buffer[50];
char last_output_buffer[50];

// Set up the arduino
void setup() {
  
  // Set left encoder pins as inputs
  pinMode(CLK,INPUT);

  // Setup Serial Monitor
  Serial.begin(115200);

  // Read the initial state of CLK
  lastStateCLK = digitalRead(CLK);

  // Call updateEncoder() when any high/low changed seen
  attachInterrupt(digitalPinToInterrupt(2), updateEncoder, CHANGE);

}

void loop() {

  // write all the counters to a buffer every ~50 ms  
  sprintf(output_buffer, "L:%d", counter);

  // send them to the serial only if there's a change
  if (last_output_buffer != output_buffer) {
    Serial.println(output_buffer);
    strcpy(last_output_buffer, output_buffer);
  }
  delay(50);
}

void updateEncoder() {
  // Read the current state of CLK
  currentStateCLK = digitalRead(CLK);

  // If last and current state of CLK are different, then pulse occurred
  // React to only 1 state change to avoid double count
  if (currentStateCLK != lastStateCLK  && currentStateCLK == 1) {

    counter ++;

  }

  // Remember last CLK state
  lastStateCLK = currentStateCLK;

}