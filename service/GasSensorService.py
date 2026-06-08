from machine import Pin


class GasSensorService:
    """
    Manages the gas sensor functionality for detecting gas and reporting its presence.

    :param pin_id: Configured GPIO pin for the gas sensor.
    :type pin_id: int
    """
    def __init__(self, pin_id):
        self.pin = Pin(pin_id, Pin.IN, Pin.PULL_UP)

    def gas_detected(self):
        """
        Determines whether gas is detected based on the sensor's reading.

        :return: True if gas is detected, False otherwise
        :rtype: bool
        """
        gas_value = self.pin.value()
        print(f"Gas value: {gas_value}")

        if gas_value == 1:
            return "false"
        else:
            return "true"