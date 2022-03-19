from machine import UART
def new_serial_connection():
    try:
        con = UART(2, 9600)
        return con
    except Exception as error:
        print(error)

