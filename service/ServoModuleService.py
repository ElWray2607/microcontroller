import asyncio
from machine import Pin, PWM


class ServoModuleService:
    def __init__(self, pin_id):
        self._servo = PWM(Pin(pin_id))
        self._servo.freq(50)
        self._position = 0
        self._moving = False
        self._stop_requested = False
        self.state = None

    def _angle_to_duty(self, position_percentage):
        value = max(0, min(100, position_percentage))
        return int((value / 100) * 128)

    def set_position(self, position):
        self._position = position
        duty = self._angle_to_duty(position)

        print("Set servo to position:", duty)
        self._servo.duty(duty)

    def set_state(self, state):
        self.set_position(state)
        self.state = state

    def get_position(self):
        print("Motor position:", self._position)
        return self._position

    def get_state(self):
        print("Motor state:", self.state)
        if self.state == ServoPosition.OPEN:
            return "OPEN"
        if self.state == ServoPosition.CLOSE:
            return "CLOSE"
        if self.state == ServoPosition.STOP:
            return "STOP"
        return None


class ServoPosition:
    OPEN = 100
    STOP = None
    CLOSE = 0
