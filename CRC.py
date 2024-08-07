#CRC.py
#Module supplying functions necessary to apply CRC 16 Checksum
#According to ISO/IEC 13239:2002 Section 4.2.5.2 16-bit FCS

#====================================== BACKGROUND FUNCTIONS =======================================

#Convert data to binary via six-bit ASCII (not UTF-8)
def to_binary_AIS(data):

    output = ''

    for char in data:

        ascii_value = ord(char)

        #Input Sanitisation 
        if ascii_value < 48 or ascii_value > 119:
            raise ValueError("Incorrect letter in ASCII code")

        #Convert to 6 bits via AIS method
        six_bit_value = ascii_value - 48
        if six_bit_value >= 40:
            six_bit_value -= 8

        #Convert 6 bit value to binary
        binary_value = format(six_bit_value, '06b')
        output += binary_value

    return output

def binary_string_to_bytes(binary_string):

    #Adds necessary initial zeroes
    while len(binary_string) % 8 != 0:
        binary_string = '0' + binary_string
    
    integer = int(binary_string, 2)

    return integer.to_bytes((len(binary_string)//8), byteorder='big')

def bytes_to_binary_string(bytes):

    output = ''

    for byte in bytes:
        output += format(byte, '08b')
    
    return output

#XOR two inputted binary strings
def xor (a,b):

    #Initialise output variable
    output = ''

    #Ensure same length of inputs
    if len(a) != len(b):
        raise ValueError(f"XOR lengths are different: a ({len(a)}) b ({len(b)})")

    #XOR digits    
    for i in range(0,len(a)):
        if a[i] == b[i]:
            output += '0'
        else:
            output += '1'
    
    return output

#Uses xor function to carry out modulo 2 division
def mod_2_div(num,den):
    
    #Create pointer for picking out next digit in numerator
    ptr = len(den)

    #Create intial remainder variable
    rem = num[0:ptr]

    #Loop through digits in numerator and xor each loop
    while ptr < len(num):
        
        rem = xor(rem, den).lstrip('0')

        #Add new digits from numerator to XOR, then increment pointer
        while (len(rem) < len(den)) and (ptr < len(num)):
            rem += num[ptr]
            ptr += 1

    #Handle edge cases where it needs one more xor 
    #Idk why they happen, I just know this fixes it      
    if len(rem) == len(den):
        rem = xor(rem, den).lstrip('0')
    return rem

#xors with binary string of 1s
def ones_complement(data):
    return(xor(data, '1'*len(data)))

#NRZI Encoding/Decoding
def NRZI_encode(input_bits):
    encoded ='0'
    for char in input_bits:
        encoded += xor(char,encoded[-1])
    return encoded

def NRZI_decode(input_bits):
    decoded = ''
    for i in range(1,len(input_bits)):
        decoded += xor(input_bits[i-1],input_bits[i])
    return decoded

#Bit Stuffing/Destuffing
def bit_stuff(input_bits):
    one_counter = 0

    for j in range (0,len(input_bits)):
        if input_bits[j] == '1': #Count how many ones in a row so far
            one_counter += 1
        else:
             one_counter = 0

        if one_counter == 5: #If 5 ones in a row, add a zero
            input_bits = input_bits[:j+1] + '0' + input_bits[j+1:]
            one_counter = 0

    return input_bits

def bit_destuff(input_bits):
    one_counter = 0
    write_flag = True
    output_bits = ''

    for bit in input_bits:
            if bit == '1': #Count how many ones in a row so far
                    one_counter += 1
            else:
                one_counter = 0

            if one_counter == 5: #If 5 ones in a row, set flag to ignore the zero
                    one_counter = 0
                    write_flag = False

            if write_flag: #Ignores the zero after 5 ones
                    output_bits += bit
            else:
                    if bit == '1':
                        #raise ValueError("Bitstuffing not detected in this packet.")
                        output_bits += bit #for message parsing when the section after the bitstuffed area is also destuffed uninentionally
                    write_flag = True

    return output_bits


#========================================= CRC FUNCTIONS =============================================

#AIS method fron ISO/IEC 13239:2002 STANDARD (In particular, the method outlined in Annex A)
def create_AIS_checksum(data):
    
    k = len(data)
    data = data + '0'*16
    data = xor(data, '1111111111111111'+('0'*k))
    sol = mod_2_div(data, '10001000000100001')
    while len(sol) < 16:
        sol = '0' + sol
    return ones_complement(sol)

def check_AIS_checksum(data):
    
    k = len(data)
    data = data + '0' * 16
    data = xor(data, ('1'*16)+('0'*k))
    sol = mod_2_div(data, '10001000000100001')
    while len(sol) < 16:
        sol = '0' + sol
    return (sol == '0001110100001111')

#ADSB from https://mode-s.org/decode/
def create_ADSB_checksum(data):
    data = data + '0' * 24
    sol = mod_2_div(data, '1111111111111010000001001')
    while len(sol) < 24:
        sol = '0' + sol
    return sol

def check_ADSB_checksum(data):
    sol = mod_2_div(data, '1111111111111010000001001')
    return (sol.lstrip('0') == '')

#VDES Methods outlined in ITU-R M.2092-1
def create_VDES_32_checksum(data):
    data += '0' * 32
    sol = mod_2_div(data, '100000100110000010001110110110111')
    while len(sol) < 32:
        sol = '0' + sol
    return sol

def check_VDES_32_checksum(data):
    sol = mod_2_div(data, '100000100110000010001110110110111')
    return (sol.lstrip('0') == '')

def create_VDES_16_checksum(data):
    data += '0' * 16
    sol = mod_2_div(data, '11000000000000101')
    while len(sol) < 16:
        sol = '0' + sol
    return sol

def check_VDES_16_checksum(data):
    sol = mod_2_div(data, '11000000000000101')
    return (sol.lstrip('0') == '')


#============================================ UNIT TESTING ===========================================

if __name__ == "__main__":

    print('AIS CRC Test')
    AIS_test_data = '11aucihP0000000CM7P000000000'
    AIS_CRC= create_AIS_checksum(to_binary_AIS(AIS_test_data))
    print(AIS_CRC)
    print(check_AIS_checksum(to_binary_AIS(AIS_test_data)+AIS_CRC))

    print('ADSB CRC Test')
    ADSB_test_data = 'A0000B378DB00030A40000'
    ADSB_CRC = create_ADSB_checksum(bytes_to_binary_string(bytes.fromhex(ADSB_test_data)))
    print(ADSB_CRC)
    print(check_ADSB_checksum(bytes_to_binary_string(bytes.fromhex(ADSB_test_data)) + ADSB_CRC))

    print('VDES 32 CRC Test')
    VDES_32_test_data = '10010100010101001010101001011110010110011001'
    VDES_32_CRC = create_VDES_32_checksum(VDES_32_test_data)
    print(VDES_32_CRC)
    print(check_VDES_32_checksum(VDES_32_test_data + VDES_32_CRC))

    print('VDES 16 CRC Test')
    VDES_16_test_data = '10010100010101001010101001011110010110011001'
    VDES_16_CRC = create_VDES_16_checksum(VDES_16_test_data)
    print(VDES_16_CRC)
    print(check_VDES_16_checksum(VDES_16_test_data + VDES_16_CRC))