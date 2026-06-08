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

        asyncio.create_task(self.init_controller())

    async def on_motor_state_change(self, topic, payload):
        state = getattr(ServoPosition, payload.upper())
        print("Received state change:", state)
        self.servo_module_service.set_state(state)
        self.mqtt_client.publish(self.TOPIC_MOTOR_STATE, self.servo_module_service.get_state())

    async def init_controller(self):
        self.mqtt_client.publish(self.TOPIC_MOTOR_STATE, self.servo_module_service.get_state())