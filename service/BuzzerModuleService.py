from machine import Pin, PWM


class BuzzerModuleService:
    def __init__(self, pin_id):
        self._buzzer = PWM(Pin(pin_id))
        self._frequency = 880
        self._buzzing = False

    def turn_on(self):
        self._buzzer.duty(1000)
        self._buzzer.freq(self._frequency)
        self._buzzing = True


    def turn_off(self):
        self._buzzer.duty(0)
        self._buzzing = False

    def get_state(self):
        if self._buzzing:
            return "ON"

        return "OFF"