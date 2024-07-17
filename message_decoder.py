import pyais
from CRC import *

def read_AIS(message):
    
    #Convert bytes to binary and extract data and checksum
    message_binary = bytes_to_binary_string(message)
    start_flag_index = message_binary.index('01111110')
    data_and_checksum = message_binary[ start_flag_index + 8 : start_flag_index + 192 ]

    #Check Checksum
    if alternate_checksum(data_and_checksum) != '':
        raise ValueError("Checksum invalid.")
    
    #Process Payload
    #payload = 

    return data_and_checksum

#Read output from file
with open('input_data.bin','rb') as file:
    print(read_AIS(file.read()))
