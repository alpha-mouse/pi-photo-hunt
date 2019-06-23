This code is for attiny85 that with the help of SN74HC153N selector grants control over the motor and rudder either to the original remote control or to the raspberry doing autopiloting.

Attiny acts as a safeguard. It motitors remote control commands, and if remote control is active, then it gets control over the boat, regardless of what raspberry wants.

In the schematic, raspberry pi has three wires to control router: one that it sets high, when it wants to autopilot, and two wires with PWM motor and rudder control.
The in-built remote control has 4 wires into router: ground, +5V, and two PWMs.
Two output wires leave the router: resultant PWM control signals to the motor and rudder.
