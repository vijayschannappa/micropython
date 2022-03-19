def zero_pad(x,size):
    while len(x) != size:
        x = '0'+x
    return x
    