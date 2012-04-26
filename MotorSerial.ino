/*/////////////////////////////////////////////////////////////////
/
/                   Serial-controlled DC motor 
/ 
/          Designed to control a DC via a pySerial interface 
/
/     Author          :   Marc-Olivier Schwartz
/     E-Mail          :   marcolivier.schwartz@gmal.com
/
/////////////////////////////////////////////////////////////////*/


// Variables declaration

// Input
char input;

// Motor state and speed
int motor_state;
int motor_speed;

// Measurements
float motor_speed_meas;
int motor_speed_mean;

// Setup of the board
void setup() {                
  // Initialize pins
  pinMode(3, OUTPUT); 
  pinMode(9, OUTPUT);
  pinMode(7, INPUT);

  // Initialize serial port
  Serial.begin(9600);
  Serial.flush();
  
  // Initialize motor state and speed
  motor_state = 0;
  motor_speed = 50;
  
  // Set motor direction
  digitalWrite(9, HIGH); 
}

// Main loop
void loop() {
  
  // Command the motor depending on the state
  if (motor_state == 0)
  {
    analogWrite(3, 0);
  }
  
   if (motor_state == 1)
  {
    analogWrite(3, motor_speed);
  }
  
  // Reading serial input and decide what to do
  input = Serial.read();

  // If no imput, do nothing
  if (input == '-1') {}

  // If there is an input, do something
  else
  {

    // Use the 'p' command to increase the motor speed
    if (input == 'p') 
    { 
      motor_speed = motor_speed + 5;
     if (motor_speed > 255)
       {
         motor_speed = 255; 
       }
    }
    
    // Use the 'm' command to decrease motor speed
    if (input == 'm') 
    { 
      motor_speed = motor_speed - 5;
     if (motor_speed < 0)
       {
         motor_speed = 0; 
       } 
    }
    
    // Use the 's' command to start the motor with the current speed 
    if (input == 's') 
    { 
      motor_state = 1; 
    }
    
    // Use the '0' command to stop te motor
    if (input == '0') 
    { 
      motor_state = 0; 
    }
    
    // Use the 'g' command to measure the motor speed
    if (input == 'g') 
    {
      // Init measurement values
      motor_speed_meas = 0;
      motor_speed_mean = 0;
     
      // Take 10 measurements and average 
      for (int i=0;i<10;i++) 
      {
        motor_speed_meas = motor_speed_meas + 500000/(float)pulseIn(7, HIGH);
      }
      
      motor_speed_mean = (int)(motor_speed_meas/10);
      
      // Write on the serial
      Serial.write(motor_speed_mean / 256);
      Serial.write(motor_speed_mean % 256);
    }
  
  }  
 
}

