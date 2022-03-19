import re
import write_read
import upload_store
import zero_padding
from initialization import *
from crc_calculation import crc_calculation
import time
import time_calculation as tm
params = ["07e4", "07e5", "07e6", "07e7", "07e8", "07e9", "07ea", "07eb", "07ec", "07ed", "07ee", "07ef", "07f0", "07f1", "07f2"]


def year_conversion(value):
    decimal_to_hex = hex(int(value)).replace("0x", "")
    decimal_to_hex_format = zero_padding.zero_pad(decimal_to_hex,4)
    return decimal_to_hex_format


def date_time_conversion(value):
    decimal_to_hex = hex(int(value)).replace("0x", "")
    decimal_to_hex_format = zero_padding.zero_pad(decimal_to_hex,2)
    return decimal_to_hex_format


def fsc_calculation_string(start_year, start_month, start_day, start_hour, start_minute, start_seconds, end_year,
                           end_month, end_day, end_hour, end_minute, end_seconds):
    fsc = str(STARTING_FRAME + LOAD_PROFILE_IP + THIRD_FRAME + start_year + start_month + start_day +
              START_END_SEPARATOR + start_hour + start_minute + start_seconds + FIRST_FRAME_LENGTH + end_year +
              end_month + end_day + START_END_SEPARATOR + end_hour + end_minute + end_seconds
              + SECOND_FRAME_LENGTH).replace(" ", "")
    return fsc


def get_start_and_end_time():
    try:
        Start_Time = open('Start_Time.txt','r')
        data = Start_Time.read()
        Start_Time.close()
        return data
    except Exception as Error:
        print(Error)


def get_load_survey_time():
    try:
        Start_Time = open('Start_Time_Backup.txt','r')
        data = Start_Time.read()
        Start_Time.close()
        return data
    except Exception as Error:
        print(Error)


def decode_load_survey_data(Serial_Number, Meter_Load_Data, start, Add_time):
#     print(Serial_Number, Meter_Load_Data, start, Add_time)
    global find_year
    for year in params:
        if year in Meter_Load_Data:
            find_year = year
        else:
            pass
    Meter_Load_Data = Meter_Load_Data.split(find_year)
    Energy = int(Meter_Load_Data[1][22:26], 16)
    R_Energy = int(Meter_Load_Data[1][28:32], 16)
    Voltage = int(Meter_Load_Data[1][34:38], 16)
    Time_Stamp = (str(zero_padding.zero_pad(str(int(find_year, 16)),4)) + '-' +
                  str(zero_padding.zero_pad(str(int(Meter_Load_Data[1][0:2], 16)),2)) + '-' +
                  str(zero_padding.zero_pad(str(int(Meter_Load_Data[1][2:4], 16)),2)) + ' ' +
                  str(zero_padding.zero_pad(str(int(Meter_Load_Data[1][6:8], 16)),2)) + ':' +
                  str(zero_padding.zero_pad(str(int(Meter_Load_Data[1][8:10], 16)),2)) + ':' +
                  str('00'))

    instant_values = (
        MAC_ADDRESS,
        str(Serial_Number),
        str(Voltage),
        str(R_Energy),
        str(Energy),
        str(Time_Stamp),
    )
    value_str = ",".join(instant_values)
    


    if str(start) == str(Time_Stamp):
        upload_store.upload_and_store(value_str, data_type="load_survey")
        start_time = Time_Stamp.replace(':', '').replace('-', '').replace(' ', '')
        Store_Last_Meter_Data_Fetch_Time = tm.calculate_add_time(start_time, int(Add_time))
        f=open('Start_Time.txt','w')
        f.write(str(Store_Last_Meter_Data_Fetch_Time))
        f.close()
        f=open('Start_Time_Backup.txt','w')
        f.write(str(Store_Last_Meter_Data_Fetch_Time))
        f.close()

    else:
        print('wrong time=', start)
        f=open('Start_Time.txt','w')
        f.write(str(start))
        f.close()

def no_load_survey_data_time_store(start, Add_time):
    start_time = start.replace(':', '').replace('-', '').replace(' ', '')
    start_time = tm.calculate_add_time(start_time, int(Add_time))
    f=open('Start_Time.txt','w')
    f.write(str(start_time))
    f.close()


def pull_load_survey_data(Serial_Number, meter_time, Add_time, Difference_Time):  # meter_time
    try:
        for error_count in range(3):
            try:
                start_time_from_memory = get_start_and_end_time()
                start_time = start_time_from_memory.replace(':', '').replace('-', '').replace(' ', '')
            except AttributeError:
                store_time = get_load_survey_time()
                try:
                    start_time = store_time.replace(':', '').replace('-', '').replace(' ', '')
                    f=open('Start_Time.txt','w')
                    f.write(str(start_time))
                    f.close()
                except AttributeError:
                    store_time = str(meter_time[0:4] + '-' + meter_time[5:7] + '-'
                                     + meter_time[8:10] + ' ' + meter_time[11:13]
                                     + ':00' + ':00')
                    f=open('Start_Time_Backup.txt','w')
                    f.write(str(store_time))
                    f.close()

            end_time = str(meter_time).replace(':', '').replace('-', '').replace(' ', '')

            if str(start_time) > str(end_time):
                store_time = get_load_survey_time()
                try:
                    f=open('Start_Time.txt','w')
                    f.write(str(store_time))
                    f.close()
                except AttributeError:
                    store_time = str(meter_time[0:4] + '-' + meter_time[5:7] + '-'
                                     + meter_time[8:10] + ' ' + meter_time[11:13]
                                     + ':00' + ':00')
                    f=open('Start_Time_Backup.txt','w')
                    f.write(str(store_time))
                    f.close()

            if tm.calculate_start_end_minus_time(start_time, 0) <= tm.calculate_start_end_minus_time(end_time, 32):
                end_time_now = tm.calculate_add_time(start_time, 29)
                end_time = str(end_time_now).replace(':', '').replace('-', '').replace(' ', '')
                print(start_time, end_time)

                start_year = year_conversion(start_time[0:4])
                start_month = date_time_conversion(start_time[4:6])
                start_day = date_time_conversion(start_time[6:8])
                start_hour = date_time_conversion(start_time[8:10])
                start_minute = date_time_conversion(start_time[10:12])
                start_seconds = date_time_conversion(start_time[12:14])

                end_year = year_conversion(end_time[0:4])
                end_month = date_time_conversion(end_time[4:6])
                end_day = date_time_conversion(end_time[6:8])
                end_hour = date_time_conversion(end_time[8:10])
                end_minute = date_time_conversion(end_time[10:12])
                end_seconds = date_time_conversion(end_time[12:14])

                FSC = crc_calculation(
                    fsc_calculation_string(start_year, start_month, start_day, start_hour, start_minute,
                                           start_seconds, end_year, end_month, end_day, end_hour,
                                           end_minute, end_seconds, ))

                load_data = (START_END_FLAG + fsc_calculation_string(start_year, start_month, start_day, start_hour,
                                                                     start_minute, start_seconds, end_year, end_month,
                                                                     end_day, end_hour, end_minute, end_seconds, )
                             + FSC + START_END_FLAG)

                Meter_Load_Data = write_read.read_load_survey_data(Load_Profile_IP_1, Load_Profile_IP_2, load_data)
                string_length = (int(Meter_Load_Data[4:6], 16) * 2 + 4)
                if len(Meter_Load_Data) == string_length:
                    if string_length == 90:
                        # Meter_Load_Data =
                        # '7ea02b41039688ede6e700c401c10001010204090c07e50107ff0300ffff8000001200001200001200fb976b7e'
                        decode_load_survey_data(Serial_Number, Meter_Load_Data, start_time_from_memory, Add_time)
                        break
                    elif string_length == 102:
                        decode_load_survey_data(Serial_Number, Meter_Load_Data, start_time_from_memory, Add_time)
                        break
                    elif string_length == 38:
                        print(len(Meter_Load_Data), Meter_Load_Data)
                        no_load_survey_data_time_store(start_time_from_memory, Add_time)
                        break
                    elif string_length == 40:
                        print(len(Meter_Load_Data), Meter_Load_Data)
                        no_load_survey_data_time_store(start_time_from_memory, Add_time)
                        break

    except Exception as Error:
        print(Error)

        