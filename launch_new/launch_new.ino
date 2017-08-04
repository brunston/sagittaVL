#include <Servo.h>

#define SERVOPIN_1 0
#define SERVOPIN_2 1
#define SERVOPIN_3 2

// Servo positions - calibrate
#define SERVO1_CLOSED 0
#define SERVO1_OPEN 180
#define SERVO2_CLOSED 0
#define SERVO2_OPEN 180
#define SERVO3_CLOSED 0
#define SERVO3_OPEN 180

#define LEDPIN 2

#define ALT_THRESH 750
#define LAUNCH_VERIFS 30
#define ARM_VERIFS 30

// States
#define PRELAUNCH 0
#define ASCENT 1
#define ARMED 2

int currentState;
int altitude;
int verifs;

Servo servo1, Servo servo2, Servo servo3

void setup() {
  // put your setup code here, to run once:
  servo1.attach(SERVOPIN_1);
  servo1.write(SERVO1_CLOSED);
  servo2.attach(SERVOPIN_2);
  servo2.write(SERVO2_CLOSED);
  servo3.attach(SERVOPIN_3);
  servo3.write(SERVO3_CLOSED);

  Serial.begin(9600);

  currentState = PRELAUNCH;
  verifs = 0;
}

void loop() {
  altitude = Serial.read();
  if (altitude == -1) {
    // no serial data found - buzzer
  } else {
    if (currentState == PRELAUNCH) {
      if (altitude > ALT_THRESH) {
        verifs++;
        if (verifs > LAUNCH_VERIFS) {
          currentState = ASCENT;
        }
      } else {
        verifs = 0;
      }
    } else if (currentState == ASCENT) {
      if (altitude < ALT_THRESH) {
        verifs++;
        if (verifs > ARM_VERIFS) {
          currentState = ARMED;
        }
      } else {
        verifs = 0;
      }
    }
  }
}
