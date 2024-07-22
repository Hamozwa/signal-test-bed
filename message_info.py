#message_info.py
#Defines message formats and default message values

AIS_message_info = {
    'msg_type' : 1,
    'mmsi' : '',
    
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
    'number1' : 0,
    'timeout1' : 0,
    

}