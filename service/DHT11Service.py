import machine
import time
import dht

class DHT11Service:
    """
    Manages the DHT11 sensor functionality for measuring temperature and humidity.

    :param pin_id: Configured GPIO pin for the DHT11 sensor.
    :type pin_id: int
    """
    def __init__(self, pin_id):
        self.dht = dht.DHT11(machine.Pin(17))

    def measure(self):
        """
        Triggers a measurement process using the associated DHT sensor instance.
        """
        self.dht.measure()

    def get_temperature(self):
        """
        Get the current temperature reading from the DHT sensor.

        :return: The current temperature value retrieved from the DHT sensor.
        :rtype: float
        """
        return self.dht.temperature()

    def get_humidity(self):
        """
       Get the current humidity value from the sensor.

        :return: The current humidity value.
        :rtype: float
        """
        return self.dht.humidity()