from machine import Pin

class PIRSensorService:
    def __init__(self, pin_id):
        self.sensor = Pin(pin_id)

    def motion_detected(self):
        motion_detected = self.sensor.value()

        if motion_detected == 1:
            return "on"
        else:
            return "off"