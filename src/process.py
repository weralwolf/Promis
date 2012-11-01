'''
Created on Nov 1, 2012

@author: weralwolf
'''

from dbConnection import DBConnection
from dbTables import Satellite, Device, Session, SessionOption
from scope import Scope
import dbConf

import json;
data = json.load(open('example.json'));


# List of classes which could be used as
__classes__ = [Satellite, Device, Session, SessionOption];
__db_conf__ = dbConf.select('contributor');
__connection__ = DBConnection(
                              __db_conf__['user'], 
                              __db_conf__['password'], 
                              __db_conf__['db_name'], 
                              __db_conf__['host'], 
                              __db_conf__['driver']
                              );

'''
@param key: element-name of some list or dictionary which should be processed
@param obj: element-value which should be processed
'''
def process(key, obj, session=None):
    __session = None;
    __emitter = False;
    __new_scope = False;

    if (session == None):
        __session = __connection__.session();
        __emitter = True;
    else:
        __session = session;

    if (obj == None) :
        return;

    # process list of objects with same key
    if (type(obj) == type([])):
        for i in obj:
            process(key, i);
    # process dictionary of multiple objects 
    elif (type(obj) == type({})):
        for i in obj.keys():
            
            if (i == 'scope'):
                Scope.push(obj);
                __new_scope = True;
            
            for i in __classes__:
                if (i.check(key)):
                    _scope, _children = i.inject(obj, __session);
                    for i in _children.keys():
                        process(i, i[key]);
                    break;
                
    if (__emitter) :
        __session.save();
        __session.close();
    
    if (__new_scope):
        Scope.pop();
    return;
