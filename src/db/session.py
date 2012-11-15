'''
Created on Nov 14, 2012

@author: weralwolf
'''

from db.__injective_table import InjectiveTable
from db.scope import Scope
from db.__channels_has_sessions import ChannelHasSessions
from db.__base import Base

from conf.local import DEBUG


from sqlalchemy import Column
from sqlalchemy import Integer, DateTime

"""
    @todo: perform more precise error check
"""

TAG = "db.session"

class Session(Base, InjectiveTable):
    """`sessions`

    `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT ,
    `iBegin` TIMESTAMP NOT NULL ,
    `iEnd` TIMESTAMP NOT NULL ,
    PRIMARY KEY (`id`)
    """
    __tablename__ = 'sessions';
    
    __defaults__ = { 'iBegin': None, 'iEnd': None, };
    
    id = Column(Integer(10, Unsigned=True), primary_key=True);
    interval_begin = Column('iBegin', DateTime);
    interval_end = Column('iEnd', DateTime);
    
    def __init__(self, interva_begin, interval_end):
        self.interval_begin = interva_begin;
        self.interval_end = interval_end;
    
    def __repr__(self):
        return "<Session %i | {%s : %s}>" % (int(self.id), str(self.interval_begin), str(self.interval_end));
    
    def __str__(self):
        return "<Session %i | {%s : %s}>" % (int(self.id), str(self.interval_begin), str(self.interval_end));
    
    @staticmethod
    def check(key):
        return str(key).lower() in ["session", "sessions"];
    
    @staticmethod
    def inject(obj, session):
        if DEBUG:
            print "%s: input information: %s " % (TAG, obj);

        errors = {};
        preset = Session.__defaults__;
        preset.update(obj);
        
        # Perform errors check
        if (obj['iBegin'] == None):
            errors['iBegin'] = "iBegine couldn't have zero value, please check it";
            
        if (obj['iEnd'] == None):
            errors['iEnd'] = "iEnd couldn't have zero value, please check it";
            
        if (len(errors)):
            return session, obj, errors;
        
        # Create session element
        toBePushed = Session(obj['iBegin'], obj['iEnd']);
        
        session.add(toBePushed);
        session.flush();
        
        if DEBUG:
            print "%s: %s" % (TAG, toBePushed);
        
        # Connect session with channels, there rules we are working with
        # 1. Scope object control correctness of all information it contains
        # 2. Scope translate all information into one usual format
        
        scope = Scope.state();
        
#        if DEBUG:
#            print "%s: current scope %s" % (TAG, str(scope));
#            
#        if scope.has_key("channels") and len(scope["channels"]):
#            for channel_title in scope["channels"]:
#                if DEBUG:
#                    print "Connection %s with <Channel %s>" % (str(session), channel_title);
#                connection = ChannelHasSessions(toBePushed.id, channel_title);
#                session.add(connection);
        
        for i in Session.__defaults__.keys():
            del obj[i];
        
        return session, obj, {};
    
    @staticmethod
    def tableName():
        return "Session";
