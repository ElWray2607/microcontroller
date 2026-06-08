import asyncio

from service.ServoModuleService import ServoModuleService, ServoPosition
from util.networking import MQTTManager


class DoorController:
    TOPIC_MOTOR_STATE = "home/door/state"
    TOPIC_MOTOR_SET = "home/door/set"

    def __init__(self, mqtt_client: MQTTManager, window_motor_pin_id: int):
        self.mqtt_client = mqtt_client
        self.servo_module_service = ServoModuleService(window_motor_pin_id)

        self.mqtt_client.subscribe(self.TOPIC_MOTOR_SET, self.on_motor_state_change)

    async def on_motor_state_change(self, topic, payload):
        self.servo_module_service.set_position(int(payload))
        self.mqtt_client.publish(self.TOPIC_MOTOR_STATE, self.servo_module_service.get_state())