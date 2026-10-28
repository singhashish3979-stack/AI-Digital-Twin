import csv
import random
import time
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent
CSV_FILE = BASE_DIR / "machine_data.csv"

HEADERS = ["timestamp", "temperature", "vibration", "rpm", "pressure"]

if not CSV_FILE.exists() or CSV_FILE.stat().st_size == 0:
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(HEADERS)

print("Smart Factory Simulator Started")
print("Generating new readings every 2 seconds.")
print("Press Ctrl+C to stop.")

try:
    while True:
        data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "temperature": round(random.uniform(50, 85), 2),
            "vibration": round(random.uniform(1, 4.5), 2),
            "rpm": random.randint(1200, 1800),
            "pressure": round(random.uniform(3, 6), 2),
        }

        with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=HEADERS)
            writer.writerow(data)

        print("New reading:", data)
        time.sleep(2)

except KeyboardInterrupt:
    print("\nSimulator stopped.")
