import time
import zero_padding
import sys

def calculate_start_end_minus_time(start, minus_time):
    tm = (int(start[0:4]), int(start[4:6]), int(start[6:8]), int(start[8:10]), int(start[10:12])-minus_time, int(start[12:14]), 0, 0)
    start_time = time.mktime((tm[0], tm[1], tm[2], tm[3], tm[4], tm[5], tm[6], tm[7]))
    year, month, day, hour, minute, second, ms, dayinyear  = time.localtime(start_time)
    start_ts ="{}-{}-{} {}:{}:{}".format(zero_padding.zero_pad(str(year),4),zero_padding.zero_pad(str(month),2),
                                         zero_padding.zero_pad(str(day),2),zero_padding.zero_pad(str(hour),2),
                                         zero_padding.zero_pad(str(minute),2),zero_padding.zero_pad(str(second),2))
    return start_ts

def calculate_add_time(start, add_time):
    tm = (int(start[0:4]), int(start[4:6]), int(start[6:8]), int(start[8:10]), int(start[10:12])+add_time, int(start[12:14]), 0, 0)
    start_time = time.mktime((tm[0], tm[1], tm[2], tm[3], tm[4], tm[5], tm[6], tm[7]))
    year, month, day, hour, minute, second, ms, dayinyear  = time.localtime(start_time)
    start_ts ="{}-{}-{} {}:{}:{}".format(zero_padding.zero_pad(str(year),4),zero_padding.zero_pad(str(month),2),
                                         zero_padding.zero_pad(str(day),2),zero_padding.zero_pad(str(hour),2),
                                         zero_padding.zero_pad(str(minute),2),zero_padding.zero_pad(str(second),2))
    return start_ts

