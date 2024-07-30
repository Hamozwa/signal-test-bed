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

#=================================== ISO/IEC 13239:2002 STANDARD ====================================
# (In particular, the method outlined in Annex A)

def create_AIS_checksum(data):
    
    k = len(data)
    data = data + '0000000000000000'
    data = xor(data, '1111111111111111'+('0'*k))
    sol = mod_2_div(data, '10001000000100001')
    while len(sol) < 16:
        sol = '0' + sol
    return ones_complement(sol)

def check_AIS_checksum(data):
    
    k = len(data)
    data = data + '0000000000000000'
    data = xor(data, '1111111111111111'+('0'*k))
    sol = mod_2_div(data, '10001000000100001')
    while len(sol) < 16:
        sol = '0' + sol
    return (sol == '0001110100001111')

#============================================ UNIT TESTING ===========================================

if __name__ == "__main__":
    test_data = '11aucihP0000000CM7P000000000'
    checked = create_AIS_checksum(to_binary_AIS(test_data))
    print(checked)
    print(check_AIS_checksum(to_binary_AIS(test_data)+checked))