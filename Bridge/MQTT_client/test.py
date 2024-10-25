from MQTT_client.client import MQTTClient

if __name__ == "__main__":
    mqtt_client = MQTTClient()

    # Esempio di pubblicazione di un messaggio
    mqtt_client.publish("Hello MQTT!")
