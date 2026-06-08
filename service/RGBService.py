from machine import Pin
import neopixel

class RGBService:
    """
    Control a Neopixel RGB LED module.

    :param pin_id: The GPIO pin number used to interface with the RGB LED module.
    :type pin_id: int
    :param pixel_count: The number of pixels in the RGB LED module.
    :type pixel_count: int
    """
    def __init__(self, pin_id, pixel_count=4):
        self.pin = Pin(pin_id, Pin.OUT)
        self.pixel_count = pixel_count
        self.np = neopixel.NeoPixel(self.pin, self.pixel_count)
        self.color = [255, 255, 255]
        self.brightness = 255
        self.is_on = False
        self._write_pixels()

    def _clamp(self, value, minimum=0, maximum=255):
        return max(minimum, min(maximum, int(value)))

    def _scaled_color(self):
        scale = self.brightness / 255
        return (
            int(self.color[0] * scale),
            int(self.color[1] * scale),
            int(self.color[2] * scale)
        )

    def _write_pixels(self):
        if self.is_on:
            color = self._scaled_color()
        else:
            color = (0, 0, 0)

        for i in range(0, self.pixel_count):
            self.np[i] = color

        self.np.write()

    def turn_on(self):
        """
        Turn the RGB module on using the current color and brightness.

        :return: None
        """
        self.is_on = True
        self._write_pixels()
        print("RGB module turned on")

    def turn_off(self):
        """
        Turn the RGB module off.

        :return: None
        """
        self.is_on = False
        self._write_pixels()
        print("RGB module turned off")

    def set_color(self, r, g, b):
        """
        Set the color for all pixels uniformly.

        :param r: Red color intensity value (0-255).
        :type r: int
        :param g: Green color intensity value (0-255).
        :type g: int
        :param b: Blue color intensity value (0-255).
        :type b: int
        :return: None
        """
        self.color = [
            self._clamp(r),
            self._clamp(g),
            self._clamp(b)
        ]
        self._write_pixels()
        print("Set color to:", self.color)

    def set_brightness(self, brightness):
        """
        Set the brightness for the RGB module.

        :param brightness: Brightness value from 0 to 255.
        :type brightness: int
        :return: None
        """
        self.brightness = self._clamp(brightness)
        self._write_pixels()
        print("Set brightness to:", self.brightness)

    def get_color(self):
        return self.color

    def get_brightness(self):
        return self.brightness

    def get_state(self):
        if self.is_on:
            return "ON"
        return "OFF"