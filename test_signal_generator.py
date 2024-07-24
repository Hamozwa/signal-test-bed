#test_signal_generator.py
#Generates a test signal and saves to a .bin file

#=========================================== IMPORTS ============================================
import pyais
from AIS.CRC import create_checksum, check_checksum, to_binary_AIS, binary_string_to_bytes
from message_info import AIS_message_info

#==================================== GENERATION FUNCTIONS =======================================

def gen_AIS(msg_info):

    #Use pyais to make NMEA 0183 Message depending on message type
    payload = pyais.encode.encode_dict(msg_info)[0]
    #Extract 168 bit data from NMEA message and convert to 6 bit ASCII
    data = payload.split(",")[5]
    print(data)
    
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
        test_dict = AIS_message_info
        test_dict['accuracy'] = 1
        bin_file.write(gen_AIS(test_dict))
