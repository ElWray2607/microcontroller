from machine import Pin

class LEDService:
    def __init__(self, pin_id):
        self.led = Pin(pin_id, Pin.OUT)
        self.state = "OFF"

    def turn_on(self):
        self.led.value(1)
        self.state = "ON"

    def turn_off(self):
        self.led.value(0)
        self.state = "OFF"

    def get_state(self):
        return self.state