import asyncio

from service.MotorModuleService import MotorModuleService, MotorPreset
from util.networking import MQTTManager


class MotorModuleController:
    TOPIC_MOTOR_STATE = "home/motor/state"
    TOPIC_MOTOR_SET = "home/motor/set"
    TOPIC_MOTOR_DIRECTION_STATE = "home/motor/direction/state"
    TOPIC_MOTOR_DIRECTION_SET = "home/motor/direction/set"
    TOPIC_MOTOR_SPEED_STATE = "home/motor/speed/state"
    TOPIC_MOTOR_SPEED_SET = "home/motor/speed/set"
    TOPIC_MOTOR_PRESET_STATE = "home/motor/preset/state"
    TOPIC_MOTOR_PRESET_SET = "home/motor/preset/set"

    def __init__(self, mqtt_client: MQTTManager, inp_pin_id: int, inm_pin_id: int):
        self.mqtt_client = mqtt_client
        self.motor_module_service = MotorModuleService(inp_pin=inp_pin_id, inm_pin=inm_pin_id)

        self.mqtt_client.subscribe(self.TOPIC_MOTOR_SET, self.on_motor_state_change)
        self.mqtt_client.subscribe(self.TOPIC_MOTOR_SPEED_SET, self.on_motor_speed_change)
        self.mqtt_client.subscribe(self.TOPIC_MOTOR_PRESET_SET, self.on_motor_preset_change)
        self.mqtt_client.subscribe(self.TOPIC_MOTOR_DIRECTION_SET, self.on_motor_direction_change)

    async def on_motor_state_change(self, topic, payload):
        if payload == "true":
            self.motor_module_service.turn_on()
        elif payload == "false":
            self.motor_module_service.turn_off()

        self.mqtt_client.publish(self.TOPIC_MOTOR_STATE, self.motor_module_service.get_state())

    async def on_motor_speed_change(self, topic, payload):
        self.motor_module_service.set_speed(payload)
        self.mqtt_client.publish(self.TOPIC_MOTOR_SPEED_STATE, self.motor_module_service.get_speed())

    async def on_motor_direction_change(self, topic, payload):
        if payload == "forward":
            self.motor_module_service.set_direction(clockwise=True)
        else:
            self.motor_module_service.set_direction(clockwise=False)

        self.mqtt_client.publish(self.TOPIC_MOTOR_DIRECTION_STATE, self.motor_module_service.get_direction())

    async def on_motor_preset_change(self, topic, payload):
        self.motor_module_service.set_preset(MotorPreset[payload.upper()])
        self.mqtt_client.publish(self.TOPIC_MOTOR_PRESET_STATE, self.motor_module_service.get_preset())