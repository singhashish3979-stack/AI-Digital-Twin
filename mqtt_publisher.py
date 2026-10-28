
import json
import time
import pandas as pd
import paho.mqtt.client as mqtt

BROKER = "YOUR_EMQX_BROKER_HOST"
PORT = 8883
import os

USERNAME = os.getenv("MQTT_USERNAME", "digitaltwin")
PASSWORD = os.getenv("MQTT_PASSWORD", "")
TOPIC = "factory/machine1/data"
CSV_FILE = "machine_data.csv"

client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    protocol=mqtt.MQTTv311
)
client.username_pw_set(USERNAME, PASSWORD)
client.tls_set()

print("Connecting to EMQX...")
client.connect(BROKER, PORT, 60)
client.loop_start()

try:
    df = pd.read_csv(CSV_FILE)

    while True:
        for _, row in df.iterrows():
            data = {
                "temperature": float(row["temperature"]),
                "vibration": float(row["vibration"]),
                "rpm": float(row["rpm"]),
                "pressure": float(row["pressure"])
            }

            info = client.publish(TOPIC, json.dumps(data), qos=1)
            info.wait_for_publish()
            print("Published:", data)
            time.sleep(2)

except KeyboardInterrupt:
    print("\nPublisher stopped.")

finally:
    client.loop_stop()
    client.disconnect()
