def transmission_delay (packetLength_bytes, rate_mbps):
    '''a transmission delay calculator'''
    return (packetLength_bytes * 8) / rate_mbps

print("{}".format(transmission_delay(1500, 4000000)))

def total_time (cableLength_KM, packetLength_b):
    '''calculates total time of propogation and transmission'''
    rate_bpms = 10000000
    transfer_speedKMms = 200
    transmission_time = packetLength_b / 10000000
    propogation_time = cableLength_KM / transfer_speedKMms
    return transmission_time + propogation_time

def queueing_delay (rate_bpms, numPackets, packetLength_by):
    '''queueing delay calaculation function'''
    leading_data = numPackets * (packetLength_by * 8)
    return leading_data / rate_bpms

def average_trials(P):
    '''calculates trial expected value'''
    ex_value = 1
    ad_trials = ex_value * P
    while ad_trials > 0.00001:
        ex_value += ad_trials
        ad_trials = ad_trials * P
    return ex_value
    
def per_from_ber(bitErrorProb, packetLen_b):
    '''probability of packet error from a bit error probability'''
    return 1 - (1 - bitErrorProb) ** packetLen_b
        
def avg_trials_from_ber (bit_error_probability, packetLength_b):
    '''calculates the average number of trials'''
    P = per_from_ber(bit_error_probability, packetLength_b)
    ex_value = 1
    ad_trials = ex_value * P
    while ad_trials > 0.00000001:
        ex_value += ad_trials
        ad_trials = ad_trials * P
    return ex_value
    
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
    byte_list = [(version << 4) | hdrlen, tosdscp << 2, totallength >> 8, totallength & 255, identification >> 8,
                 identification & 255, (flags << 5) | fragmentoffset >> 8, fragmentoffset & 255, timetolive,
                 protocoltype, headerchecksum >> 8, headerchecksum & 255, sourceaddress >> 24,
                 (sourceaddress & 16711680) >> 16, (sourceaddress & 65280) >> 8, sourceaddress & 255,
                 destinationaddress >> 24, (destinationaddress & 16711680) >> 16, (destinationaddress & 65280) >> 8,
                 destinationaddress & 255]
    return bytearray(byte_list)

def basicpacketcheck(pkt):
    if len(pkt) < 20:
        return 1
    if (pkt[0] >> 4) != 4:
        return 2
    checksum = 0
    for i in range(0, 20):
        if i % 2 == 1:
            checksum += (pkt[i] << 8) + pkt[i-1]
    if checksum > 0xffff:
        x1, x2 = checksum & 0xffff, checksum >> 16
        checksum = x1 + x2
    if checksum != 0xffff:
        return 3
    if (pkt[2] << 8) | pkt[3] != len(pkt):
        return 4
    return True

def destaddress(pkt):
    a = pkt[16]
    b = pkt[17]
    c = pkt[18]
    d = pkt[19]   
    addr = (a << 24) | (b << 16) | (c << 8) | d
    return addr, "{}.{}.{}.{}".format(a,b,c,d)

def payload (pkt):
    header_length = ((pkt[0] & 15) * 32)// 8
    return pkt[header_length:]
    
def revisedcompose (hdrlen, tosdscp, identification, flags, fragmentoffset, timetolive, protocoltype, sourceaddress, destinationaddress, payload):
    if hdrlen >= 16 or hdrlen < 5:
        return 2
    if tosdscp >= 64 or tosdscp < 0:
        return 3
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
    if sourceaddress >= 4294967296 or sourceaddress < 0:
        return 11
    if destinationaddress >= 4294967296 or destinationaddress < 0:
        return 12
    totallength = (hdrlen * 4) + len(payload)
    checksum = 0
    byte_list = [(4 << 4) | hdrlen, tosdscp << 2, totallength >> 8, totallength & 255, identification >> 8,
                 identification & 255, (flags << 5) | fragmentoffset >> 8, fragmentoffset & 255, timetolive,
                 protocoltype, checksum, checksum, sourceaddress >> 24,
                 (sourceaddress & 16711680) >> 16, (sourceaddress & 65280) >> 8, sourceaddress & 255,
                 destinationaddress >> 24, (destinationaddress & 16711680) >> 16, (destinationaddress & 65280) >> 8,
                 destinationaddress & 255]    
    for i in range(len(byte_list)):
        if i % 2 == 1:
            checksum += (byte_list[i] << 8) + byte_list[i-1]
    while checksum > 0xffff:
        checksum = (checksum & 0xffff) + (checksum >> 16)
    checksum = checksum ^ 65535
    byte_list[10], byte_list[11] = checksum & 255, checksum >> 8
    while len(byte_list) < hdrlen * 4:
        byte_list.append(0)
    for byte in payload:
        byte_list.append(byte)
    return bytearray(byte_list) 
