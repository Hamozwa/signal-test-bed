#test_signal_generator.py
#Generates a test signal and saves to a .bin file

#=========================================== IMPORTS ============================================
import pyais
from AIS.CRC import create_checksum, check_checksum, to_binary_AIS, binary_string_to_bytes
from message_info import AIS_message_info

#==================================== GENERATION FUNCTIONS =======================================

def gen_AIS(msg_info):

    #Use pyais to make NMEA 0183 Message depending on message type
    match msg_info['msg_type']:
        case 1:
            payload = pyais.messages.MessageType1.create(
                msg_type = msg_info['msg_type'],
                repeat = msg_info['repeat'],
                mmsi=msg_info['mmsi'],
                status = msg_info['status'],
                turn = msg_info['turn'],
                speed = msg_info['speed'],
                accuracy = msg_info['accuracy'],
                lon = msg_info['lon'],
                lat = msg_info['lat'],
                course = msg_info['course'],
                heading = msg_info['heading'],
                second = msg_info['second'],
                maneuver = msg_info['maneuver'],
                spare_1 = msg_info['spare_1'],
                raim = msg_info['raim'],
                radio = msg_info['radio']
            )
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
    checksum = create_checksum(to_binary_AIS(data))
    data_and_checksum = binary_string_to_bytes(to_binary_AIS(data)+checksum)

    #Checksum Validation

    if not check_checksum(to_binary_AIS(data)+checksum):
        raise ValueError("Checksum invalid.")

    #Combine to form packet
    return ramp + training_seq + flag + data_and_checksum + flag + buffer


def gen_ADSB():
    pass

def gen_L_Band():
    pass

#etc...

#======================================= UNIT TESTING ===========================================

if __name__ == "__main__":
    #Save output in file
    with open('output_data.bin','wb') as bin_file:
        bin_file.write(gen_AIS(AIS_message_info))
