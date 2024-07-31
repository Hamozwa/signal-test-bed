#test_signal_generator.py
#Generates a test signal and saves to a .bin file

#=========================================== IMPORTS ============================================
import pyais
import CRC
import message_info

#==================================== GENERATION FUNCTIONS =======================================

def gen_AIS(msg_info):

    #Use pyais to make NMEA 0183 Message depending on message type
    payload = pyais.encode.encode_dict(msg_info)[0]
    #Extract 168 bit data from NMEA message and convert to 6 bit ASCII
    data = payload.split(",")[5]
    
    #Assign simple variables for transmission packet
    ramp = b'\x00'
    training_seq = b'\x55\x55\x55'
    flag = b'\x7E'
    buffer = b'\x00\x00\x00'

    #Apply CRC 16 Checksum
    checksum = CRC.create_AIS_checksum(CRC.to_binary_AIS(data))
    data_and_checksum = CRC.binary_string_to_bytes(CRC.to_binary_AIS(data)+checksum)

    #Checksum Validation

    if not CRC.check_AIS_checksum(CRC.to_binary_AIS(data)+checksum):
        raise ValueError("Checksum invalid.")

    #Combine to form packet
    return ramp + training_seq + flag + data_and_checksum + flag + buffer


def gen_ADSB(msg_info):

    #Initialise variables common to all message types
    DF = msg_info['DF']
    CA = msg_info['CA']
    ICAO = msg_info['ICAO']
    TC = msg_info['TC']

    DF_bin = format(DF,'05b')
    CA_bin = format(CA,'03b')
    ICAO_bin = CRC.bytes_to_binary_string(ICAO)
    TC_bin = format(TC,'05b')

    preamble_bin = '1010000101000000'

    #Create corresponding Extended Squitter Message
    #(Wish there was a pyais equivalent for ADS-B...)
    match TC:

        case TC if 1 <= TC <= 4: #Aircraft Identification

            ME_bin = TC_bin + format(CA,'03b')

            for char in msg_info['callsign']:
                a = format(ord(char), '06b')
                ME_bin += a[len(a)-6:len(a)]
        
        case TC if ((9 <= TC <= 18) | (20 <= TC <= 22)): #Airborne Position
            SS_bin = format(msg_info['SS'],'02b')
            SAF_bin = format(msg_info['SAF','b'])
            ALT_bin = format(msg_info['ALT'],'012b')
            T_bin = format(msg_info['T'], 'b')
            F_bin = format(msg_info['F'],'b')
            LAT_CPR_bin = format(msg_info['LAT-CPR'],'017b')
            LON_CPR_bin = format(msg_info['LON-CPR'],'017b')

            ME_bin = TC_bin + SS_bin + SAF_bin + ALT_bin + T_bin + F_bin + LAT_CPR_bin + LON_CPR_bin
            
        case TC if 5 <= TC <= 8: #Surface Position
            MOV_bin = format(msg_info['MOV'],'07b')
            S_bin = format(msg_info['S'],'b')
            TRK_bin = format(msg_info['TRK'],'07b')
            T_bin = format(msg_info['T'], 'b')
            F_bin = format(msg_info['F'],'b')
            LAT_CPR_bin = format(msg_info['LAT-CPR'],'017b')
            LON_CPR_bin = format(msg_info['LON-CPR'],'017b')


            ME_bin = TC_bin + MOV_bin + S_bin + TRK_bin + T_bin + F_bin + LAT_CPR_bin + LON_CPR_bin

        case 19: #Airborne Velocity
            ST_bin = format(msg_info['ST'],'03b')
            IC_bin = format(msg_info['IC'],'b')
            IFR_bin = format(msg_info['IFR'],'b')
            NUCv_bin = format(msg_info['NUCv'],'03b')
            match msg_info['ST']:

                case 1 | 2:
                    Dew_bin = format(msg_info['Dew'],'b')
                    Vew_bin = format(msg_info['Vew'],'010b')
                    Dns_bin = format(msg_info['Dns'],'b')
                    Vns_bin = format(msg_info['Vns'],'010b',)
                    ST_specific_bin = Dew_bin + Vew_bin + Dns_bin + Vns_bin
                
                case 3 | 4:
                    SH_bin = format(msg_info['SH'],'b')
                    HDG_bin = format(msg_info['HDG'],'010b')
                    T_bin = format(msg_info['T'],'b')
                    AS_bin = format(msg_info['AS'],'010b')
                    ST_specific_bin = SH_bin + HDG_bin + T_bin + AS_bin

            VrSrc_bin = format(msg_info['VrSrc'],'b')
            Svr_bin = format(msg_info['Svr'],'b')
            VR_bin = format(msg_info['VR'],'09b')
            Reserved = '00'
            SDif_bin = format(msg_info['SDif'],'b')
            dAlt_bin = format(msg_info['dAlt'],'07b')

            ME_bin = TC_bin + ST_bin + IC_bin + IFR_bin + NUCv_bin + ST_specific_bin + VrSrc_bin + Svr_bin + VR_bin + Reserved + SDif_bin + dAlt_bin

        case 31: #Operation Status
            ST_bin = format(msg_info['ST'],'03b')
            CC_bin = format(msg_info['CC'],'016b')
            OM_bin = format(msg_info['OM'],'016b')
            Ver_bin = format(msg_info['Ver'],'03b')
            NICa_bin = format(msg_info['NICa'],'b')
            NACp_bin = format(msg_info['NACp'],'04b')
            GVA_bin = format(msg_info['GVA'],'02b')
            SIL_bin = format(msg_info['SIL'],'02b')
            BAI_HDG_bin = format(msg_info['BAI/HDG'],'b')
            HRD_bin = format(msg_info['HRD'],'b')
            SILs_bin = format(msg_info['SILs'],'b')
            Reserved = '0'

            ME_bin = TC_bin + ST_bin + CC_bin + OM_bin + Ver_bin + NICa_bin + NACp_bin + GVA_bin + SIL_bin + BAI_HDG_bin + HRD_bin + SILs_bin + Reserved
            
    data_bin = DF_bin + CA_bin + ICAO_bin + ME_bin

    PI_bin = CRC.create_ADSB_checksum(data_bin)

    #Apply PPM (Pulse Position Modulation) and prepend preamble
    payload = data_bin + PI_bin
    transmission_packet = ''
    for num in payload:
        match num:
            case '0':
                transmission_packet += '01'
            case '1':
                transmission_packet += '10'

    return CRC.binary_string_to_bytes(preamble_bin + transmission_packet)

def gen_L_Band():
    pass

#etc...

#======================================= UNIT TESTING ===========================================

if __name__ == "__main__":
    #Save output in file

    with open('output_data.bin','wb') as bin_file:
        test_dict = message_info.AIS_message_info
        test_dict['accuracy'] = 1
        bin_file.write(gen_AIS(test_dict))
        
    print(gen_ADSB(message_info.ADSB_message_info))
