import urequests
import utime
import network
import ubinascii
import ujson
import re
import collections
from machine import UART


def set_url(data_type=None):
    global url
    if data_type == 'lsd_data':
        url = 'https://demo.reconnectenergy.com/eesl/index.php/C_eesl_data/two'
    elif data_type == 'rt_data':
        url = 'https://demo.reconnectenergy.com/eesl/index.php/C_eesl_data/one'
    else:
        url = 'https://demo.reconnectenergy.com/eesl/index.php/C_eesl_data/three'

def upload_data(data_dict,data_type=None):
    set_url(data_type)
    print('initialising port')
    initialise_port()
    print('pushing data')
    final_data_to_push = format_data_dict(data_dict,data_type)
    #post_data_via_wifi(data_dict)
    post_data_via_gsm(final_data_to_push)
    
def format_data_dict(data_dict,data_type):
    final_dict = collections.OrderedDict()
    mac_id = get_mac_id()
    imei = get_imei_num()
    final_dict['IMEI'] = imei
    final_dict['MAC'] = mac_id
    if data_type == 'lsd_data':
        final_dict['TAG'] = 'LSD'
        final_dict['M.S'] = data_dict['M.S']
        final_dict['LSD'] = data_dict['LSD']
    elif data_type == 'rt_data':
        final_dict['TAG'] = 'RTD'
        final_dict['M.S'] = data_dict.get('SL_NUM')
        final_dict['T.S'] = data_dict.get('T')
        final_dict['P'] = data_dict.get('P')
        final_dict['V'] = data_dict.get('V')
        final_dict['E'] = data_dict.get('E')
        final_dict['I'] = data_dict.get('I')
        final_dict['F'] = data_dict.get('F')
    for k,v in final_dict.items():
        if v is None:
            del final_dict[k]
    print("final_dict:{}".format(final_dict))
    return final_dict
        
       
def get_mac_id():
    mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
    return mac

def connect_to_wifi():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        #sta_if.connect('REConnect_Energy', 'Welcome@REC')
        sta_if.connect('REConnect_Energy_Guest', 'recGuest246#')
        while not sta_if.isconnected():
            pass
    #print('network config:', sta_if.ifconfig())


def post_data_via_wifi(data):
    connect_to_wifi()
    _token='a4dfb9dd-f6b6-f62a-3518-c31981d2a462'
    payload = '------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"data\"\r\n\r\n{}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--'.format(data) 
    payload = payload.replace('OrderedDict({','').replace('})','')
    headers = {
   'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
   'cache-control': "no-cache",
   'postman-token': _token
    }
    response = urequests.request("POST",url,data=payload,headers=headers)
    print("data pushed status:{}".format(response.status_code))


def post_data_via_gsm(data):
    payload = '------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"data\"\r\n\r\n{}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--'.format(data) 
    payload = payload.replace('OrderedDict({','').replace('})','')
    write_to_server(payload)

def initialise_port():
   global uart
   uart = UART(2, baudrate=115200, rts=21, cts=22)
   utime.sleep_ms(1000)
   #nt("initialisation status:{}".format(uart.read()))

def initialise_http():
   uart.write("AT+HTTPINIT\r")
   utime.sleep(1)
   #print("http initialization: {}".format(uart.read()))
   
def write_to_server(data):
    key = 'a4dfb9dd-f6b6-f62a-3518-c31981d2a462'
    try:
        url_write = 'AT+HTTPPARA="URL","{}"\r'.format(url)
        uart.write(url_write)
        utime.sleep(2)
        uart.write('AT+HTTPPARA="CONTENT","multipart/form-data;boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW"\r')
        utime.sleep(2)
        at_write_command = "AT+HTTPDATA={},15000".format(len(data)) + '\r\n'
        uart.write(at_write_command)
        utime.sleep(2)
        uart.write(data)
        utime.sleep(10)
        uart.read()
        uart.write('AT+HTTPACTION=1' + '\r\n')
        utime.sleep(10)        
        print("data push status:{}".format(str(uart.read().decode('utf-8'))))
        #terminate_http()
    except Exception as e:
        print(e)
        #terminate_http()
    

 
def check_for_missing_lsd():
    imei = get_imei_num()
    missing_ts = get_missing_ts(imei)
    return missing_ts
    
def get_imei_num():
    uart.write("AT+SIMEI?\r")
    utime.sleep(5)
    _imei = str(uart.read())
    imei = int(''.join(filter(str.isdigit,_imei)))
    imei = 897584038945866
    return imei

def get_missing_ts(imei,url=None):
    url = 'https://demo.reconnectenergy.com/eesl/index.php/C_eesl_data/send_ide/{}'.format(imei)
    url_write = 'AT+HTTPPARA="URL","{}"\r'.format(url)
    uart.write(url_write)
    utime.sleep(2)
    uart.write('AT+HTTPACTION=0' + '\r\n')
    utime.sleep(5)
    uart.read()
    uart.write("AT+HTTPREAD=19\r")
    utime.sleep(5)
    _raw_ts= str(uart.read())
    print('missing ts:{}'.format(_raw_ts))
    missing_ts = extract_missing_ts(_raw_ts)
    return missing_ts
    
def extract_missing_ts(_raw_ts):
    try:
        datepattern = re.compile("\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d")
        matcher = datepattern.search(_raw_ts)
        ts = matcher.group(0)
        return ts
    except Exception as e:
        return None


if __name__ == "__main__":
    upload_data()