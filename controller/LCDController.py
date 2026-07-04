import asyncio

from service.LCDService import LCDService


class LCDController:
    TOPIC_LCD_TEXT = "home/lcd/set"
    TOPIC_LCD_STATE = "home/lcd/state"

    def __init__(self, mqtt_manager, scl_pin = 22, sda_pin = 21):
        self.lcd_service = LCDService(scl_pin, sda_pin)
        self.mqtt_manager = mqtt_manager
        mqtt_manager.subscribe(self.TOPIC_LCD_TEXT, self.on_lcd_text)

        asyncio.create_task(self.init_controller())

    async def on_lcd_text(self, topic, payload):
        self.lcd_service.show_message(payload)
        self.mqtt_manager.publish(self.TOPIC_LCD_STATE, payload)

    async def init_controller(self):
        self.lcd_service.show_message("")
        self.mqtt_manager.publish(self.TOPIC_LCD_STATE, "")