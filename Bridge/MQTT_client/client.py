# client.py

from configparser import ConfigParser

import paho.mqtt.client as mqtt


class MQTTClient:
    def __init__(self, bridge=None):
        """
        Initializes the MQTT client.
        """
        self.config = ConfigParser()
        self.config.read('config.ini')
        self.bridge = bridge
        self.clientMQTT = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.clientMQTT.on_connect = self.on_connect
        self.clientMQTT.on_message = self.on_message
        self.server_address = self.config.get("MQTT", "Server", fallback="localhost")
        self.server_port = self.config.getint("MQTT", "Port", fallback=1883)
        self.clientMQTT.connect(self.server_address, self.server_port, 60)
        self.topic = self.config.get("MQTT", "Topicc", fallback="alerts")
        self.clientMQTT.loop_start()

    def on_connect(self, client, userdata, flags, rc, *args, **kwargs):
        """
        Callback function for when the client connects to the MQTT broker.
        """
        self.clientMQTT.subscribe(self.topic)
        print("Subscribed to " + self.topic)

    def on_message(self, client, userdata, message):
        """
        Callback function for when a message is received.
        """
        self.bridge.handle_alert(message.payload)

    def publish(self, payload):
        """
        Publishes a message to the MQTT broker.
        """
        self.clientMQTT.publish(self.topic, payload)

    def disconnect(self):
        """
        Disconnects the MQTT client from the broker.
        """
        self.clientMQTT.disconnect()

    def subscribe(self):
        """
        Subscribes the MQTT client to the specified topic.
        """
        self.clientMQTT.subscribe(self.topic)
