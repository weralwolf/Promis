# -*- coding: utf-8 -*-
"""
Title: Exchange file parser

Created on Tue Sep 18 14:55:38 2012

@author: Elena Piankova
@project: PROMIS
"""

def parserExchangeFile(string):
    """Function for parsing of exchange file from Conec PI TMI KNAP"""
    
    data_bloks = string.split("@")
    # data_bloks[0] -- metadata.
    
    # Metadata parser:
    [descriptive_line, time_creation, session_number, channels] = data_bloks[0].strip().split("\n")
    
    (channel_names, time, measurements) = ([], [], [])
    # Data parser
    for i in xrange(1, len(data_bloks)):
        data = data_bloks[i].strip().split()    
        channel_names.append(data.pop(0))
        time.append(map(int,data[::2]))
        measurements.append(map(float,data[1::2]))
        
    return (channel_names, time, measurements)
#    print time
#    print type(measurements[0][0])
#    print len(channel_names), channel_names

     
     
