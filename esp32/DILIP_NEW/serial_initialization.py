from machine import UART
def new_serial_connection():
    try:
        con = UART(1, 9600, rts=0, cts=0, tx=21, rx=22)
        return con
    except Exception as error:
        print(error)

