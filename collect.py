import csv
import os
import time
import tomllib
from datetime import datetime

from sensors.pms5003 import PMS5003
from sensors.scd41 import SCD41

FIELDS = [
    "timestamp",
    "co2_ppm",
    "temperature_c",
    "humidity_pct",
    "pm1_ugm3",
    "pm25_ugm3",
    "pm10_ugm3",
    "event",
]


def load_config(path="config.toml"):
    with open(path, "rb") as f:
        return tomllib.load(f)


def ensure_csv_exists(csv_path):
    if not os.path.exists(csv_path):
        with open(csv_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()


def main():
    config = load_config()

    collection = config["collection"]
    logging = config["logging"]

    CSV_PATH = collection["output"]
    INTERVAL = collection["interval_seconds"]
    VERBOSE = logging["verbose"]

    ensure_csv_exists(CSV_PATH)

    print(f"Writing to path {CSV_PATH} with interval {INTERVAL}")

    scd41 = SCD41()
    pms5003 = PMS5003()

    scd41.stop_measurement()
    scd41.start_measurement()

    # 5 second wait required to start measuring
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
                    "event": "",
                }

                writer.writerow(row)
                f.flush()

                _ = print(row) if VERBOSE else None

                time.sleep(INTERVAL)

    except KeyboardInterrupt:
        print(f"Stopping collection to file {CSV_PATH}")

    finally:
        scd41.stop_measurement()


if __name__ == "__main__":
    # config = load_config()
    # print(config)
    main()
