from machine import Pin, PWM


class ButtonService:
    def __init__(self, pin_id):
        self._button = Pin(pin_id, Pin.IN, Pin.PULL_UP)

    def isPressed(self):
        return self._button.value() == 0