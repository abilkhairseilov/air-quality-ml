#!/usr/bin/env python3
from smbus2 import SMBus, i2c_msg
from time import sleep

# some constants
I2C_ADDR = 0x62

# https://sensirion.com/media/documents/E0F04247/631EF271/CD_DS_SCD40_SCD41_Datasheet_D1.pdf
# 3.4 lists all the hex codes needed for a command. we simply have to establish some constants for them
CMD_START_PERIODIC = [0x21, 0xB1]
CMD_STOP_PERIODIC = [0x36, 0x15]
CMD_READ_MEASUREMENT = [0xEC, 0x05]


def sensirion_common_generate_crc(data: list[int]) -> int:
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


def start_measurement():
    with SMBus(1) as bus:
        try:
            write_frame = i2c_msg.write(I2C_ADDR, CMD_START_PERIODIC)
            bus.i2c_rdwr(write_frame)
        except Exception as error:
            print(f"Start_measurement failed: {error}")


def stop_measurement():
    with SMBus(1) as bus:
        try:
            write_frame = i2c_msg.write(I2C_ADDR, CMD_STOP_PERIODIC)
            bus.i2c_rdwr(write_frame)
        except Exception as error:
            print(f"Start_measurement failed: {error}")


def read_measurement():
    with SMBus(1) as bus:
        write_frame = i2c_msg.write(I2C_ADDR, CMD_READ_MEASUREMENT)
        print("create write_frame:", write_frame)
        bus.i2c_rdwr(write_frame)
        print("write_frame sent.")

        sleep(1)
        print("Sleep passed.")

        read_frame = i2c_msg.read(I2C_ADDR, 9)
        print("create read_frame:", read_frame)
        bus.i2c_rdwr(read_frame)
        print("read_frame sent.")

        data_bytes = list(read_frame)
        print(data_bytes)

        # will skip CRC verification for now
        co2_result = data_bytes[0:2]
        temp_result = data_bytes[3:5]
        humidity_result = data_bytes[6:8]

        raw_co2 = (co2_result[0] << 8) | co2_result[1]
        raw_temp = (temp_result[0] << 8) | temp_result[1]
        raw_humidity = (humidity_result[0] << 8) | humidity_result[1]

        co2_ppm = raw_co2
        temperature_c = -45 + 175 * raw_temp / (2**16 - 1)
        humidity = 100 * raw_humidity / (2**16 - 1)

        result = list([co2_ppm, temperature_c, humidity])
        print(result)

        return result


if __name__ == "__main__":
    start_measurement()

    sleep(10)

    read_measurement()

    sleep(1)

    stop_measurement()
