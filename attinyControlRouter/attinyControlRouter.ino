#include <avr/io.h>

#define SET(reg, b) (reg |= _BV(b))
#define CLEAR(reg, b) (reg &= ~_BV(b))
#define IS_SET(reg, b) (reg & _BV(b))

#define RC_OVERRIDE_THRESHOLD 0.08

const int resolution = 20;
float counts[resolution];
int currentCounter = 0;
bool initiated = false;
unsigned long pulseStart = 0;
unsigned long pulseEnd = 0;

volatile bool rcOverride = false;

// RC interrupt
ISR(INT0_vect)
{
  int currentLevel = IS_SET(PINB, PINB2);
  if (initiated) {
    unsigned long m = micros();
    if (currentLevel) {
      float pulseLength = pulseEnd - pulseStart;
      if (600 < pulseLength && pulseLength < 2600) {
        counts[currentCounter++ % resolution] = pulseLength / (m - pulseStart);
        float sum = 0;
        for (int i = 0; i < resolution; ++i) {
          sum += counts[i];
        }
        float currentMotorDutyCycle = sum / resolution;
        rcOverride = currentMotorDutyCycle > RC_OVERRIDE_THRESHOLD;
      }
      pulseStart = m;
    } else {
      pulseEnd = m;
    }
  } else {
    if (pulseStart) {
      pulseEnd = micros();
      initiated = true;
    } else if (currentLevel) {
      pulseStart = micros();
    }
  }
}

void setup() {
  // PB0 as output
  SET(DDRB, DDB0);
  // PB3 as input
  CLEAR(DDRB, DDB3);
  // PB2 as interrupt input
  CLEAR(DDRB, DDB2);

  // pin change interrupt
  CLEAR(MCUCR, ISC01);
  SET(MCUCR, ISC00);

  // enable interrupt
  SET(GIMSK, INT0);
  //SREG |= 0x80;
}

void loop() {
  bool switchToAutopilot;
  if (rcOverride) {
    switchToAutopilot = false;
  } else {
    // if PB3 is high, which is if autopilot control is requested
    switchToAutopilot = IS_SET(PINB, PINB3);
  }
  if (switchToAutopilot) {
    SET(PORTB, PB0);
  } else {
    CLEAR(PORTB, PB0);
  }
}
