#message_parser
#Reads signal from a file

#=========================================== IMPORTS ============================================

import pyais
import CRC
import bitarray

#======================================= READING FUNCTIONS=======================================  

def read_AIS(message):
    
    #Convert bytes to binary and extract data and checksum
    message_binary = CRC.bytes_to_binary_string(message)
    start_flag_index = message_binary.index('01111110')
    data_and_checksum = message_binary[ start_flag_index + 8 : start_flag_index + 192 ]
    data = data_and_checksum[0:len(data_and_checksum)-16]

    #Check Checksum
    if not CRC.check_AIS_checksum(data_and_checksum):
        raise ValueError("Checksum invalid.")
    
    #Process Payload
    msg_type = int(data[0:6],2)
    bit_array = bitarray.bitarray()
    bit_array.frombytes(CRC.binary_string_to_bytes(data))
    msg = pyais.messages.MSG_CLASS[msg_type].from_bitarray(bit_array)

    return str(msg).lstrip("MessageType1(").rstrip(")")

#========================================== UNIT TESTING ========================================

if __name__ == "__main__":
    #Read output from file
    with open('input_data.bin','rb') as file:
        print(read_AIS(file.read()))