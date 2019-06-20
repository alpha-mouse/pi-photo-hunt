from gpiozero import DigitalOutputDevice
from pwm import PWM
import time

speed_offset = 0.25
speed_scale = 0.9

direction_offset = 0
direction_scale = 1.4

""" value from -1 to 1 translated into 1000000 to 2000000 range """
def _translate_duty_cycle(value, offset = 0, scale = 1):
    offsetted_and_scaled = ((1 + value*scale + offset) / 2)
    bounded = max(0, min (offsetted_and_scaled, 1))
    return int(1000000 + bounded * 1000000)

class Motion:
    _enabledPin = 6

    def __init__(self):
        self._speed = 0
        self._direction = 0
        self._enabled = False

        self._enabledOutput = DigitalOutputDevice(self._enabledPin)
        self._speedPwm = PWM(0) # pin 12
        self._directionPwm = PWM(1) # pin 13

        self._speedPwm.export()
        self._directionPwm.export()

        time.sleep(1) # wait till pwms are exported

        self._speedPwm.period = 50000000
        self._directionPwm.period = 50000000

    def enable(self):
        self._updatePwm()
        self._speedPwm.enable = True
        self._directionPwm.enable = True
        self._enabledOutput.value = 1 if self._enabled else 0

    def disable(self):
        self._enabledOutput.value = 1 if self._enabled else 0
        self._speedPwm.enable = False
        self._directionPwm.enable = False

    def set_values(self, speed = None, direction = None):
        self._speed = speed if speed is not None else self._speed
        self._direction = direction if direction is not None else self._direction
        self._updatePwm()

    def _updatePwm(self):
        self._speedPwm.duty_cycle  = _translate_duty_cycle(self._speed, speed_offset, speed_scale)
        self._directionPwm.duty_cycle  = _translate_duty_cycle(self._direction, direction_offset, direction_scale)
