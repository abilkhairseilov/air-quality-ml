#!/usr/bin/env python3
from smbus2 import SMBus, i2c_msg

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


_ = i2c_msg.write(I2C_ADDR, CMD_READ_MEASUREMENT)
