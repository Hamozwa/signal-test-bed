#test_signal_generator.py
#Generates a test signal and saves to a .bin file

import pyais
from AIS.CRC import *
import message_info



def gen_AIS(msg_type, msg_object):

    #Use pyais to make NMEA 0183 Message depending on message type
    match msg_type:
        case 1:
            payload = pyais.messages.MessageType1.create(
                msg_type = 1,
                repeat = 0,
                mmsi="111111111",
                status = 0,
                turn = 0,
                speed = 0,
                accuracy = 0,
                lon = 0,
                lat = 34,
                course = 0,
                heading = 0,
                second = 0,
                maneuver = 0,
                spare_1 = b'',
                raim = 0,
                radio = 0
            )
            print(payload)
            payload.radio = 1
            print
        case 2:
            pass
        case 3:
            pass
        case 4:
            pass
        case 5:
            pass
        case 6:
            pass
        case 7:
            pass
        case 8:
            pass
        case 9:
            pass
        case 10:
            pass
        case 11:
            pass
        case 12:
            pass
        case 13:
            pass
        case 14:
            pass
        case 15:
            pass
        case 16:
            pass
        case 17:
            pass
        case 18:
            pass
        case 19:
            pass
        case 20:
            pass
        case 21:
            pass


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
        raise ValueError(f"Checksum invalid: {alternate_checksum(to_binary_AIS(data)+checksum)}")

    #Combine to form packet
    return ramp + training_seq + flag + data_and_checksum + flag + buffer


def gen_ADSB():
    pass

def gen_L_Band():
    pass

#etc...

#Save output in file
with open('output_data.bin','wb') as bin_file:
    bin_file.write(gen_AIS(1, []))