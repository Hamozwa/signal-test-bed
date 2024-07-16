#test_signal_generator.py
#Generates a test signal and saves to a .bin file

import pyais
from CRC import *


def gen_AIS():

    #Use pyais to make NMEA 0183 Message
    payload = pyais.messages.MessageType1.create(
        mmsi="111111111",
        nav_status = 0,
        sog = 0,
        cog = 0,
        lat = 34,
        lon = 0,
    )

    NMEA_Message = pyais.encode.encode_msg(payload)[0]

    #Extract 168 bit data from NMEA message and convert to 6 bit ASCII
    data = NMEA_Message.split(",")[5]
    
    #Assign simple variables for transmission packet
    ramp = b'\x00'
    training_seq = b'\x55\x55\x55'
    flag = b'\x7E'
    buffer = b'\x00\x00\x00'

    #Apply CRC 16 Checksum
    checksum = alternate_checksum(to_binary_AIS(data))
    data_and_checksum = binary_string_to_bytes(to_binary_AIS(data)+checksum)

    #Checksum Validation

    if alternate_checksum(to_binary_AIS(data)+checksum) != '':
        raise ValueError("Checksum invalid.")

    #Combine to form packet
    return ramp + training_seq + flag + data_and_checksum + flag + buffer


def gen_ADSB():
    pass

def gen_L_Band():
    pass

#etc...

#Save output in file
with open('C:\\Users\\Lab\\Documents\\Simulator\\output_data.bin','wb') as file:
    file.write(gen_AIS())