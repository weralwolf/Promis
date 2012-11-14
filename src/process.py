'''
Created on Nov 1, 2012

@author: weralwolf
'''

from dbConnection import DBConnection
from mutableTables import Session, SessionOption, MeasurementPoint, Measurement
from scope import Scope
import dbConf

import json;
data = json.load(open('example.json'));


# List of classes which could be used as
__classes__ = [Session, SessionOption, MeasurementPoint, Measurement, Scope];
__db_conf__ = dbConf.select('contributor');
__connection__ = DBConnection(
                              __db_conf__['user'],
                              __db_conf__['password'],
                              __db_conf__['db_name'],
                              __db_conf__['host'],
                              __db_conf__['driver']
                              );

def process(key, obj, session=None):
    '''
        Process JSON-key element and recursively goes deep inside 
        @param key: element-name of some list or JSON-dictionary which should be 
               processed
        @param obj: element-value which should be processed
        @param session: data base session data to be pushed to 
    '''
    
    # Guaranteed container of data base session
    __session = None;
    
    # Indicate does session should be also closed by this thread of recursion
    __emitter = False;
    
    # Indicate does was created a new scope here
    __new_scope = False;

    # We should verify data base session situation
    if (session == None):
        __session = __connection__.session();
        __emitter = True;
    else:
        __session = session;

    # Stop doing nothing, cause empty object couldn't be parsed
    if (obj == None) :
        return;

    # Process list of objects with same key
    if (type(obj) == type([])):
        for i in obj:
            process(key, i);
            
    # Process dictionary of multiple objects 
    elif (type(obj) == type({})):
        for i in obj.keys():
            
            for i in __classes__:
                if (i.check(key)):
                    _children = i.inject(obj, __session);
                    for i in _children.keys():
                        process(i, i[key]);
                
                    if (i.tableName() == "Scope"):
                        __new_scope = True;

    if (__emitter) :
        __session.save();
        __session.close();
    
    if (__new_scope):
        Scope.pop();
    return;
