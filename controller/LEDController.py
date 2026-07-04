import asyncio
from service.LEDService import LEDService
from util.networking import MQTTManager


class LEDController:
    TOPIC_LED_STATE = "home/yellow_led/state"
    TOPIC_LED_SET = "home/yellow_led/set"

    def __init__(self, mqtt_client: MQTTManager, gas_sensor_pin_id: int):
        self.mqtt_client = mqtt_client
        self.led_service = LEDService(gas_sensor_pin_id)

        self.mqtt_client.subscribe(self.TOPIC_LED_SET, self.on_led_state_change)

        self.mqtt_client.publish(self.TOPIC_LED_STATE, self.led_service.get_state())

    async def on_led_state_change(self, topic, payload):
        if payload == "ON":
            self.led_service.turn_on()
        elif payload == "OFF":
            self.led_service.turn_off()

        self.mqtt_client.publish(self.TOPIC_LED_STATE, self.led_service.get_state())