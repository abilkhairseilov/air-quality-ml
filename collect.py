import csv
import os
import time
from datetime import datetime

from sensors.pms5003 import PMS5003
from sensors.scd41 import SCD41

CSV_PATH = "dataset.csv"

FIELDS = [
    "timestamp",
    "co2_ppm",
    "temperature_c",
    "humidity_pct",
    "pm1_ugm3",
    "pm25_ugm3",
    "pm10_ugm3",
]


def ensure_csv_exists():
    if not os.path.exists(CSV_PATH):
        with open(CSV_PATH, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()


def main():
    ensure_csv_exists()

    scd41 = SCD41()
    pms5003 = PMS5003()

    scd41.stop_measurement()
    scd41.start_measurement()

    time.sleep(5)

    try:
        with open(CSV_PATH, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)

            while True:
                co2, temperature, humidity = scd41.read_measurement()
                pm1, pm25, pm10 = pms5003.read_measurement()

                row = {
                    "timestamp": datetime.now().astimezone().isoformat(),
                    "co2_ppm": co2,
                    "temperature_c": temperature,
                    "humidity_pct": humidity,
                    "pm1_ugm3": pm1,
                    "pm25_ugm3": pm25,
                    "pm10_ugm3": pm10,
                }

                writer.writerow(row)
                f.flush()

                time.sleep(30)

    except KeyboardInterrupt:
        print("Stopping collection...")

    finally:
        scd41.stop_measurement()


if __name__ == "__main__":
    main()
