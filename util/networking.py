import network
import uasyncio as asyncio

from umqtt.simple import MQTTClient


class NetworkManager:
    def __init__(self, ssid, password, timeout=15):
        self.ssid = ssid
        self.password = password
        self.timeout = timeout
        self.wifi = network.WLAN(network.STA_IF)

    async def connect(self):
        """
        Connect to the WiFi network.
        """
        print("Resetting WiFi...")

        self.wifi.active(True)
        self.wifi.disconnect()
        await asyncio.sleep(2)

        self.wifi.active(False)
        await asyncio.sleep(2)

        self.wifi.active(True)
        await asyncio.sleep(2)

        if self.wifi.isconnected():
            self.wifi.disconnect()
            await asyncio.sleep(1)

        print("Connecting to WiFi:", self.ssid)
        self.wifi.connect(self.ssid, self.password)

        timeout = self.timeout
        while not self.wifi.isconnected() and timeout > 0:
            print("WiFi status:", self.wifi.status())
            await asyncio.sleep(1)
            timeout -= 1

        if self.wifi.isconnected():
            print("WiFi connected")
            print("WiFi config:", self.wifi.ifconfig())
            return

        print("Final WiFi status:", self.wifi.status())
        raise RuntimeError("Failed to connect to WiFi")

    async def print(self):
        print("WiFi Config:")
        print(self.wifi.ifconfig())

        print("WiFi Status:")
        print(self.wifi.status())

        print("WiFi rsi:")
        print(self.wifi.status("rssi"))

    def disconnect(self):
        """
        Disconnect from the WiFi network.
        """
        if self.wifi.isconnected():
            self.wifi.disconnect()

        self.wifi.active(False)
        print("WiFi disconnected")

    def is_connected(self):
        """
        Check if the WiFi network is connected.
        :return: True if connected, False otherwise
        """
        return self.wifi.isconnected()

    def status(self):
        """
        Get the current status of the WiFi network.
        :return: A tuple containing IP address, subnet mask, gateway, and DNS servers
        """
        return self.wifi.ifconfig()


class MQTTManager:
    def __init__(self, client_id, broker, port=1883):
        """
        Initializes a new instance of the MQTT Manager.

        :param client_id: Unique identifier for the MQTT client.
        :type client_id: str
        :param broker: Address of the MQTT broker.
        :type broker: str
        :param port: Port to connect to on the MQTT broker. Defaults to 1883.
        :type port: int
        """
        self.client = MQTTClient(
            client_id=client_id,
            server=broker,
            port=port
        )
        self.topic_callbacks = {}
        self.connected = False
        self.running = False

    async def connect(self):
        """
        Connect to the MQTT broker.
        :return:
        """
        self.client.set_callback(self._handle_message)
        self.client.connect()
        self.connected = True
        self.client.subscribe(b"#")
        print("MQTT connected")

    def subscribe(self, topic, callback):
        """
        :param topic: The topic to subscribe to. Can be provided as a string.
        :param callback: A function to handle messages received on the subscribed topic.
        """
        if isinstance(topic, str):
            topic = topic.encode()

        self.topic_callbacks[topic] = callback

        print("Subscribed to:", topic)

    def _handle_message(self, topic, message):
        callback = self.topic_callbacks.get(topic)

        if callback is None:
            print("No callback registered for topic:", topic)
            return

        asyncio.create_task(callback(topic, message.decode()))

    async def listen(self, delay_ms=100):
        """
        Asynchronously listen for incoming messages from the MQTT broker.
        :param delay_ms: The delay in milliseconds between message checks.
        :return:
        """
        self.running = True

        while self.running:
            if self.connected:
                try:
                    self.client.check_msg()
                except OSError as error:
                    print("MQTT listen error:", error)

            await asyncio.sleep_ms(delay_ms)

    def publish(self, topic, message):
        """
        Publishes a message to a specified topic.

        :param topic: The topic to publish the message to.
        :param message: The message to be sent to the specified topic.
        """
        if message is None:
            payload = None

        elif isinstance(message, str):
            payload = message.encode()

        elif isinstance(message, bool):
            payload = str(message).encode()

        elif isinstance(message, (bytes, bytearray)):
            payload = message

        elif isinstance(message, (int, float)):
            payload = str(message).encode()

        elif isinstance(message, (list, tuple)):
            payload = ",".join(map(str, message)).encode()

        elif isinstance(message, dict):
            import json
            payload = json.dumps(message).encode()

        else:
            raise TypeError(
                f"Unsupported MQTT payload type: {type(message).__name__}"
            )

        print("Publishing to topic:", topic, "with payload:", payload)

        self.client.publish(topic, payload)

    def stop(self):
        """
        Stop listening for incoming messages.
        """
        self.running = False

    def disconnect(self):
        """
        Disconnect from the MQTT broker.
        """
        self.stop()
        self.connected = False
        self.client.disconnect()