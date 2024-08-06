#message_parser
#Reads signal from a file

#=========================================== IMPORTS ============================================

import pyais
import CRC
import bitarray

#======================================= READING FUNCTIONS=======================================  

def read_AIS(message):
    message = b'\xfefffT?\x80F\x98/\xff\xff\xe0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x16\xbaT'
    #Extract data and checksum
    message_bin = CRC.bytes_to_binary_string(message)
    
    #NRZI Decoding of entire message
    NRZI_decoded = CRC.NRZI_decode(message_bin)

    #Extract section that definitely contains entire message (bit stuffing causes variable length)
    start_flag_index = NRZI_decoded.index('01111110')
    section_to_destuff = NRZI_decoded[ start_flag_index + 8 : start_flag_index + min(len(NRZI_decoded) - 8, 248) ]

    #Destuff and extract byte-reversed data and FCS
    bit_destuffed = CRC.bit_destuff(section_to_destuff)
    byte_reversed_data = bit_destuffed[:168]
    reversed_FCS = bit_destuffed[168:184]


    #Reverse Bytes and extract data and FCS
    data_bin = ''.join(byte_reversed_data[i:i+8][::-1] for i in range(0, len(byte_reversed_data), 8))
    checksum_bin = reversed_FCS[::-1]

    #Check Checksum
    if not CRC.check_AIS_checksum(data_bin + checksum_bin):
        raise ValueError("Checksum invalid.")
    
    #Process Payload
    msg_type = int(data_bin[0:6],2)
    bit_array = bitarray.bitarray()
    bit_array.frombytes(CRC.binary_string_to_bytes(data_bin))
    msg = pyais.messages.MSG_CLASS[msg_type].from_bitarray(bit_array)

    return str(msg).lstrip("MessageType1(").rstrip(")")

#========================================== UNIT TESTING ========================================

if __name__ == "__main__":
    #Read output from file
    #with open('input_data.bin','rb') as file:
    print(read_AIS(''))