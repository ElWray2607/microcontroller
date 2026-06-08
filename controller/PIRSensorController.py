import asyncio

from service.PIRSensorService import PIRSensorService
from util.networking import MQTTManager


class PIRSensorController:
    TOPIC_GAS_SENSOR_STATE = "home/motion/state"

    def __init__(self, mqtt_client: MQTTManager, pir_sensor_pin_id: int):
        self.mqtt_client = mqtt_client
        self.pir_sensor_service = PIRSensorService(pir_sensor_pin_id)

    async def run(self):
        while True:
            self.mqtt_client.publish(self.TOPIC_GAS_SENSOR_STATE, self.pir_sensor_service.motion_detected())
            await asyncio.sleep(1)