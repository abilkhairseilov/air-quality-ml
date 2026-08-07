import serial

import struct
import time

PORT = "/dev/serial0"

with serial.Serial(PORT, 9600, timeout=2) as ser:
    while True:
        # Synchronize to the 0x42 0x4D frame header.
        if ser.read(1) != b"\x42":
            continue
        if ser.read(1) != b"\x4d":
            continue

        rest = ser.read(30)
        if len(rest) != 30:
            continue

        frame = b"\x42\x4d" + rest
        expected_checksum = int.from_bytes(frame[-2:], "big")
        calculated_checksum = sum(frame[:-2])

        if calculated_checksum != expected_checksum:
            print("Checksum failure")
            continue

        values = struct.unpack(">13H", frame[4:30])

        pm1_atm = values[3]
        pm25_atm = values[4]
        pm10_atm = values[5]

        print(
            f"PM1.0={pm1_atm:3d} µg/m³  "
            f"PM2.5={pm25_atm:3d} µg/m³  "
            f"PM10={pm10_atm:3d} µg/m³"
        )

        time.sleep(1)
