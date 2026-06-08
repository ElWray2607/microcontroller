import asyncio

from service.BuzzerModuleService import BuzzerModuleService
from util.networking import MQTTManager


class BuzzerModuleController:
    TOPIC_BUZZER_MODULE_STATE = "home/buzzer/state"
    TOPIC_BUZZER_MODULE_SET = "home/buzzer/set"

    def __init__(self, mqtt_client: MQTTManager, buzzer_module_pin_id: int):
        self.mqtt_client = mqtt_client
        self.buzzer_module_service = BuzzerModuleService(buzzer_module_pin_id)

        self.mqtt_client.subscribe(self.TOPIC_BUZZER_MODULE_SET, self.on_buzzer_module_state_change)

        asyncio.create_task(self.init_controller())

    async def on_buzzer_module_state_change(self, topic, payload):
        if payload == "ON":
            self.buzzer_module_service.turn_on()
        elif payload == "OFF":
            self.buzzer_module_service.turn_off()

        self.mqtt_client.publish(self.TOPIC_BUZZER_MODULE_STATE, self.buzzer_module_service.get_state())

    async def init_controller(self):
        self.buzzer_module_service.turn_off()
        self.mqtt_client.publish(self.TOPIC_BUZZER_MODULE_STATE, self.buzzer_module_service.get_state())
