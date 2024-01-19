import math
def connection_setup_delay (cableLength_km, speedOfLight_kms, dataRate_bps, messageLength_b, processingTimes_s):
  '''calculates setup delay in a connection request'''
  return 4*((cableLength_km/speedOfLight_kms) + (messageLength_b/dataRate_bps) + processingTimes_s)

def message_delay (connSetupTime_s, cableLength_km, speedOfLight_kms, messageLength_b, dataRate_bps):
  '''calculates a message delay for a connection'''
  return connSetupTime_s + 2*(cableLength_km/speedOfLight_kms) + (messageLength_b/dataRate_bps)

def total_number_bits (maxUserDataBitsPerPacket_b, overheadBitsPerPacket_b, messageLength_b):
  S = maxUserDataBitsPerPacket_b
  O = overheadBitsPerPacket_b
  M = messageLength_b
  return M + ((M+(S-1))//S)*O

def packet_transfer_time (linkLength_km, speedOfLight_kms, processingDelay_s, dataRate_bps, maxUserDataBitsPerPacket_b, overheadBitsPerPacket_b):
  L = linkLength_km
  C = speedOfLight_kms
  P = processingDelay_s
  R = dataRate_bps
  S = maxUserDataBitsPerPacket_b
  O = overheadBitsPerPacket_b
  return 2*((L/C) + P + (S + O)/R)

def total_transfer_time (linkLength_km, speedOfLight_kms, processingDelay_s, dataRate_bps, maxUserDataBitsPerPacket_b, overheadBitsPerPacket_b, messageLength_b):
  l = linkLength_km
  c = speedOfLight_kms
  p = processingDelay_s
  r = dataRate_bps
  s = maxUserDataBitsPerPacket_b
  o = overheadBitsPerPacket_b
  m = messageLength_b
  return 2*((l/c) + p) + (s+o)/r + ((m+((m/s)*o))/r)
print ("{:.5f}".format(total_transfer_time(10000, 200000, 0.001, 1000000, 1000, 100, 1000000000)))