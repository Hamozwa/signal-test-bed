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
    ramp_bin = '1111111'
    training_seq_bin = '010101010101010101010101'
    flag_bin = '01111110'

    #Apply CRC 16 Checksum
    checksum_bin = CRC.create_AIS_checksum(CRC.to_binary_AIS(data))
    data_bin = CRC.to_binary_AIS(data)

    #Checksum Validation
    if not CRC.check_AIS_checksum(data_bin+checksum_bin):
        raise ValueError("Checksum invalid.")

    #Byte Reversal
    data_bin = ''.join(data_bin[i:i+8][::-1] for i in range(0, len(data_bin), 8))
    checksum_bin = checksum_bin[::-1]

    reversed_data_and_checksum_bin = data_bin + checksum_bin

    #Bit stuffing
    bitstuffed_packet_section = CRC.bit_stuff(reversed_data_and_checksum_bin)

    #Transmission packet Formation
    main_packet = CRC.NRZI_encode(training_seq_bin + flag_bin + bitstuffed_packet_section + flag_bin)

    return CRC.binary_string_to_bytes(ramp_bin + main_packet)


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

def gen_VDES(*arg):

    #Extract arguments
    vdes_info = arg[0]
    if len(arg) > 1:
        ais_info = arg[1]
    else:
        if vdes_info['message_id'] == 0:
            raise ValueError('AIS info not provided for VDES message type 0.')

    #Initialise common fields
    msg_id = vdes_info['message_id']
    msg_id_bin = format(msg_id,'04b')
    retransmit_flag_bin = format(vdes_info['retransmit_flag'],'01b')
    repeat_indicator_bin = format(vdes_info['repeat_indicator'],'02b')
    session_id_bin = format(vdes_info['session_id'],'06b')
    source_id_bin = format(vdes_info['source_id'],'032b')

    #Construct payload from function input
    match msg_id:

        case 0: #Broadcast AIS ASM Message
            data_count_bin = format(vdes_info['data_count'],'011b')
            ais_bin = CRC.bytes_to_binary_string(gen_AIS(ais_info))[32:]

            payload_bin = msg_id_bin + retransmit_flag_bin + repeat_indicator_bin + session_id_bin + source_id_bin + data_count_bin + ais_bin
        
        case 1: #Scheduled Broadcast message
            data_count_bin = format(vdes_info['data_count'],'011b')
            ASM_identifier_bin = format(vdes_info['ASM_identifier'],'016b')
            binary_data = vdes_info['binary_data']
            communication_state_bin = format(vdes_info['communication_state'],'038b')
            spare_bits = '00'

            payload_bin = msg_id_bin + retransmit_flag_bin + repeat_indicator_bin + session_id_bin + source_id_bin + data_count_bin + ASM_identifier_bin + binary_data + communication_state_bin + spare_bits

        case 2: #Broadcast Message
            data_count_bin = format(vdes_info['data_count'],'011b')
            ASM_identifier_bin = format(vdes_info['ASM_identifier'],'016b')
            binary_data = vdes_info['binary_data']

            payload_bin = msg_id_bin + retransmit_flag_bin + repeat_indicator_bin + session_id_bin + source_id_bin + data_count_bin + ASM_identifier_bin + binary_data

        case 3: #Scheduled Individual Addressed Message
            destination_id_bin = format(vdes_info['destination_id'],'032b')
            data_count_bin = format(vdes_info['data_count'],'011b')
            ASM_identifier_bin = format(vdes_info['ASM_identifier'],'016b')
            binary_data = vdes_info['binary_data']
            communication_state_bin = format(vdes_info['communication_state'],'038b')
            spare_bits = '00'

            payload_bin = msg_id_bin + retransmit_flag_bin + repeat_indicator_bin + session_id_bin + source_id_bin + destination_id_bin + data_count_bin + ASM_identifier_bin + binary_data + communication_state_bin + spare_bits

        case 4: #Individual Addressed Message
            destination_id_bin = format(vdes_info['destination_id'],'032b')
            data_count_bin = format(vdes_info['data_count'],'011b')
            ASM_identifier_bin = format(vdes_info['ASM_identifier'],'016b')
            binary_data = vdes_info['binary_data']
            
            payload_bin = msg_id_bin + retransmit_flag_bin + repeat_indicator_bin + session_id_bin + source_id_bin + destination_id_bin + data_count_bin + ASM_identifier_bin + binary_data

        case 5: #Acknowledgement Message
            destination_id_bin = format(vdes_info['destination_id'],'032b')
            ACK_NACK_mask_bin = format(vdes_info['ACK_NACK_mask'],'016b')

            payload_bin = msg_id_bin + retransmit_flag_bin + repeat_indicator_bin + session_id_bin + source_id_bin + destination_id_bin + ACK_NACK_mask_bin

        case 6: #Geographical Multicast Message
            longitude_1_bin = format(vdes_info['longitude_1'],'018b')
            latitude_1_bin = format(vdes_info['latitude_1'],'017b')
            longitude_2_bin = format(vdes_info['longitude_2'],'018b')
            latitude_2_bin = format(vdes_info['latitude_2'],'017b')
            data_count_bin = format(vdes_info['data_count'],'011b')
            spare_bits = '00'
            ASM_identifier_bin = format(vdes_info['ASM_identifier'],'016b')
            binary_data = vdes_info['binary_data']

            payload_bin = msg_id_bin + retransmit_flag_bin + repeat_indicator_bin + session_id_bin + source_id_bin + longitude_1_bin + latitude_1_bin + longitude_2_bin + latitude_2_bin +data_count_bin + spare_bits + ASM_identifier_bin + binary_data

    return payload_bin

#======================================= UNIT TESTING ===========================================

if __name__ == "__main__":
    #Save output in file

    #with open('output_data.bin','wb') as bin_file:
    #    test_dict = message_info.AIS_message_info
    #    test_dict['accuracy'] = 1
    #    print(gen_AIS(test_dict))
    #    bin_file.write(gen_AIS(test_dict))

    #print(gen_ADSB(message_info.ADSB_message_info))

    print(len(gen_VDES(message_info.VDES_message_info,message_info.AIS_message_info)))
