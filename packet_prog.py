def composepacket (version, hdrlen, tosdscp, totallength, identification, flags, fragmentoffset, timetolive, protocoltype, headerchecksum, sourceaddress, destinationaddress):
    '''constructs a packet'''
    if version != 4:
        return 1
    if hdrlen >= 16 or hdrlen < 0:
        return 2
    if tosdscp >= 64 or tosdscp < 0:
        return 3
    if totallength >= 65536 or totallength < 0:
        return 4
    if identification >= 65536 or identification < 0:
        return 5
    if flags >= 8 or flags < 0:
        return 6
    if fragmentoffset >= 8192 or fragmentoffset < 0:
        return 7
    if timetolive >= 256 or timetolive < 0:
        return 8
    if protocoltype >= 256 or protocoltype < 0:
        return 9
    if headerchecksum >= 65536 or headerchecksum < 0:
        return 10
    if sourceaddress >= 4294967296 or sourceaddress < 0:
        return 11
    if destinationaddress >= 4294967296 or destinationaddress < 0:
        return 12
    byte_list = [(version << 4) | hdrlen, tosdscp << 2, totallength >> 8, totallength & 255, identification >> 8, identification & 255, (flags << 5) | fragmentoffset >> 8, fragmentoffset & 255, timetolive, protocoltype, headerchecksum >> 8, headerchecksum & 255, sourceaddress >> 24, (sourceaddress & 16711680) >> 16, (sourceaddress & 65280) >> 8, sourceaddress & 255, destinationaddress >> 24, (destinationaddress & 16711680) >> 16, (destinationaddress & 65280) >> 8, destinationaddress & 255]
    print(byte_list)
    return bytearray(byte_list)

def basicpacketcheck(pkt):
    if len(pkt) < 20:
        return 1

def convert(x, base):
    if not isinstance(x, int):
        return -1
    if not isinstance(base, int):
        return -2
    if x < 0:
        return -3
    if base < 2:
        return -4
    result = []
    i = 1
    temp = 0
    while temp < x:
        temp = x % (base**i)
        result.append(temp//(base**(i-1)))
        i += 1
    result.reverse()
    return result

def hexstring(x):
    if not isinstance(x, int):
        return -1
    if x < 0:
        return -2
    hexlist = convert(x, 16)
    hexletters = ['A', 'B', 'C', 'D', 'E', 'F']
    hexstr = '0x'
    for a in hexlist:
        if a > 9:
            hexstr += hexletters[(a-10)]
        else:
            hexstr += str(a)
    return hexstr

def decodedate(x):
    month = (x & 4026531840) >> 28
    day = (x & 260046848) >> 23
    year = x & 8388607
    return ('{}.{}.{}'.format(day+1, month+1, year))

def encodedate(day, month, year):
    if day < 1 or day > 31 or month < 1 or month > 12:
        return -1
    return ((month-1) << 28) | ((day-1) << 23) | year 
    