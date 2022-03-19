import time
import collections
import write_read
import upload_store
import zero_padding
from initialization import *
from crc_calculation import crc_calculation
import time_calculation as tm
import sys

# params = ["07e4", "07e5", "07e6", "07e7", "07e8", "07e9", "07ea",
#           "07eb", "07ec", "07ed", "07ee", "07ef", "07f0", "07f1", "07f2"]


def year_conversion(value):
    decimal_to_hex = hex(int(value)).replace("0x", "")
    decimal_to_hex_format = zero_padding.zero_pad(decimal_to_hex, 4)
    return decimal_to_hex_format


def date_time_conversion(value):
    decimal_to_hex = hex(int(value)).replace("0x", "")
    decimal_to_hex_format = zero_padding.zero_pad(decimal_to_hex, 2)
    return decimal_to_hex_format


def fsc_calculation_string(start_year, start_month, start_day, start_hour, start_minute, start_seconds, end_year,
                           end_month, end_day, end_hour, end_minute, end_seconds):
    fsc = str(STARTING_FRAME + LOAD_PROFILE_IP + THIRD_FRAME + start_year + start_month + start_day +
              START_END_SEPARATOR + start_hour + start_minute + start_seconds + FIRST_FRAME_LENGTH + end_year +
              end_month + end_day + START_END_SEPARATOR + end_hour + end_minute + end_seconds
              + SECOND_FRAME_LENGTH).replace(" ", "")
    return fsc


def get_start_time():
    try:
        Start_Time = open('Start_Time.txt', 'r')
        data = Start_Time.read()
        Start_Time.close()
        st_time = data.replace(':', '').replace('-', '').replace(' ', '')
        return st_time
    except Exception as Error:
        print('error in reading start time, considering backup time')

    try:
        Start_Time = open('Start_Time_Backup.txt', 'r')
        data = Start_Time.read()
        st_time = data.replace(':', '').replace('-', '').replace(' ', '')
        f = open('Start_Time.txt', 'w')
        f.write(str(st_time))
        f.close()
        Start_Time.close()
        return st_time
    except Exception as e:
        print('error in reading load survey time from backup text')
        return None


def get_load_survey_time():
    try:
        Start_Time = open('Start_Time_Backup.txt', 'r')
        data = Start_Time.read()
        Start_Time.close()
        return data
    except Exception as Error:
        print(Error)
        return None

def get_decoded_params(Meter_Load_Data,coded_year):
    if coded_year not in Meter_Load_Data:
        int_last_year = int(coded_year,16)-1
        hex_last_year = str(0)+hex(int_last_year)[2:]
    if hex_last_year in Meter_Load_Data:
        coded_year = hex_last_year
    Meter_Load_Data = Meter_Load_Data.split(coded_year)
    print("check_for_splitting:{}".format(Meter_Load_Data))
#     volt = int(Meter_Load_Data[1][34:38], 16)
#     energy = int(Meter_Load_Data[1][22:26], 16)
#     re_energy = int(Meter_Load_Data[1][28:32], 16)
    coded_raw_inst_vals = coded_year+Meter_Load_Data[-1]
    ts= (str(zero_padding.zero_pad(str(int(coded_year, 16)), 4)) + '-' +
                  str(zero_padding.zero_pad(str(int(Meter_Load_Data[1][0:2], 16)), 2)) + '-' +
                  str(zero_padding.zero_pad(str(int(Meter_Load_Data[1][2:4], 16)), 2)) + ' ' +
                  str(zero_padding.zero_pad(str(int(Meter_Load_Data[1][6:8], 16)), 2)) + ':' +
                  str(zero_padding.zero_pad(str(int(Meter_Load_Data[1][8:10], 16)), 2)) + ':' +
                  str('00'))
    return coded_raw_inst_vals,ts
    #return volt,energy,re_energy,ts
    

def decode_load_survey_data(Serial_Number, Meter_Load_Data,coded_year, start, Add_time,historical):
    data_dict={}
    data_dict['M.S']=Serial_Number
    data_dict['LSD'] = Meter_Load_Data
    volt,energy,re_energy,ts = get_decoded_params(Meter_Load_Data,coded_year)
    start_time = ts.replace(':', '').replace('-', '').replace(' ', '')
    if not historical:
        update_local_files(start_time,start,Add_time)
        print('pushing lsd rt data')
        upload_store.upload_data(data_dict,"lsd_data")
    else:
        print('pushing lsd historical data for :{}'.format(start))
        upload_store.upload_data(data_dict,"lsd_data")
        


def update_local_files(start_time,start,Add_time):
    if start == start_time:
        Store_Last_Meter_Data_Fetch_Time = tm.calculate_add_time(
            start_time, int(Add_time))
        f = open('Start_Time.txt', 'w')
        f.write(str(Store_Last_Meter_Data_Fetch_Time))
        f.close()
        f = open('Start_Time_Backup.txt', 'w')
        f.write(str(Store_Last_Meter_Data_Fetch_Time))
        f.close()
    else:
        print('wrong time=', start)
        f = open('Start_Time.txt', 'w')
        f.write(str(start))
        f.close()
        

def no_load_survey_data_time_store(start, Add_time):
    start_time = tm.calculate_add_time(start, int(Add_time))
    f = open('Start_Time.txt', 'w')
    f.write(str(start_time))
    f.close()


def store_correct_time():
    store_time = get_load_survey_time()
    try:
        f = open('Start_Time.txt', 'w')
        f.write(str(store_time))
        f.close()
    except AttributeError:
        store_time = str(meter_time[0:4] + '-' + meter_time[5:7] + '-'
                         + meter_time[8:10] +
                         ' ' + meter_time[11:13]
                         + ':00' + ':00')
        f = open('Start_Time_Backup.txt', 'w')
        f.write(str(store_time))
        f.close()


def store_backup_time(meter_time):
    store_time = str(meter_time[0:4] + '-' + meter_time[5:7] + '-' +
                                 meter_time[8:10] + ' ' + meter_time[11:13] + ':00' + ':00')
    f = open('Start_Time_Backup.txt', 'w')
    f.write(str(store_time))
    f.close()
    
def pull_load_survey_data(lsp,Serial_Number,meter_time,coded_year,Add_time=None,Difference_Time=None,missing_ts=None,historical=False):  # meter_time
    try:
        for error_count in range(3):
            if historical:
                start_time= str(missing_ts).replace(':', '').replace('-', '').replace(' ', '')
                _end_time = tm.calculate_add_time(start_time, 29)
                end_time = str(_end_time).replace(':', '').replace('-', '').replace(' ', '')
                Meter_Load_Data= get_coded_lsd_data(start_time,end_time,lsp)
            else:
                start_time = get_start_time()
                if not start_time:
                    store_backup_time(meter_time)
                end_time = str(meter_time).replace(':', '').replace('-', '').replace(' ', '')
                if str(start_time) > str(end_time):
                    store_correct_time()
                if tm.calculate_start_end_minus_time(start_time, 0) <= tm.calculate_start_end_minus_time(end_time, 32):
                    _end_time = tm.calculate_add_time(start_time, 29)
                    end_time = str(_end_time).replace(':', '').replace('-', '').replace(' ', '')
                    Meter_Load_Data = get_coded_lsd_data(start_time,end_time,lsp)
                else:
                    return None
            string_length = (int(Meter_Load_Data[4:6], 16) * 2 + 4)
            if len(Meter_Load_Data) == string_length:
                decode_load_survey_data(Serial_Number, Meter_Load_Data,coded_year,start_time, Add_time,historical)
                break
    except Exception as Error:
        print(Error)

def get_coded_lsd_data(start_time,end_time,lsp):
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
    FSC = crc_calculation(fsc_calculation_string(start_year, start_month, start_day, start_hour, start_minute,
                                           start_seconds, end_year, end_month, end_day, end_hour,
                                           end_minute, end_seconds, ))

    load_data = (START_END_FLAG + fsc_calculation_string(start_year, start_month, start_day, start_hour,start_minute, start_seconds, end_year, end_month,end_day, end_hour, end_minute, end_seconds, )+ FSC + START_END_FLAG)

    Meter_Load_Data = write_read.read_load_survey_data(Load_Profile_IP_1, Load_Profile_IP_2, load_data,lsp)
    print('mtr load data:{}'.format(Meter_Load_Data))
    return Meter_Load_Data

if __name__ == '__main__':
    pull_load_survey_data('Serial_Number', 'meter_time',
                          'Add_time', 'Difference_Time')
