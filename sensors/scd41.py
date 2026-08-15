#!/usr/bin/env python3
from time import sleep

from smbus2 import SMBus, i2c_msg

# some constants
I2C_ADDR = 0x62

# https://sensirion.com/media/documents/E0F04247/631EF271/CD_DS_SCD40_SCD41_Datasheet_D1.pdf
# 3.4 lists all the hex codes needed for a command. we simply have to establish some constants for them
CMD_START_PERIODIC = [0x21, 0xB1]
CMD_STOP_PERIODIC = [0x3F, 0x86]
CMD_READ_MEASUREMENT = [0xEC, 0x05]
CMD_SINGLE_SHOT = [0x21, 0x9D]


class SCD41:
    def sensirion_common_generate_crc(self, data: list[int]) -> int:
        """
        Function to generate a CRC checksum for Sensirion devices.
        Takes a list of integers, and outputs an integer.
        """
        crc = 0xFF
        for byte in data:
            crc ^= byte
            for _ in range(8):
                crc = crc << 1 ^ 49 if crc & 128 else crc << 1

        return crc

    def single_shot(self):
        with SMBus(1) as bus:
            try:
                write_frame = i2c_msg.write(I2C_ADDR, CMD_SINGLE_SHOT)
                bus.i2c_rdwr(write_frame)
            except Exception as error:
                print(f"single_shot failed: {error}")

    def start_measurement(self):
        with SMBus(1) as bus:
            try:
                write_frame = i2c_msg.write(I2C_ADDR, CMD_START_PERIODIC)
                bus.i2c_rdwr(write_frame)
            except Exception as error:
                print(f"start_measurement failed: {error}")

    def stop_measurement(self):
        with SMBus(1) as bus:
            try:
                write_frame = i2c_msg.write(I2C_ADDR, CMD_STOP_PERIODIC)
                bus.i2c_rdwr(write_frame)
            except Exception as error:
                print(f"stop_measurement failed: {error}")

    def read_measurement(self, verbose: bool = False):
        with SMBus(1) as bus:
            write_frame = i2c_msg.write(I2C_ADDR, CMD_READ_MEASUREMENT)
            bus.i2c_rdwr(write_frame)

            sleep(1)

            read_frame: i2c_msg = i2c_msg.read(I2C_ADDR, 9)
            bus.i2c_rdwr(read_frame)

            data_bytes: list[int] = list(read_frame)  # pyright: ignore[reportArgumentType, reportUnknownVariableType]

            _ = (
                print(f"Printing raw bytes:{[hex(num) for num in data_bytes]}")
                if verbose
                else None
            )

            # will skip CRC verification for now
            co2_list = data_bytes[0:2]
            temp_list = data_bytes[3:5]
            humidity_list = data_bytes[6:8]

            raw_co2 = (co2_list[0] << 8) | co2_list[1]
            raw_temp = (temp_list[0] << 8) | temp_list[1]
            raw_humidity = (humidity_list[0] << 8) | humidity_list[1]

            # Signal conversions
            co2_ppm = raw_co2
            temperature_c = -45 + 175 * raw_temp / (2**16 - 1)
            humidity = 100 * raw_humidity / (2**16 - 1)

            if verbose:
                print(f"CO_2 ppm: {co2_ppm}")
                print(f"Temperature (C): {temperature_c}")
                print(f"Humidity: {humidity}")

            return (co2_ppm, temperature_c, humidity)


if __name__ == "__main__":
    scd41 = SCD41()
    scd41.stop_measurement()
    scd41.single_shot()

    sleep(5)
    _ = scd41.read_measurement(verbose=True)

    print("PROGRAM END\n")
