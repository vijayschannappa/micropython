import snrm_frame_construction as snrm
import aaqr_frame_construction as aarq
import serial_initialization

import binascii
import time
WAIT_SECONDS = 1


def write_and_read(serial_con, hex_input):
    try:
        to_send = binascii.unhexlify(hex_input.replace(' ', ''))
        serial_con.write(to_send)
        time.sleep(WAIT_SECONDS)
        byte_array = serial_con.read()
        raw_hex_value = binascii.hexlify(byte_array).decode()
        time.sleep(0.2)
        return raw_hex_value

    except Exception as Error:
        print(Error)
        pass


def hand_shake():
    connection = serial_initialization.new_serial_connection()
    value = snrm.snrm_frame_construction()
    value_1 = aarq.aarq_frame_generation()
    values = [value, value_1]
    for value in values:
        write_and_read(connection, value)


def send_data(parameters_frame):
    hand_shake()
    connection = serial_initialization.new_serial_connection()
    Meter_Read_Data = write_and_read(connection, parameters_frame)
    if Meter_Read_Data:
        value_decimal = Meter_Read_Data
    else:
        value_decimal = 'DLMS_ERROR'
    return value_decimal


def read_load_survey_data(load_ip_1, load_ip_2, load_data):
    hand_shake()
    connection = serial_initialization.new_serial_connection()
    write_and_read(connection, load_ip_1)
    write_and_read(connection, load_ip_2)
    Meter_Read_Data = write_and_read(connection, load_data)
    return Meter_Read_Data

