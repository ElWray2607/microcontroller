import asyncio
from enum import Enum
from machine import Pin, PWM


class ServoModuleService:
    def __init__(self, pin_id):
        self._servo = PWM(Pin(pin_id))
        self._servo.freq(50)
        self._position = 0
        self._moving = False
        self._stop_requested = False
        self.state = None

    def _angle_to_duty(self, angle):
        angle = max(0, min(180, angle))
        return int(25 + (angle / 180) * 103)

    def set_position(self, position):
        self._position = position
        duty = self._angle_to_duty(position)
        self._servo.duty(duty)

    async def move_to(self, target_position, step_delay_ms=20):
        target_position = max(0, min(180, target_position))
        self._moving = True
        self._stop_requested = False

        if target_position > self._position:
            step = 1
        else:
            step = -1

        while self._position != target_position:
            if self._stop_requested:
                break

            self.set_position(self._position + step)
            await asyncio.sleep_ms(step_delay_ms)

        self._moving = False

    def stop(self):
        self._stop_requested = True
        self.set_position(self._position)

    def set_state(self, state):
        if state == ServoPosition.STOP:
            self._stop_requested = True
        else:
            self.move_to(state)
            
        self.state = state

    def get_position(self):
        return self._position

    def get_state(self):
        return self.state.name


class ServoPosition(Enum):
    OPEN = 180
    STOP = None
    CLOSE = 0