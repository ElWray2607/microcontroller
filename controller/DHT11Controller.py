import asyncio
from util.networking import MQTTManager
from service.DHT11Service import DHT11Service


class DHT11Controller:
    TOPIC_TEMPERATURE_SENSOR = "home/dht11/temperature"
    TOPIC_HUMIDITY_SENSOR = "home/dht11/humidity"

    def __init__(self, mqtt_client: MQTTManager, dht11_sensor_pin: int):
        self.mqtt_client = mqtt_client
        self.dht11_service = DHT11Service(dht11_sensor_pin)

    async def run(self):
        while True:
            self.dht11_service.measure()
            self.mqtt_client.publish(self.TOPIC_HUMIDITY_SENSOR, self.dht11_service.get_humidity())
            self.mqtt_client.publish(self.TOPIC_TEMPERATURE_SENSOR, self.dht11_service.get_temperature())
            await asyncio.sleep(2)