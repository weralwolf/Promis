'''
Created on Nov 1, 2012

@author: weralwolf
'''

from db.connection import DBConnection
from db import Session, SessionOption, MeasurementPoint, Measurement, Scope

import conf.db as dbConf
from conf.local import DEBUG

TAG = "process"

# List of classes which could be used as
__injectors__ = [Session, SessionOption, MeasurementPoint, Measurement, Scope];
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
        if DEBUG:
            print "%s: [%s] list of %i elements" % (TAG, str(key), len(obj));
        for i in obj:
            process(key, i);
            
    # Process dictionary of multiple objects 
    elif (type(obj) == type({})):
        if DEBUG:
            print "%s: [%s] dictionary -> exact object" % (TAG, str(key));

        for injector in __injectors__:
            if injector.check(key):
                if DEBUG:
                    print "%s: [%s] injector found!" % (TAG, str(key));
                __session, _children, _errors = injector.inject(obj, __session);
                
                # If we have any errors we should stop
                if len(_errors):
                    __session.rollback();
                    return _errors;
                
                if DEBUG:
                    print "%s: [%s] children [%i]" % (TAG, str(key), len(_children));
                for child in _children.keys():
                    if DEBUG:
                        print "%s: [%s] child %s" % (TAG, str(key), str(child));

                    process(child, _children[child]);
            
                if injector.tableName() == "Scope":
                    __new_scope = True;

    if __emitter:
        __session.commit();
        __session.close();
    
    if __new_scope:
        Scope.pop();
    return {};
