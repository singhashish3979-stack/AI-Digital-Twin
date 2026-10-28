import paho.mqtt.client as mqtt
import json
import os

BROKER = "m4410441.ala.eu-central-1.emqxsl.com"
PORT = 8883

USERNAME = os.getenv("MQTT_USERNAME", "digitaltwin")
PASSWORD = os.getenv("MQTT_PASSWORD", "")
TOPIC = "factory/machine1/data"

LIVE_FILE = "live_data.json"


def on_connect(client, userdata, flags, reason_code, properties):
    print("CONNECTED")
    print("Connect reason:", reason_code)

    if reason_code == 0:
        print("SUBSCRIBING...")
        result, mid = client.subscribe(TOPIC, qos=0)
        print("Subscribe result:", result)
        print("Message ID:", mid)


def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())

        print("MESSAGE RECEIVED:")
        print(data)

        with open(LIVE_FILE, "w") as file:
            json.dump(data, file)

        print("Saved to live_data.json")

    except Exception as e:
        print("ERROR:", e)


client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    protocol=mqtt.MQTTv311
)

client.username_pw_set(USERNAME, PASSWORD)
client.tls_set()

client.on_connect = on_connect
client.on_message = on_message

print("STARTING RECEIVER...")

client.connect(BROKER, PORT, 60)

client.loop_forever()