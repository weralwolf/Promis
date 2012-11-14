'''
Created on Nov 14, 2012

@author: weralwolf
'''

from db.__injective_table import InjectiveTable
from db.scope import Scope
from db.__channels_has_sessions import channels_has_sessions
from db.__base import Base
from sqlalchemy import Column
from sqlalchemy import Integer, DateTime

"""
    @todo: perform more precise error check
"""
        
class Session(Base, InjectiveTable):
    """`sessions`

    `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT ,
    `iBegin` TIMESTAMP NOT NULL ,
    `iEnd` TIMESTAMP NOT NULL ,
    PRIMARY KEY (`id`)
    """
    __tablename__ = 'sessions';
    
    __defaults__ = { 'iBegin': None, 'iEnd': None, };
    
    id = Column(10, Integer(Unsigned=True), primary_key=True);
    interval_begin = Column('iBegin', DateTime);
    interval_end = Column('iEnd', DateTime);
    
    @staticmethod
    def check(key):
        return type(key) == type("") and key.lower() in ["session", "sessions"];
    
    @staticmethod
    def inject(obj, session):
        errors = {};
        obj.update(Session.__defaults__);
        
        # Perform errors check
        if (obj['iBegin'] == None):
            errors['iBegin'] = "iBegine couldn't have zero value, please check it";
            
        if (obj['iEnd'] == None):
            errors['iEnd'] = "iEnd couldn't have zero value, please check it";
            
        if (len(errors)):
            return obj, errors;
        
        # Create session element
        toBePushed = Session();
        toBePushed.interval_begin = obj['iBegin'];
        toBePushed.interval_end = obj['iEnd'];
        
        session.add(toBePushed);
        
        # Connect session with channels, there rules we are working with
        # 1. Scope object control correctness of all information it contains
        # 2. Scope translate all information into one usual format
        
        scope = Scope.state();
        if (scope.has_key("channels") and len(scope["channels"])):
            for channel_title in scope["channels"]:
                connection = channels_has_sessions();
                connection.sessions_id = toBePushed.id;
                connection.channels_title = channel_title;
                session.add(connection);
        
        for i in Session.__defaults__.keys():
            del obj[i];
        
        return obj, {};
    
    @staticmethod
    def tableName():
        return "Session";
