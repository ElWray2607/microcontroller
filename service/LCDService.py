from machine import Pin, SoftI2C

from lcd_api.i2c_lcd import I2cLcd


class LCDService:
    def __init__(self, scl_pin: int = 22, sda_pin: int = 21):
        self.DEFAULT_I2C_ADDR = 0x27

        scl_pin = Pin(scl_pin, Pin.OUT, pull=Pin.PULL_UP)  # GPIO22 with internal pull-up enabled
        sda_pin = Pin(sda_pin, Pin.OUT, pull=Pin.PULL_UP)  # GPIO21 with internal pull-up enabled

        i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100000)
        self.lcd = I2cLcd(i2c, self.DEFAULT_I2C_ADDR, 2, 16)

    def show_message(self, message: str):
        self.lcd.clear()
        self.lcd.putstr(message)