import asyncio

from service.MotorModuleService import MotorModuleService, MotorPreset
from util.networking import MQTTManager


class MotorModuleController:
    TOPIC_MOTOR_STATE = "home/motor/state"
    TOPIC_MOTOR_SET = "home/motor/set"
    TOPIC_MOTOR_DIRECTION_STATE = "home/motor/direction/state"
    TOPIC_MOTOR_DIRECTION_SET = "home/motor/direction/set"
    TOPIC_MOTOR_SPEED_STATE = "home/motor/speed/percentage/state"
    TOPIC_MOTOR_SPEED_SET = "home/motor/speed/percentage/set"
    TOPIC_MOTOR_PRESET_STATE = "home/motor/preset/presetmode/state"
    TOPIC_MOTOR_PRESET_SET = "home/motor/preset/presetmode/set"

    def __init__(self, mqtt_client: MQTTManager, inp_pin_id: int, inm_pin_id: int):
        self.mqtt_client = mqtt_client
        self.motor_module_service = MotorModuleService(inp_pin=inp_pin_id, inm_pin=inm_pin_id)

        self.mqtt_client.subscribe(self.TOPIC_MOTOR_SET, self.on_motor_state_change)
        self.mqtt_client.subscribe(self.TOPIC_MOTOR_SPEED_SET, self.on_motor_speed_change)
        self.mqtt_client.subscribe(self.TOPIC_MOTOR_PRESET_SET, self.on_motor_preset_change)
        self.mqtt_client.subscribe(self.TOPIC_MOTOR_DIRECTION_SET, self.on_motor_direction_change)

        asyncio.create_task(self.publish_state())

    async def on_motor_state_change(self, topic, payload):
        if payload == "true":
            self.motor_module_service.turn_on()
        elif payload == "false":
            self.motor_module_service.turn_off()

        asyncio.create_task(self.publish_state())

    async def on_motor_speed_change(self, topic, payload):
        self.motor_module_service.set_speed(int(payload))
        asyncio.create_task(self.publish_state())

    async def on_motor_direction_change(self, topic, payload):
        if payload == "forward":
            self.motor_module_service.set_direction(clockwise=True)
        else:
            self.motor_module_service.set_direction(clockwise=False)

        asyncio.create_task(self.publish_state())

    async def on_motor_preset_change(self, topic, payload):
        preset = getattr(MotorPreset, payload.upper())
        self.motor_module_service.set_preset(preset)
        asyncio.create_task(self.publish_state())

    async def publish_state(self):
        self.mqtt_client.publish(self.TOPIC_MOTOR_STATE, self.motor_module_service.get_state())
        self.mqtt_client.publish(self.TOPIC_MOTOR_SPEED_STATE, self.motor_module_service.get_speed())
        self.mqtt_client.publish(self.TOPIC_MOTOR_DIRECTION_STATE, self.motor_module_service.get_direction())
        self.mqtt_client.publish(self.TOPIC_MOTOR_PRESET_STATE, self.motor_module_service.get_preset())