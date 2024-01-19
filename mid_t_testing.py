def queueingDelay (packetSize_bits, dataRate_bps, flagCurrentTransmission, numberInQueue):
    L    =  packetSize_bits
    R    =  dataRate_bps
    flag =  flagCurrentTransmission
    N    =  numberInQueue
    if flag == True:
        return ((N + 0.5) * L)/R
    else:
        return 0
    


def packetSwitching (numberRouters, messageSize_b, userDataSize_b, overheadSize_b, processingTime_s, dataRate_bps, propagationDelay_s):
    N  =  numberRouters
    M  =  messageSize_b
    S  =  userDataSize_b
    O  =  overheadSize_b
    P  =  processingTime_s
    R  =  dataRate_bps
    T  =  propagationDelay_s
    links = N+1
    pcktsize = S + O
    trans = pcktsize/R
    return (links*(T + trans)) + ((links-1)*P) + (((M/S)-1)*trans)

import math    
def fragmentOffsets (fragmentSize_bytes, overheadSize_bytes, messageSize_bytes):
    F  =  fragmentSize_bytes
    O  =  overheadSize_bytes
    M  =  messageSize_bytes
    result = []
    for i in range(math.ceil(M/(F-O))):
        result.append(i*(F-O))
    return result

def IPToString (addr):
    return ('{}.{}.{}.{}'.format((addr>>24), ((addr>>16)&255), ((addr>>8)&255), addr&255))
    
print(IPToString(0x20304050))