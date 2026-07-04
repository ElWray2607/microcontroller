import asyncio

from service.ButtonService import ButtonService


class ButtonController:
    def __init__(self, pin_id, button_name, mqtt_client):
        self.button_service = ButtonService(pin_id)
        self.button_name = button_name
        self.mqtt_client = mqtt_client
        self.TOPIC_BUTTON_PRESSED = f"home/button/{button_name}/pressed"

    async def run(self):
        while True:
            if self.button_service.isPressed():
                self.mqtt_client.publish(self.TOPIC_BUTTON_PRESSED, "true")
            await asyncio.sleep(0.5)