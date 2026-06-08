from enum import Enum
from machine import Pin, PWM


class MotorModuleService:
    def __init__(self, inp_pin, inm_pin):
        self.INm = PWM(Pin(inm_pin, Pin.OUT), 1000)
        self.INp = PWM(Pin(19, Pin.OUT), 10000)
        self.clockwise = True
        self.speed = 0
        self.preset = None

    def _map_speed_to_duty(self, speed):
        return int((speed / 10) * 1023)

    def _set_duty(self, duty):
        if self.clockwise:
            self.INm.duty(0)
            self.INp.duty(duty)
        else:
            self.INp.duty(0)
            self.INm.duty(duty)

    def turn_off(self):
        self.set_speed(0)

    def turn_on(self):
        self.set_speed(self.speed)

    def set_speed(self, speed):
        self.speed = speed

        duty = self._map_speed_to_duty(speed)

        self._set_duty(duty)

    def set_preset(self, preset):
        self.preset = preset
        self.set_speed(preset)

    def set_direction(self, clockwise):
        self.clockwise = clockwise

    def get_speed(self):
        return self.speed

    def get_state(self):
        if self.speed > 0:
            return "ON"
        return "OFF"

    def get_direction(self):
        if self.clockwise:
            return "CLOCKWISE"
        return "COUNTERCLOCKWISE"

    def get_preset(self):
        return self.preset.name

class MotorPreset(Enum):
    OFF = 0
    LOW = 4
    MEDIUM = 7
    HIGH = 10