from machine import Pin, PWM


class MotorModuleService:
    def __init__(self, inp_pin, inm_pin):
        self.INm = PWM(Pin(inm_pin, Pin.OUT), freq=10000)
        self.INp = PWM(Pin(inp_pin, Pin.OUT), freq=10000)
        self.turned_on = False
        self.clockwise = True
        self.speed = 0
        self.preset = None

    def _map_speed_to_duty(self, speed):
        if speed <= 0:
            return 0

        min_working_speed = 7
        max_speed = 10
        max_duty = 1023

        min_working_duty = int((min_working_speed / max_speed) * max_duty)

        return int(min_working_duty + ((speed / max_speed) * (max_duty - min_working_duty)))

    def _set_duty(self, duty):
        if self.clockwise:
            self.INm.duty(0)
            self.INp.duty(duty)
        else:
            self.INp.duty(0)
            self.INm.duty(duty)

    def turn_off(self):
        self.set_speed(0)
        self.turned_on = False

    def turn_on(self):
        if self.speed == 0:
            self.speed = 3

        self.set_speed(self.speed)
        self.turned_on = True

    def set_speed(self, speed):
        self.speed = speed

        if self.speed > 0:
            self.turned_on = True
        else:
            self.turned_on = False

        duty = self._map_speed_to_duty(speed)

        self._set_duty(duty)

    def set_preset(self, preset):
        self.preset = preset
        self.set_speed(preset)

    def set_direction(self, clockwise):
        self.clockwise = clockwise
        self.set_speed(self.speed)

    def get_speed(self):
        return self.speed

    def get_state(self):
        return "true" if self.turned_on else "false"

    def get_direction(self):
        if self.clockwise:
            return "forward"
        return "reverse"

    def get_preset(self):
        if self.preset == MotorPreset.OFF:
            return "OFF"
        if self.preset == MotorPreset.LOW:
            return "LOW"
        if self.preset == MotorPreset.MEDIUM:
            return "MEDIUM"
        if self.preset == MotorPreset.HIGH:
            return "HIGH"
        return None


class MotorPreset:
    OFF = 0
    LOW = 4
    MEDIUM = 7
    HIGH = 10