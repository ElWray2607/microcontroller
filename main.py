import asyncio

from controller.BuzzerModuleController import BuzzerModuleController
from controller.DoorController import DoorController
from controller.MotorModuleController import MotorModuleController
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
    window_controller = WindowController(mqtt_manager, 13)
    door_controller = DoorController(mqtt_manager, 5)

asyncio.run(main())