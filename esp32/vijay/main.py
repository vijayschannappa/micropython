import utime
import network
import ujson
import machine
import meter_data_read as obis
import load_profile_construction as lsd
import upload_store
from machine import UART

def main(restart_required=None):
    port_read_status = initialise_port()
    terminate_http()
    http_init_status =initialise_http()
    network_connect_status = check_network_connection()
    if 'OK' not in network_connect_status:
        machine.reset()
    if restart_required or 'OK' not in http_init_status:
        restart_gsm_module()
    try:
        add_minutes, time_diff, param_name = get_dynamic_load_survey_params()
    except Exception as e:
        print('getting static lsp')
        add_minutes, time_diff, param_name = get_static_load_survey_params()
    mtr_sl_num,mtr_time,coded_year_val = obis.obis_code_generation(load_survey_params)
    if param_name.replace(' ','') == 'LSP_INTERVAL':
        lsd.pull_load_survey_data(load_survey_params,Serial_Number=mtr_sl_num,meter_time = mtr_time,coded_year=coded_year_val,Add_time=add_minutes,Difference_Time = time_diff,historical=False)
    missing_ts = upload_store.check_for_missing_lsd()
    if missing_ts:
        lsd.pull_load_survey_data(load_survey_params,Serial_Number=mtr_sl_num,meter_time=mtr_time,missing_ts=missing_ts,historical=True)
    terminate_http()
 
def terminate_http():
   uart.write("AT+HTTPTERM\r")
   utime.sleep(1)
   uart.read()
   
def restart_gsm_module():
    print('restarting gsm device')
    uart.write('AT+CRESET\r')
    utime.sleep(10)
   
def get_static_load_survey_params():
    global load_survey_params
    with open("data.json", "r") as data:
        load_survey_params = ujson.load(data)
        ls_interval = 'LSP_INTERVAL'
        data = load_survey_params[ls_interval]
        add_minutes = data.split('.')[0]
        time_diff_minutes = data.split('.')[1]
    return add_minutes, time_diff_minutes, ls_interval


def get_dynamic_load_survey_params():
    global load_survey_params
    load_survey_params = get_configuration_settings()
    load_survey_params['METER_SL_SLICE'] = '26:6'
    #load_survey_params['PASSWD'] = '11111111'
    ls_interval = 'LSP_INTERVAL'
    data = load_survey_params[ls_interval]
    add_minutes = data.split('.')[0]
    time_diff_minutes = data.split('.')[1]
    return add_minutes, time_diff_minutes, ls_interval

def check_network_connection():
    url = 'https://www.google.com'
    url_write = 'AT+HTTPPARA="URL","{}"\r'.format(url)
    uart.write(url_write)
    utime.sleep(0.5)
    nw_status = str(uart.read().decode('utf-8'))
    return nw_status

def initialise_port():
   global uart
   uart = UART(2, baudrate=115200,rts=0,cts=0)
   uart.write("AT\r")
   utime.sleep_ms(1)
   port_status = str(uart.read())
   print("initialisation status:{}".format(port_status))
   return port_status

def initialise_http():
   terminate_http()
   uart.write("AT+HTTPINIT\r")
   utime.sleep(1)
   http_init_status = str(uart.read().decode('utf-8'))
   print("http initialization: {}".format(http_init_status))
   return http_init_status

def get_configuration_settings():
    url = 'https://demo.reconnectenergy.com/eesl/index.php/C_eesl_data/send_response/sph'
    url_write = 'AT+HTTPPARA="URL","{}"\r'.format(url)
    uart.write(url_write)
    utime.sleep(2)
    print(uart.read())
    uart.write('AT+HTTPACTION=0' + '\r\n') 
    utime.sleep(5)
    data_len=str(uart.read().decode('utf-8')).split(",")[-1]
    data_read_len = "AT+HTTPREAD={}\r".format(data_len)
    uart.write(data_read_len)
    utime.sleep(10)
    _raw_string= str(uart.read().decode('utf-8'))
    utime.sleep(2)
    load_survey_params=get_json_string(_raw_string)
    return load_survey_params


def get_json_string(_raw_string):
    open_indices= []
    close_indices=[]
    for i in find_indices_of('{', _raw_string):
        open_indices.append(i)
    for i in find_indices_of('}', _raw_string):
        close_indices.append(i)
    open_index = open_indices[0]
    close_index = close_indices[-1]+1
    json_string = ujson.loads(_raw_string[open_index:close_index])
    print(json_string)
    return json_string
        
    
def find_indices_of(char, in_string):
    index = -1
    while True:
        index = in_string.find(char, index + 1)
        if index == -1:
            break
        yield index


if __name__ == '__main__':
    module_st_time = utime.mktime(utime.localtime())
    while True:
        try:
            present_time = utime.mktime(utime.localtime())
            print('time dff in min:{}'.format((present_time - module_st_time)))
            if (present_time - module_st_time) > 1800:
                module_st_time = present_time
                main(restart_required=True)
            else:
                main()
        except Exception as e:
            print(e)
