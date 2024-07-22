import pyais
from AIS.CRC import bytes_to_binary_string, check_checksum, from_binary_AIS

def read_AIS(message):
    
    #Convert bytes to binary and extract data and checksum
    message_binary = bytes_to_binary_string(message)
    start_flag_index = message_binary.index('01111110')
    data_and_checksum = message_binary[ start_flag_index + 8 : start_flag_index + 192 ]

    #Check Checksum
    if not check_checksum(data_and_checksum):
        raise ValueError("Checksum invalid.")
    
    #Process Payload
    payload = from_binary_AIS(data_and_checksum[0:168])
    msg = pyais.decode(b"!AIVDM,1,1,,A,"+str.encode(payload)+b",0*4E")

    return msg

#Read output from file
with open('input_data.bin','rb') as file:
    print(read_AIS(file.read()))
