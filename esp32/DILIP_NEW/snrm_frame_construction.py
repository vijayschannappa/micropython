from crc_calculation import crc_calculation
from initialization import *
import zero_padding 

def snrm_frame_construction():
    f_length = str(FRAME_TYPE + DESTINATION_ADDRESS + SOURCE_ADDRESS + MODE)
    frame_length = (hex(int((len(f_length) + 6) / 2))).replace("0x", "")
    frame_length = zero_padding.zero_pad(frame_length, 2)
    fsc = crc_calculation(str(FRAME_TYPE + frame_length + DESTINATION_ADDRESS + SOURCE_ADDRESS + MODE))
    snrm = str(START_END_FLAG + FRAME_TYPE + frame_length + DESTINATION_ADDRESS + SOURCE_ADDRESS + MODE + fsc
               + START_END_FLAG)
    return snrm


def disconnection_frame_construction():
    f_length = str(FRAME_TYPE + DESTINATION_ADDRESS + SOURCE_ADDRESS + MODE)
    frame_length = (hex(int((len(f_length) + 6) / 2))).replace("0x", "")
    frame_length = zero_padding.zero_pad(frame_length, 2)
    fsc = crc_calculation(str(FRAME_TYPE + frame_length + DESTINATION_ADDRESS + SOURCE_ADDRESS + MODE_DISCONNECTION))
    snrm = str(START_END_FLAG + FRAME_TYPE + frame_length + DESTINATION_ADDRESS + SOURCE_ADDRESS + MODE_DISCONNECTION
               + fsc + START_END_FLAG)
    return snrm
