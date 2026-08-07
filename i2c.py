#!/usr/bin/env python3
from smbus2 import SMBus, i2c_msg

# some constants
I2C_ADDR = 0x62

# https://sensirion.com/media/documents/E0F04247/631EF271/CD_DS_SCD40_SCD41_Datasheet_D1.pdf
# 3.4 lists all the hex codes needed for a command. we simply have to establish some constants for them
CMD_START_PERIODIC  = [0x21, 0xB1]
CMD_STOP_PERIODIC   = [0x36, 0x15]
CMD_READ_MEASUREMENT = [0xEC, 0x05]

#define CRC8_POLYNOMIAL 0x31
#define CRC8_INIT 0xFF
# uint8_t sensirion_common_generate_crc(const uint8_t* data, uint16_t count) {
# uint16_t current_byte;
# uint8_t crc = CRC8_INIT;
# uint8_t crc_bit;
# /* calculates 8-Bit checksum with given polynomial */
# for (current_byte = 0; current_byte < count; ++current_byte) {
# crc ^= (data[current_byte]);
# for (crc_bit = 8; crc_bit > 0; --crc_bit) {
# if (crc & 0x80)
# crc = (crc << 1) ^ CRC8_POLYNOMIAL;
# else
# crc = (crc << 1);
# }
# }
# return crc;
# }

def sensirion_common_generate_crc(data: list) -> int {
    '''
    Function to generate a CRC checksum for Sensirion devices.
    Takes a list of data, and outputs an integer.
    '''
    crc = 0xff
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x80:
                crc = (crc << 1) ^ 0x31
            else:
                crc = (crc << 1)

    return crc
}

# def read_data():
