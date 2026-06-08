import asyncio

from service.GasSensorService import GasSensorService
from util.networking import MQTTManager

class GasSensorController:
    TOPIC_GAS_SENSOR_STATE = "home/gas/detected"

    def __init__(self, mqtt_client: MQTTManager, gas_sensor_pin_id: int):
        self.mqtt_client = mqtt_client
        self.gas_sensor_service = GasSensorService(gas_sensor_pin_id)

    async def run(self):
        while True:
            self.mqtt_client.publish(self.TOPIC_GAS_SENSOR_STATE, self.gas_sensor_service.gas_detected())
            await asyncio.sleep(2)