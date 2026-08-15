import struct

import serial

PORT = "/dev/serial0"


class PMS5003:
    def __init__(self) -> None:
        self.ser: serial.Serial = serial.Serial(PORT, 9600, timeout=2)

    def read_measurement(self, samples: int = 5) -> tuple[float, float, float]:
        """
        Takes samples of measurements and returns the average of all samples taken.
        Takes an integer and returns a tuple with these measurements in order: PM_1, PM2.5, and PM_10.
        """
        pm1 = []
        pm25 = []
        pm10 = []

        for i in range(samples):
            data = self._read_frame()

            pm1.append(data[0])
            pm25.append(data[1])
            pm10.append(data[2])

        return (sum(pm1) / samples, sum(pm25) / samples, sum(pm10) / samples)

    def _read_frame(self):
        while True:
            # Synchronize to the 0x42 0x4D frame header.
            if self.ser.read(1) != b"\x42":
                continue
            if self.ser.read(1) != b"\x4d":
                continue

            rest = self.ser.read(30)
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

            return (pm1_atm, pm25_atm, pm10_atm)


if __name__ == "__main__":
    # some testing

    pms = PMS5003()

    print(pms.read_measurement())
