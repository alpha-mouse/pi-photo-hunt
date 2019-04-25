from gpiozero import Servo, DigitalOutputDevice


class Motion:
    _speedPin = 12
    _directionPin = 13
    _enabledPin = 6

    def __init__(self):
        self._speed = 0
        self._direction = 0
        self._enabled = False

        self._enabledOutput = DigitalOutputDevice(self._enabledPin)
        self._speedServo = Servo(self._speedPin)
        self._directionServo = Servo(self._directionPin)

    def enable(self):
        self._enabled = True
        self._update()

    def disable(self):
        self._enabled = False
        self._update()

    def set_values(self, speed = None, direction = None):
        self._speed = speed if speed is not None else self._speed
        self._direction = direction if direction is not None else self._direction
        self._update()

    def _update(self):
        self._enabledOutput.value = 1 if self._enabled else 0
        self._speedServo.value = self._speed
        self._directionServo.value = self._direction
