from machine import UART
import utime
import re
url = 'https://demo.reconnectenergy.com/eesl/index.php/C_eesl_data/send_response/lnt'
# APN = 'airtelgprs.com'
APN = 'airteliot.com'


def new_serial_connection():
    try:
        con = UART(2, 115200, rts=0, cts=0)
        return con
    except Exception as error:
        print(error)
        

def send_commands_and_responce(command, responce_1, responce_2, time_out):
    serial_connection.write((command + '\r\n').encode())
    utime.sleep(0.5)
    t=0
    while(t <=time_out):
        t = t+0.005
        utime.sleep(0.005)
        try:
            res = serial_connection.read().decode()
            if responce_1 in res.upper():
                print(res)
                if '713' in res.upper():
                    send_commands_and_responce('AT+CRESET','OK',"ERROR", 10)
                    utime.sleep(30)
                break
            elif responce_2 in res.upper():
                print(res)
                break
            elif '713' in res.upper():
                send_commands_and_responce('AT+CRESET','OK',"ERROR", 10)
                utime.sleep(30)
                break
        except Exception as e:
            pass
        

def read_second_responce(responce, time_out):
    t=0
    while(t <= time_out):
        t = t+0.005
        utime.sleep(0.005)
        try:
            res = serial_connection.read().decode()
            if responce in res.upper():
                print(res)
                if '713' in res.upper():
                    send_commands_and_responce('AT+CRESET','OK',"ERROR", 10)
                    utime.sleep(30)
                break
        except Exception as e:
            pass            
     

def data_upload_to_server(data):
    try:
#         serial_connection = new_serial_connection()
        send_commands_and_responce("AT", "OK","ERROR", 10)
#         send_commands_and_responce('AT+CSQ','OK',"ERROR", 10)
#         send_commands_and_responce('AT+CREG?','+CREG: 0,1',"ERROR", 10)
#         send_commands_and_responce('AT+CPSI?','OK',"ERROR", 10)
#         send_commands_and_responce('AT+CGREG?','+CGREG: 0,1',"ERROR", 10)
#         send_commands_and_responce('AT+CGSOCKCONT=1,\"IP\",\"'+APN+'\"','OK',"ERROR", 10)
#         send_commands_and_responce('AT+CSOCKSETPN=1','OK',"ERROR", 10)
#         send_commands_and_responce('AT+CIPMODE=0','OK',"ERROR", 10)
#         send_commands_and_responce('AT+NETOPEN', '+NETOPEN: 0',"ERROR", 10)
        send_commands_and_responce("AT+HTTPINIT", "OK","ERROR", 10)
        send_commands_and_responce('AT+HTTPPARA="URL","{}"'.format(url),
                                   "OK","ERROR", 10)
        send_commands_and_responce('AT+HTTPACTION=0',"OK","ERROR", 10)
        read_second_responce('HTTPACTION', 10)
        send_commands_and_responce("AT+HTTPREAD=297","OK","ERROR", 10)
#         utime.sleep(5)
        send_commands_and_responce("AT+HTTPTERM","OK","ERROR", 10)
        send_commands_and_responce('AT+HTTPINIT','OK',"ERROR", 10)
        send_commands_and_responce("AT+HTTPPARA=\"URL\",\"https://demo.reconnectenergy.com/eesl/index.php/C_eesl_data/get_meter_get/"+ str(data.replace(' ',''))+"\"",'OK',"ERROR", 10)
        send_commands_and_responce('AT+HTTPACTION=1','OK',"ERROR", 10)
        read_second_responce('HTTPACTION', 10)
        send_commands_and_responce('AT+HTTPTERM','OK',"ERROR", 10)
#         send_commands_and_responce('AT+CIPCLOSE=0','+CIPCLOSE: 0,0',"ERROR", 10)
#         send_commands_and_responce('AT+NETCLOSE', '+NETCLOSE: 0',"ERROR", 10)
    except Exception as e:
        print(e)


def upload_and_store(data, data_type):
    print(data, data_type)
    data_upload_to_server(data)



def get_data_files(data_type):
    print(data_type)


def data_upload(data, to_upload_file, data_type):
    print(data)    


serial_connection = new_serial_connection()