# -*- coding: utf-8 -*-
"""
Title: Exchange file parser

Created on Tue Sep 18 14:55:38 2012

@author: Elena Piankova
@project: PROMIS
"""
def mergingString4segmentedTime(string1, string2):
    return string1+ " " + string2

def parserExchangeFile(string):
    """Function for parsing of exchange file from Conec PI TMI KNAP"""
    
    data_bloks = string.split("@")
    # data_bloks[0] -- metadata.
    
    # Metadata parser:
    [descriptive_line, time_creation, session_number, channels] = data_bloks[0].strip().split("\n")
    
    (channel_names, channel_units, time_BTS, measurements, time_segmented) = ([], [], [], [], [])
    # Data parser
    for i in xrange(1, len(data_bloks)):
        data = data_bloks[i].strip().split()    
        channel_names.append(data.pop(0))
        channel_units.append(data.pop(0).lstrip("(").rstrip(")"))        
        time_BTS.append(map(int,data[::4]))
        measurements.append(map(float,data[1::4]))
        time_segmented.append(map(mergingString4segmentedTime, data[2::4], data[3::4]))
        
    return (channel_names, channel_units, time_BTS, measurements, time_segmented)
    #(channel_names, channel_units, time_BTS, time_semented, measurements)
#    print time
#    print type(measurements[0][0])
#    print len(channel_names), channel_names

     
     
