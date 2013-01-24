'''
Created on Nov 1, 2012

@author: weralwolf
'''

from db.connection import DBConnection

import conf.db as db
from conf.local import DEBUG
from db.injectors import injectors

TAG = "process"

# List of classes which could be used as
# __db_conf__ = dbConf.select('contributor');
__db_conf__ = db.select('root');
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
    @param obj: element-value which should be processed, it's an JSON-node
    @param session: data base session data to be pushed to
    '''
    
    # Guaranteed container of data base session
    __session = None;
    
    # Flag which indicates that session created at this iteration and should be
    # deleted here. Also if __emitter is True, it means that it's base level
    # of process inheritance.  
    __emitter = False;
    
    # We should verify data base session status and assign right value for it
    if (session == None):
        # Creating new session, cause it wasn't created before
        __session = __connection__.session();
        __emitter = True;
    else:
        # Inherit already created session
        __session = session;

    # Stop doing nothing, cause empty object couldn't be processed
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
#        # New scope creation flag
#       __new_scope = False;
        Scope.pushLevel();
        
        if DEBUG:
            print "%s: [%s] dictionary -> exact object" % (TAG, str(key));

        # Select type of injector to be used to process object 
        for injector in injectors:
            
            # Comparing injector possible keys with current 
            if injector.check(key):
                if DEBUG:
                    print "%s: [%s] injector found `%s`!" % (TAG, str(key), injector.tableName());
                    
#                # @attention: specific behavior for Scope to check __new_scope flag
#                # @todo: remove it with global `push` & `pop` functions for scope
#                if injector.check("scope"):
#                    if DEBUG:
#                        print "%s: new scope registered" % (TAG);
#                        
#                    __new_scope = True;
                
                __session, _children, _errors = injector.inject(obj, __session);
                
                # If we have any errors we should stop and give them back to user
                if len(_errors):
                    __session.rollback();
                    return _errors;
                
                if DEBUG:
                    print "%s: [%s] children [%i]" % (TAG, str(key), len(_children));
                    
                for child in _children.keys():
                    if DEBUG:
                        print "%s: [%s] child %s" % (TAG, str(key), str(child));

                    process(child, _children[child]);
#        if __new_scope:
#        if DEBUG:
#            print "%s: removing current level scope" % (TAG);
#            
#       Scope.pop();
        Scope.popLevel();
    
    if __emitter:
        if DEBUG:
            print "%s: commit and close session" % (TAG);
            
        __session.commit();
        __session.close();
    
    return {};
