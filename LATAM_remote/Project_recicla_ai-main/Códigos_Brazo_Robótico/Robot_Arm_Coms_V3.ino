#include <Braccio.h>
#include <Servo.h>

Servo base;
Servo shoulder;
Servo elbow;
Servo wrist_rot;
Servo wrist_ver;
Servo gripper;

int step_delay = 20;

// Order: Plastic, Organic, Cardboard, Trash, Metal, Glass

int X[6] = {118, 90, 65, 118, 176, 161};
int Y[6] = {18, 18, 71, 106, 66, 18};
int Z[6] = {93, 84, 12, 1, 12, 84};
int W[6] = {50, 58, 47, 14, 47, 58};

int ID = 0;

void setup() {
  //Initialization functions and set up the initial position for Braccio
  //All the servo motors will be positioned in the "safety" position:
  //Base (M1):90 degrees
  //Shoulder (M2): 45 degrees
  //Elbow (M3): 180 degrees
  //Wrist vertical (M4): 180 degrees
  //Wrist rotation (M5): 90 degrees
  //gripper (M6): 10 degrees
  
  Braccio.begin();
  Serial.begin(9600);
  
  Braccio.ServoMovement(step_delay, 118, 119, 1, 20, 90, 72);
  delay(1000);
}

void loop() {
  
   if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    
    if (data == "plastic"){
      ID = 0;
    } else if(data == "organic"){
      ID = 1;
    } else if((data == "cardboard") || (data == "paper")){
      ID = 2;
    } else if(data == "trash"){
      ID = 3;
    } else if(data == "metal"){
      ID = 4;
    } else if(data == "glass"){
      ID = 5;
    }
    DeploySequence();
  }
  
}

void DeploySequence(){
  StepTakeTrash();
  delay(1000);
  StepOriginPos();
  delay(1000);
  StepTrashBin();
  delay(1000);
  StepStandBy();
}

void StepTakeTrash(){
  Braccio.ServoMovement(step_delay, 28, 100, 1, 14, 91, 30);
  delay(500);
  Braccio.ServoMovement(step_delay, 28, 94, 0, 38, 90, 30);
  delay(500);
  Braccio.ServoMovement(step_delay, 28, 66, 0, 82, 90, 30);
  delay(500);
  Braccio.ServoMovement(step_delay, 28, 60, 12, 64, 89, 30);
  delay(500);
  Braccio.ServoMovement(step_delay, 28, 60, 12, 64, 89, 73);
}

void StepOriginPos(){
  Braccio.ServoMovement(step_delay, 28, 70, 1, 80, 90, 73);
  delay(500);
  Braccio.ServoMovement(step_delay, 28, 84, 1, 52, 90, 73);
  delay(500);
  Braccio.ServoMovement(step_delay, 28, 119, 1, 20, 90, 73);
}

void StepTrashBin(){
  Braccio.ServoMovement(step_delay, X[ID], 119, 1, 20, 90, 73);
  delay(500);
  Braccio.ServoMovement(step_delay, X[ID], Y[ID], Z[ID], W[ID], 91, 73);
  delay(500);
  Braccio.ServoMovement(step_delay, X[ID], Y[ID], Z[ID], W[ID], 91, 30);
}

void StepStandBy(){
  Braccio.ServoMovement(step_delay, X[ID], 100, 1, 14, 91, 30);
  delay(500);
  Braccio.ServoMovement(step_delay, 118, 100, 1, 14, 91, 30);
}