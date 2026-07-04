import asyncio

from controller.BuzzerModuleController import BuzzerModuleController
from controller.DHT11Controller import DHT11Controller
from controller.DoorController import DoorController
from controller.GasSensorController import GasSensorController
from controller.LCDController import LCDController
from controller.MotorModuleController import MotorModuleController
from controller.PIRSensorController import PIRSensorController
from controller.RGBController import RGBController
from controller.WindowController import WindowController
from util.networking import NetworkManager, MQTTManager

WIFI_SSID = "Schueler-Mobil"
WIFI_PASSWORD = "nfSuLITC"

CLIENT_ID = "HOMECONTROL"
BROKER_IP = "192.168.8.100"

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

async def main():
    network_manager = await init_wifi()
    mqtt_manager = await init_mqtt()

    rgb_controller = RGBController(mqtt_manager, 26)
    buzzer_controller = BuzzerModuleController(mqtt_manager, 25)
    fan_controller = MotorModuleController(mqtt_manager, inm_pin_id=18, inp_pin_id=19)
    window_controller = WindowController(mqtt_manager, 5)
    door_controller = DoorController(mqtt_manager, 13)
    gas_sensor = GasSensorController(mqtt_manager, 23)
    dht11_controller = DHT11Controller(mqtt_manager, 17)
    motion_controller = PIRSensorController(mqtt_manager, 14)
    lcd_controller = LCDController(mqtt_manager)

    asyncio.create_task(gas_sensor.run())
    asyncio.create_task(dht11_controller.run())
    asyncio.create_task(motion_controller.run())

    while True:
        await asyncio.sleep(1)

asyncio.run(main())