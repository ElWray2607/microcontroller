import asyncio
import machine

from controller.ButtonController import ButtonController
from controller.BuzzerModuleController import BuzzerModuleController
from controller.DHT11Controller import DHT11Controller
from controller.DoorController import DoorController
from controller.GasSensorController import GasSensorController
from controller.LCDController import LCDController
from controller.LEDController import LEDController
from controller.MotorModuleController import MotorModuleController
from controller.PIRSensorController import PIRSensorController
from controller.RGBController import RGBController
from controller.WindowController import WindowController
from util.networking import NetworkManager, MQTTManager

WIFI_SSID = "Schueler-Mobil"
WIFI_PASSWORD = "nfSuLITC"

CLIENT_ID = "HOMECONTROL"
BROKER_IP = "192.168.8.150"

async def init_wifi():
    network_manager = NetworkManager(WIFI_SSID, WIFI_PASSWORD)
    await network_manager.connect()

    if network_manager.is_connected():
        print("WiFi status:")
        print(network_manager.status())

    return network_manager

async def init_mqtt():
    mqtt_manager = MQTTManager(CLIENT_ID, BROKER_IP)
    await mqtt_manager.connect()

    return mqtt_manager

async def safe_run(task_name, coro):
    try:
        print(f"Starting task: {task_name}")
        await coro
    except Exception as e:
        print(f"Task '{task_name}' failed with error: {e}")

async def main():
    try:
        network_manager = await init_wifi()
        mqtt_manager = await init_mqtt()
        
        # Start MQTT listener task
        mqtt_listener_task = asyncio.create_task(mqtt_manager.listen())

        rgb_controller = RGBController(mqtt_manager, 26)
        buzzer_controller = BuzzerModuleController(mqtt_manager, 25)
        fan_controller = MotorModuleController(mqtt_manager, inm_pin_id=18, inp_pin_id=19)
        window_controller = WindowController(mqtt_manager, 5)
        door_controller = DoorController(mqtt_manager, 13)
        gas_sensor = GasSensorController(mqtt_manager, 23)
        dht11_controller = DHT11Controller(mqtt_manager, 17)
        motion_controller = PIRSensorController(mqtt_manager, 14)
        led_controller = LEDController(mqtt_manager, 12)
        lcd_controller = LCDController(mqtt_manager)
        button_left_controller = ButtonController(16, "left", mqtt_manager)
        button_right_controller = ButtonController(27, "right", mqtt_manager)

        asyncio.create_task(safe_run("gas_sensor", gas_sensor.run()))
        asyncio.create_task(safe_run("dht11_controller", dht11_controller.run()))
        asyncio.create_task(safe_run("motion_controller", motion_controller.run()))
        asyncio.create_task(safe_run("button_left_controller", button_left_controller.run()))
        asyncio.create_task(safe_run("button_right_controller", button_right_controller.run()))

        while True:
            if mqtt_listener_task.done():
                await mqtt_listener_task

            await asyncio.sleep(1)
    except Exception as e:
        print(f"Main loop crashed: {e}")
        await asyncio.sleep(5)
        machine.reset()

asyncio.run(main())