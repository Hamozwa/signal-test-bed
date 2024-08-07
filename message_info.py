#message_info.py
#Defines message formats and default message values

AIS_message_info = {
    'msg_type' : 1,
    'mmsi' : '11111111',
    
    #No repeated variables
    #1
    'repeat' : 0,
    'status' : 0,
    'turn' : 0,
    'speed' : 0,
    'accuracy' : 0,
    'lon' : 0,
    'lat' : 0,
    'course' : 0,
    'heading' : 0,
    'second' : 0,
    'maneuver' : 0,
    'spare_1' : b'',
    'raim' : 0,
    'radio' : 0,
    #4
    'year' : 1970,
    'month' : 1,
    'day' : 1,
    'hour' : 0,
    'minute' : 0,
    'second' : 0,
    'epfd' : 0,
    #5
    'ais_version' : 0,
    'imo' : 0,
    'callsign' :'',
    'shipname' :'',
    'ship_type' : 0,
    'to_bow' : 0,
    'to_stern' : 0,
    'to_port' : 0,
    'to_starboard' :0,
    'draught' : 0,
    'destination' :'',
    'dte' : 0,
    #6
    'seqno' : 0,
    'dest_mmsi' : "111111111",
    'retransmit' : False,
    'dac' : 0,
    'fid' : 0,
    'data' : b'',
    #7
    'mmsi1' : 0,
    'mmsiseq1' : 0,
    'mmsi2' : 0,
    'mmsiseq2' : 0,
    'mmsi3' : 0,
    'mmsiseq3' : 0,
    'mmsi4' : 0,
    'mmsiseq4' : 0,
    #9
    'alt' : 0,
    'reserved_1' : 0,
    'assigned' : 0,
    #10
    'spare_2' : b'',
    #12
    'text' :'',
    #15
    'type1_1' : 0,
    'offset1_1' : 0,
    'type1_2' : 0,
    'offset1_2' : 0,
    'spare_3' : b'',
    'type2_1' : 0,
    'offset2_1' : 0,
    'spare_4' : b'',
    #16
    'increment1' : 0,
    'increment2' : 0,
    'reserved_2' : 0,
    'cs' : 0,
    'display' : 0,
    'dsc' : 0,
    'band' : 0,
    'msg22' : 0,
    #20
    'offset1' : 0,
    'number1' : 0,
    'timeout1' : 0,
    'offset2' : 0,
    'number2' : 0,
    'timeout2' : 0,
    'offset3' : 0,
    'number3' : 0,
    'timeout3' : 0,
    'increment3' : 0,
    'offset4' : 0,
    'number4' : 0,
    'timeout4' : 0,
    'increment4' : 0,
    #21
    'aid_type' : 0,
    'name' : 0,
    'off_position' : 0,
    'virtual_aid' : 0,
    'name_ext' : '',
    #23
    'ne_lon' : 0,
    'ne_lat' : 0,
    'sw_lon' : 0,
    'sw_lat' : 0,
    'station_type' : 0,
    'txrx' : 0,
    'interval' : 0,
    'quiet' : 0,
    #27
    'gnss' : 0

}

ADSB_message_info = {

    #Common
    'DF': 17, #Downlink Format
    'CA': 0, #Transponder Capability
    'ICAO' : b'H@\xd6',
    'TC' : 1, #Type Code

    #1-4 - Aircraft Identification
    'category' : 0,
    'callsign' : 'KLM1023 ',

    #9-18, 20-22 - Airborne Position
    'SS' : 0, #Surveillance State
    'SAF': 0, #Single Antenna Flag
    'ALT': 0, #Encoded Altitude
    'T': 0, #Time
    'F':0, #CPR Format
    'LAT-CPR': 0, #Encoded Latitude
    'LON-CPR': 0, #Encoded Longitude
    
    #5-8 - Surface Position
    'MOV': 0, #Movement
    'S': 0, #Status for Ground Track
    'TRK': 0, #Ground Track

    #19 - Airborne Velocity
    'ST': 0, #Sub-type
    'IC': 0, #Intent Change Flag
    'IFR': 0, #IFR Capability Flag
    'NUCv': 0, #Navigation Uncertainty Category for Velocity
    'VrSrc': 0, #Source Bit for Vertical Rate
    'Svr': 0, #Sign Bit for Vertical Rate
    'VR': 0, #Vertical Rate
    'SDif': 0, #Sign Bit for GNSS and Baro altitudes difference
    'dAlt': 0, #Difference between GNSS and Baro difference
    
    #ST 1-2
    'Dew': 0, #Direction for E-W Vel.
    'Vew': 0, #E-W Vel.
    'Dns': 0, #Direction for N-S Vel.
    'Vns': 0, #N-S Vel.
    #ST 3-4
    'SH': 0, #Status Bit for Magnetic Heading
    'HDG': 0, #Magnetic Heading
    'T': 0, #Airspeed Type (Not Time)
    'AS': 0, #Airspeed

    #31 - Operation Status
    'ST': 0, #Sub-type
    'CC': 0, #Capacity Class Codes
    'OM': 0, #Operational Mode Codes
    'Ver': 2, #ADS-B Version Number
    'NicA': 0, #NIC Supplement - A
    'NACp': 0, #Navigational Accuracy Category - Position
    'GVA': 0, #Geometrics Vertical Accuracy
    'SIL': 0, #Source Integrity Level
    'BAI/HDG': 0, #Barometric Altitude Integrity/Track Angle or Heading
    'HRD': 0, #Horizontal Reference Direction
    'SILs': 0, #SIL Supplement

}

VDES_message_info = {
    'message_id': 0,

    # Message-specific Fields (no repeats)
    #0 - Broadcast AIS ASM Message (supports AIS messages 6,8,12,14,21,25,26)
    'retransmit_flag': 0,
    'repeat_indicator': 0,
    'session_id': 0,
    'source_id': 0,
    'data_count': 0,
    #TODO: add AIS encapsulation

    #1 - Scheduled Broadcast Message
    'ASM-identifier': 0,
    'communication_state': 0,
    'binary_data': '',

    #2 - Broadcast Message

    #3 - Scheduled Individual Addressed Message
    'destination_id': 0,

    #4 - Individual Addressed Message

    #5 - Acknowledgement Message
    'ACK_NACK_mask': 0,
    'coding_rate_adaptation_request': 0,
    'channel_quality_indicator': 0,


    #6 - Geougraphical Multicast Message
    'longitude_1': 0,
    'latitude_1': 0,
    'longitude_2': 0,
    'latitude_2': 0,
    
}