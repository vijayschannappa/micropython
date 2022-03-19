from aaqr_frame_construction import *
import write_read as data_read
from initialization import *
from meter_data_read import *
import upload_store
import zero_padding
import binascii
import json
import time

def frame_length(obis_code):
    length = hex((int((len(str(FRAME_TYPE + DESTINATION_ADDRESS + SOURCE_ADDRESS + CONTROL_FIELD_FRAME + LLC
                               + READ_REQUEST + REQUEST_NUMBER + INVOKE_ID + OBIS_CLASS + obis_code + ATTRIBUTE_1
                               + ATTRIBUTE_2).replace(' ', '')) + 10) / 2))).replace('0x', '')
    
        
    aarq_frame_length = zero_padding.zero_pad(length,2)
    return aarq_frame_length


def fsc_calculation_string(f_length, hcs, obis_code):
    fsc = str(FRAME_TYPE + f_length + DESTINATION_ADDRESS + SOURCE_ADDRESS + CONTROL_FIELD_FRAME + hcs + LLC
              + READ_REQUEST + REQUEST_NUMBER + INVOKE_ID + OBIS_CLASS + obis_code + ATTRIBUTE_1
              + ATTRIBUTE_2).replace(' ', '')
    return fsc


def parameters_frame_generation(f_length, hcs, obis_code, fsc):
    aarq_frame = str(START_END_FLAG + FRAME_TYPE + f_length + DESTINATION_ADDRESS + SOURCE_ADDRESS
                     + CONTROL_FIELD_FRAME + hcs + LLC + READ_REQUEST + REQUEST_NUMBER + INVOKE_ID + OBIS_CLASS
                     + obis_code + ATTRIBUTE_1 + ATTRIBUTE_2 + fsc + START_END_FLAG).replace(' ', '')
    return aarq_frame


def read_serial_number(data_frame):
    global value_decimal
    try:
        with open("data.json", "r") as data:
            string = json.load(data)
            for para in string["METER_SERIAL_NUMBER_SLICE"]:
            #print(para.split())
                Read_Values = para.split('=')
                First_Slice_Value = Read_Values[1].split(':')[0]
                Second_Slice_Value = Read_Values[1].split(':')[1]

            for error_count in range(3):
                Meter_Read_Data = data_read.send_data(data_frame)
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


def read_time_stamp(data_frame):
    global value_decimal
    global meter_time_load_servey
    try:
        for error_count in range(3):
            Meter_Read_Data = data_read.send_data(data_frame)
            string_length = (int(Meter_Read_Data[4:6], 16) * 2 + 4)
            if len(Meter_Read_Data) == string_length:
                value_split = Meter_Read_Data[-30:-14]  # -14 -6
                try:
                    meter_time_load_servey = zero_padding.zero_pad(str(value_split[1:4]),4)
                    value_decimal = (zero_padding.zero_pad(str(int(value_split[1:4], 16)),4) + '-' +
                                     zero_padding.zero_pad(str(int(value_split[4:6], 16)),2)+ '-' +
                                     zero_padding.zero_pad(str(int(value_split[6:8], 16)),2) + ' ' +
                                     zero_padding.zero_pad(str(int(value_split[10:12], 16)),2) + ':' +
                                     zero_padding.zero_pad(str(int(value_split[12:14], 16)),2) + ':' +
                                     zero_padding.zero_pad(str(int(value_split[14:16], 16)),2))
                except ValueError as error:
                    print(error)
                break
            else:
                time.sleep(0.3)
            value_decimal = 'DLMS_ERROR'
    except Exception as error:
        print(error)
        value_decimal = 'DLMS_ERROR'
    return value_decimal


def read_instantaneous_parameters(data_frame):
    global value_decimal
    try:
        for error_count in range(3):
            Meter_Read_Data = data_read.send_data(data_frame)
            string_length = (int(Meter_Read_Data[4:6], 16) * 2 + 4)
            if len(Meter_Read_Data) == string_length:
                if len(Meter_Read_Data) == 42:
                    value_decimal = Meter_Read_Data[-10:-6]  # -14 -6
                    break
                elif len(Meter_Read_Data) == 46:
                    value_decimal = Meter_Read_Data[-14:-6]  # -14 -6
                    break
            else:
                time.sleep(0.3)
            value_decimal = 'DLMS_ERROR'
    except Exception as error:
        print(error)
        value_decimal = 'DLMS_ERROR'
    return value_decimal


def obis_code_generation():
    try:
        with open("data.json", "r") as data:
            string = json.load(data)
            final_data = ''
            upload_final_data = ''
            for para in string["PARAMETERS"]:
                Read_Values = para.split('=')
                parameters_name = Read_Values[0].replace(' ', '')
                Read_value_data = Read_Values[1].split('.')
                obis_code = ''
                for parameter in Read_value_data:
                    password = hex(int(parameter)).replace('0x', '')
                    psw = zero_padding.zero_pad(password,2)
                    obis_code += psw
                f_length = frame_length(obis_code)
                hcs = crc_calculation(str(FRAME_TYPE + f_length + DESTINATION_ADDRESS + SOURCE_ADDRESS
                + CONTROL_FIELD_FRAME))
                fsc = crc_calculation(fsc_calculation_string(f_length, hcs, obis_code))
                data_frame = parameters_frame_generation(f_length, hcs, obis_code, fsc).upper()
                if parameters_name == 'SERIAL_NUMBER':
                    Read_Data = read_serial_number(data_frame)
                    Meter_Serial_Number = Read_Data
                elif parameters_name == 'TIME':
                    Read_Data = read_time_stamp(data_frame)
                    Meter_Time = Read_Data
                else:
                    Read_Data = read_instantaneous_parameters(data_frame)
                final_data += parameters_name + '=' + Read_Data + ','
                upload_final_data += Read_Data + ' '

                
                instant_values = (
                MAC_ADDRESS,
                upload_final_data[:-1],
                )
            instant_values_str = " ".join(instant_values)
            upload_store.upload_and_store(instant_values_str, data_type="instant")
            
        return Meter_Serial_Number, Meter_Time, meter_time_load_servey
    except Exception as error:
        print(error)


