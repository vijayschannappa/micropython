import time
import sys
import upload_store
import binascii
from initialization import *
import write_read as data_read
from crc_calculation import crc_calculation
from zero_padding import zero_pad


def frame_length(obis_code):
    length = hex((int((len(str(FRAME_TYPE + DESTINATION_ADDRESS + SOURCE_ADDRESS + CONTROL_FIELD_FRAME + LLC
                           + READ_REQUEST + REQUEST_NUMBER + INVOKE_ID +
                           OBIS_CLASS + obis_code + ATTRIBUTE_1
                           + ATTRIBUTE_2).replace(' ', '')) + 10) / 2))).replace('0x', '')
    aarq_frame_length = zero_pad(length, 2)
    return aarq_frame_length


def get_fsc_calculation_string(f_length, hcs, obis_code):
    fsc = str(FRAME_TYPE + f_length + DESTINATION_ADDRESS + SOURCE_ADDRESS + CONTROL_FIELD_FRAME + hcs + LLC
              + READ_REQUEST + REQUEST_NUMBER + INVOKE_ID +
              OBIS_CLASS + obis_code + ATTRIBUTE_1
              + ATTRIBUTE_2).replace(' ', '')
    return fsc


def parameters_frame_generation(f_length, hcs, obis_code, fsc):
    aarq_frame = str(START_END_FLAG + FRAME_TYPE + f_length + DESTINATION_ADDRESS + SOURCE_ADDRESS
                     + CONTROL_FIELD_FRAME + hcs + LLC + READ_REQUEST +
                     REQUEST_NUMBER + INVOKE_ID + OBIS_CLASS
                     + obis_code + ATTRIBUTE_1 + ATTRIBUTE_2 + fsc + START_END_FLAG).replace(' ', '')
    return aarq_frame


def read_serial_number(data_frame,lsp):
    try:
        slice_ratio = lsp["METER_SL_SLICE"]
        First_Slice_Value = slice_ratio.split(':')[0]
        Second_Slice_Value = slice_ratio.split(':')[1]
        #data_frame = '7EA0190341986AB7E6E600C001C100010000600100FF020089A07E'
        #print(First_Slice_Value,Second_Slice_Value)
        for error_count in range(3):
            Meter_Read_Data = data_read.send_data(data_frame,lsp)
            print("Mtr_read_data:{}".format(Meter_Read_Data))
            string_length = (int(Meter_Read_Data[4:6], 16) * 2 + 4)
            if len(Meter_Read_Data) == string_length:
                value_split = Meter_Read_Data[-int(First_Slice_Value):-int(Second_Slice_Value)]
                value_decimal = binascii.unhexlify(value_split).decode()
                break
            else:
                time.sleep(0.3)
            value_decimal = 'DLMS_ERROR'
    except Exception as error:
        print(error)
        value_decimal = 'DLMS_ERROR'
    return value_decimal


def read_time_stamp(data_frame,lsp):
    try:
        for error_count in range(3):
            Meter_Read_Data = data_read.send_data(data_frame,lsp)
            string_length = (int(Meter_Read_Data[4:6], 16) * 2 + 4)
            value_decimal = get_zero_padded_timestamp(
                Meter_Read_Data, string_length)
            if value_decimal == 'DLMS_ERROR':
                time.sleep(0.3)
                continue
            else:
                return value_decimal
    except Exception as error:
        print(error)
        value_decimal = 'DLMS_ERROR'
    return value_decimal


def get_zero_padded_timestamp(Meter_Read_Data, string_length):
    global coded_year_val
    if len(Meter_Read_Data) == string_length:
        value_split = Meter_Read_Data[-30:-14]
        coded_year_val = zero_pad(str(value_split[1:4]), 4)
        try:
            value_decimal = (zero_pad(str(int(value_split[1:4], 16)), 4) + '-' +
                             zero_pad(str(int(value_split[4:6], 16)), 2) + '-' +
                             zero_pad(str(int(value_split[6:8], 16)), 2) + ' ' +
                             zero_pad(str(int(value_split[10:12], 16)), 2) + ':' +
                             zero_pad(str(int(value_split[12:14], 16)), 2) + ':' +
                             zero_pad(str(int(value_split[14:16], 16)), 2))
        except ValueError as error:
            print('zero padding error')
            print(error)
            sys.exit()
    else:
        value_decimal = 'DLMS_ERROR'
    return value_decimal


def read_instantaneous_parameters(data_frame,lsp):
    try:
        for error_count in range(3):
            Meter_Read_Data = data_read.send_data(data_frame,lsp)
            string_length = (int(Meter_Read_Data[4:6], 16) * 2 + 4)
            value_decimal = get_instantaneous_val(
                Meter_Read_Data, string_length)
            if value_decimal == 'DLMS_ERROR':
                time.sleep(0.3)
                continue
            else:
                return value_decimal
    except Exception as error:
        print(error)
    value_decimal = error
    return value_decimal


def get_instantaneous_val(Meter_Read_Data, string_length):
    if len(Meter_Read_Data) == string_length and len(Meter_Read_Data) == 42:
        value_decimal = Meter_Read_Data[-10:-6]  # -14 -6
    elif len(Meter_Read_Data) == string_length and len(Meter_Read_Data) == 46:
        value_decimal = Meter_Read_Data[-14:-6]  # -14 -6
    else:
        value_decimal = 'DLMS_ERROR'
    return value_decimal


def obis_code_generation(lsp):
    final_dict = {}
    try:
        for param in lsp["PARAMETERS"]:
            print(param)
            read_vals = param.split('=')
            param_name = read_vals[0].replace(" ","")
            param_vals = read_vals[1].split('.')
            obis_code = get_obis_code(param_vals)
            f_length = frame_length(obis_code)
            hcs = crc_calculation(str(FRAME_TYPE + f_length + DESTINATION_ADDRESS + SOURCE_ADDRESS
                                      + CONTROL_FIELD_FRAME))
            fsc_calculation_string = get_fsc_calculation_string(
                f_length, hcs, obis_code)
            fsc = crc_calculation(fsc_calculation_string)
            data_frame = parameters_frame_generation(
                f_length, hcs, obis_code, fsc)
            data = get_data(param_name, data_frame,lsp)
            final_dict[param_name] = data
        print("pushing_final_dict:{}".format(final_dict))
        upload_store.upload_data(final_dict,"rt_data")
        return meter_sl_num,meter_time,coded_year_val
    except Exception as error:
        print(error)
    

def get_obis_code(param_vals):
    obis_code = ''
    for vals in param_vals:
        _obis_code = hex(int(vals)).replace('0x', '')
        hex_code = zero_pad(_obis_code, 2)
        obis_code += hex_code
    #print("obis code:{}".format(obis_code))
    return obis_code


def get_data(param, data_frame,lsp):
    global meter_sl_num, meter_time
    if param == 'SL_NUM':
        #print("sl_df:{}".format(data_frame))
        read_data = read_serial_number(data_frame,lsp)
        meter_sl_num = read_data
    elif param == 'T':
        read_data = read_time_stamp(data_frame,lsp)
        meter_time = read_data
    else:
        read_data = read_instantaneous_parameters(data_frame,lsp)

    return read_data


if __name__ == '__main__':
    obis_code_generation(lsp=None)
