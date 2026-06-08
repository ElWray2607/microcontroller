import asyncio

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


asyncio.run(main())