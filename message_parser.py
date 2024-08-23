#message_parser
#Reads signal from a file

#=========================================== IMPORTS ============================================

import pyais
import CRC
import bitarray
import message_info

#======================================= READING FUNCTIONS=======================================  

def read_AIS(message):
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

def read_ADSB(message):
    #Convert to Binary
    message_bin = CRC.bytes_to_binary_string(message)

    #Extract message after preamble
    preamble_bin = '1010000101000000'
    start_index = message_bin.index(preamble_bin)
    no_preamble_bin = message_bin[ start_index + 16 : start_index + 240 ]

    #Undo Pulse Position Modulation
    payload = ''
    for i in range(0, len(no_preamble_bin),2):
     match no_preamble_bin[i:i+2]:
            case '01':
               payload += '0'
            case '10':
               payload += '1'
    
    #Check and Strip CRC
    if not CRC.check_ADSB_checksum(payload):
        raise ValueError("Checksum invalid.")
    data_bin = payload[:-24]

    #Create dcitionary to store info
    msg_info = {}

    #Separate out data into fields
    DF_bin = data_bin[0:6]
    CA_bin = data_bin[6:9]
    ICAO_bin = data_bin[9:33]
    ME_bin = data_bin[33:]
    TC_bin = ME_bin[0:6]

    DF = int(DF_bin,2)
    CA = int(CA_bin,2)
    ICAO = int(ICAO_bin,2)
    TC = int(TC_bin,2)

    msg_info['DF'] = DF
    msg_info['CA'] = CA
    msg_info['ICAO'] = ICAO
    msg_info['TC'] = TC


    #Split main payload into specific fields and save to dictionary
    main_data_bin = ME_bin[6:]
    match TC:

        case TC if 1 <= TC <= 4: #Aircraft Identification

            main_data_bin = main_data_bin.lstrip(CA_bin)

            callsign = ''
            for j in range(0,len(main_data_bin),6):
                callsign += chr(main_data_bin[j:j+6])
            
            msg_info['callsign'] = callsign
        
        case TC if ((9 <= TC <= 18) | (20 <= TC <= 22)): #Airborne Position
            
            SS_bin = main_data_bin[0:2]
            SAF_bin = main_data_bin[2]
            ALT_bin = main_data_bin[3:15]
            T_bin = main_data_bin[16]
            F_bin = main_data_bin[17]
            LAT_CPR_bin = main_data_bin[18:35]
            LON_CPR_bin = main_data_bin[35:52]

            msg_info['SS'] = int(SS_bin, 2)
            msg_info['SAF'] = int(SAF_bin, 2)
            msg_info['ALT'] = int(ALT_bin, 2)
            msg_info['T'] = int(T_bin, 2)
            msg_info['F'] = int(F_bin, 2)
            msg_info['LAT_CPR'] = int(LAT_CPR_bin, 2)
            msg_info['LON_CPR'] = int(LON_CPR_bin, 2)
            
        case TC if 5 <= TC <= 8: #Surface Position
            MOV_bin = main_data_bin[0:7]
            S_bin = main_data_bin[7]
            TRK_bin = main_data_bin[8:15]
            T_bin = main_data_bin[16]
            F_bin = main_data_bin[17]
            LAT_CPR_bin = main_data_bin[18:35]
            LON_CPR_bin = main_data_bin[35:52]

            msg_info['MOV'] = int(MOV_bin, 2)
            msg_info['S'] = int(S_bin, 2)
            msg_info['TRK'] = int(TRK_bin, 2)
            msg_info['T'] = int(T_bin, 2)
            msg_info['F'] = int(F_bin, 2)
            msg_info['LAT_CPR'] = int(LAT_CPR_bin, 2)
            msg_info['LON_CPR'] = int(LON_CPR_bin, 2)

        case 19: #Airborne Velocity
            ST_bin = main_data_bin[0:3]
            IC_bin = main_data_bin[3]
            IFR_bin = main_data_bin[4]
            NUCv_bin = main_data_bin[5:8]

            msg_info['ST'] = int(ST_bin, 2)
            msg_info['IC'] = int(IC_bin, 2)
            msg_info['IFR'] = int(IFR_bin, 2)
            msg_info['NUCv'] = int(NUCv_bin, 2)

            ST_specific_bin = main_data_bin[8:30]
            remaining_bin = main_data_bin[30:]

            match msg_info['ST']:

                case 1 | 2:
                    Dew_bin = ST_specific_bin[0]
                    Vew_bin = ST_specific_bin[1:11]
                    Dns_bin = ST_specific_bin[11]
                    Vns_bin = ST_specific_bin[12:]
                    
                    msg_info['Dew'] = int(Dew_bin, 2)
                    msg_info['Vew'] = int(Vew_bin, 2)
                    msg_info['Dns'] = int(Dns_bin, 2)
                    msg_info['Vns'] = int(Vns_bin, 2)

                
                case 3 | 4:
                    SH_bin = ST_specific_bin[0]
                    HDG_bin = ST_specific_bin[1:11]
                    T_bin = ST_specific_bin[11]
                    AS_bin = start_index[12:]
                    
                    msg_info['SH'] = int(SH_bin, 2)
                    msg_info['HDG'] = int(HDG_bin, 2)
                    msg_info['T'] = int(T_bin, 2)
                    msg_info['AS'] = int(AS_bin, 2)

            VrSrc_bin = format(msg_info['VrSrc'],'b')
            Svr_bin = format(msg_info['Svr'],'b')
            VR_bin = format(msg_info['VR'],'09b')
            Reserved = '00'
            SDif_bin = format(msg_info['SDif'],'b')
            dAlt_bin = format(msg_info['dAlt'],'07b')

            ME_bin = TC_bin + ST_bin + IC_bin + IFR_bin + NUCv_bin + ST_specific_bin + VrSrc_bin + Svr_bin + VR_bin + Reserved + SDif_bin + dAlt_bin

        case 31: #Operation Status
            ST_bin = remaining_bin[0:3]
            CC_bin = remaining_bin[3:19]
            OM_bin = remaining_bin[19:35]
            Ver_bin = remaining_bin[35:38]
            NICa_bin = remaining_bin[39]
            NACp_bin = remaining_bin[40:44]
            GVA_bin = remaining_bin[44:46]
            SIL_bin = remaining_bin[46:48]
            BAI_HDG_bin = remaining_bin[48]
            HRD_bin = remaining_bin[49]
            SILs_bin = remaining_bin[50]

            msg_info['ST'] = int(ST_bin, 2)
            msg_info['CC'] = int(CC_bin, 2)
            msg_info['OM'] = int(OM_bin, 2)
            msg_info['Ver'] = int(Ver_bin, 2)
            msg_info['NICa'] = int(NICa_bin, 2)
            msg_info['NACp'] = int(NACp_bin, 2)
            msg_info['GVA'] = int(GVA_bin, 2)
            msg_info['SIL'] = int(SIL_bin, 2)
            msg_info['BAI_HDG'] = int(BAI_HDG_bin, 2)
            msg_info['HRD'] = int(HRD_bin, 2)
            msg_info['SILs'] = int(SILs_bin, 2)

    return msg_info


#========================================== UNIT TESTING ========================================

#if __name__ == "__main__":
    #Read output from file
    #with open('input_data.bin','rb') as file: