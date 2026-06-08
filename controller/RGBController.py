from service.RGBService import RGBService
from util.networking import MQTTManager

class RGBController:
    TOPIC_LIGHT_STATE_CHANGE = "home/rgb_light/set"
    TOPIC_LIGHT_STATE = "home/rgb_light/state"

    TOPIC_LIGHT_BRIGHTNESS_STATE_CHANGE = "home/rgb_light/brightness/set"
    TOPIC_LIGHT_BRIGHTNESS_STATE = "home/rgb_light/brightness/state"

    TOPIC_LIGHT_RGB_STATE_CHANGE = "home/rgb_light/rgb/set"
    TOPIC_LIGHT_RGB_STATE = "home/rgb_light/rgb/state"

    def __init__(self, mqtt_client: MQTTManager, rgb_pin_id: int, rgb_pixel_count: int = 4):
        self.mqtt_client = mqtt_client
        self.rgb_service = RGBService(rgb_pin_id, rgb_pixel_count)
        self.mqtt_client.subscribe(self.TOPIC_LIGHT_STATE_CHANGE, self.on_light_state_change)
        self.mqtt_client.subscribe(self.TOPIC_LIGHT_BRIGHTNESS_STATE_CHANGE, self.on_light_brightness_change)
        self.mqtt_client.subscribe(self.TOPIC_LIGHT_RGB_STATE_CHANGE, self.on_light_rgb_change)

    def on_light_state_change(self, topic, payload):
        print("Received light state change:", payload)
        if payload == "ON":
            self.rgb_service.turn_on()
        elif payload == "OFF":
            self.rgb_service.turn_off()

        print("Current light state:", self.rgb_service.get_state())
        self.mqtt_client.publish(self.TOPIC_LIGHT_STATE, self.rgb_service.get_state())

    def on_light_brightness_change(self, topic, payload):
        print("Received light brightness change:", payload)
        self.rgb_service.set_brightness(payload)
        self.mqtt_client.publish(self.TOPIC_LIGHT_BRIGHTNESS_STATE, self.rgb_service.get_brightness())

    def on_light_rgb_change(self, topic, payload):
        print("Received light RGB change:", payload)
        r, g, b = map(int, payload.split(","))
        self.rgb_service.set_color(int(r), int(g), int(b))
        self.mqtt_client.publish(self.TOPIC_LIGHT_RGB_STATE, self.rgb_service.get_color())