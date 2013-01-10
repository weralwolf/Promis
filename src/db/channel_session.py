'''
Created on Nov 14, 2012

@author: weralwolf
'''

from db.__injective_table import InjectiveTable
from db import Scope
from db.__base import Base

from conf.local import DEBUG


from sqlalchemy import String, Float, Integer, DateTime
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.orm import relationship, relation

"""
    @todo: perform more precise error check
"""

"""`channels_has_sessions`

`channels_title` VARCHAR(255) NOT NULL ,
`sessions_id` INT(10) UNSIGNED NOT NULL ,
PRIMARY KEY (`channels_title`, `sessions_id`) ,
INDEX `fk_channels_has_sessions_sessions1` (`sessions_id` ASC) ,
INDEX `fk_channels_has_sessions_channels1` (`channels_title` ASC) ,
CONSTRAINT `fk_channels_has_sessions_channels1`
    FOREIGN KEY (`channels_title` )
    REFERENCES `promis`.`channels` (`title` )
CONSTRAINT `fk_channels_has_sessions_sessions1`
    FOREIGN KEY (`sessions_id` )
    REFERENCES `promis`.`sessions` (`id` )
"""

channels_has_sessions = Table('channels_has_sessions', Base.metadata,
                              Column('channels_title', String(255), ForeignKey('channels.title')),
                              Column('sessions_id', Integer(10, Unsigned=True), ForeignKey('sessions.id'))
                              );

TAG = "db.session"

class Channel(Base):
    """`channels`
    
    `title` VARCHAR(255) NOT NULL ,
    `description` TEXT NOT NULL ,
    `sampling_frequency` DOUBLE NULL ,
    `devices_title` VARCHAR(255) NOT NULL ,
    `parameters_title` VARCHAR(255) NOT NULL ,
    PRIMARY KEY (`title`) ,
    UNIQUE INDEX `title_UNIQUE` (`title` ASC) ,
    INDEX `fk_channels_devices1` (`devices_title` ASC) ,
    INDEX `fk_channels_parameters1` (`parameters_title` ASC) ,
    CONSTRAINT `fk_channels_devices1`
        FOREIGN KEY (`devices_title` )
        REFERENCES `promis`.`devices` (`title` )
    CONSTRAINT `fk_channels_parameters1`
        FOREIGN KEY (`parameters_title` )
        REFERENCES `promis`.`parameters` (`title` )
    """
    __tablename__ = 'channels';
    
    title = Column(String(255), primary_key=True, unique=True);
    description = Column(String);
    sampling_frequency = Column(Float);
    
    devices_title = Column(String(255), ForeignKey('devices.title'));
    device = relationship('Device', backref='channel');
    
    parameters_title = Column(String(255), ForeignKey('parameters.title'));
    parameter = relationship('Parameter', backref='channel');
    
    sessions = relation(
                            'Session',
                            secondary=channels_has_sessions,
                            backref='channels'
                        );

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
    
    def __init__(self, interval_begin, interval_end):
        self.interval_begin = interval_begin;
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
        preset.update(obj);            # Why are you need "preset" variable if you don't use it later?
        
        # Perform errors check
        if (obj['iBegin'] == None):    # Maybe you should use preset['iBegin'] here because if obj hasn't 'iBegin' key exception will be generated
            errors['iBegin'] = "iBegine couldn't have zero value, please check it";
            
        if (obj['iEnd'] == None):      # Maybe you should use preset['iEnd'] here because if obj hasn't 'iEnd' key exception will be generated
            errors['iEnd'] = "iEnd couldn't have zero value, please check it";
            
        if (len(errors)):
            return session, obj, errors;
        
        # Create session element
        toBePushed = Session(obj['iBegin'], obj['iEnd']);  # Maybe you should use preset['iEnd'] and preset['iEnd'] here
        
        # Connect session with channels, there rules we are working with
        # 1. Scope object controls correctness of all information it contains
        # 2. Scope translates all information into one usual format
        
        scope = Scope.state();
        
        if DEBUG:
            print "%s: current scope %s" % (TAG, str(scope));
            
        if scope.has_key("channels") and len(scope["channels"]):
            for channel_title in scope["channels"]:
                if DEBUG:
                    print "Connection %s with <Channel %s>" % (str(session), channel_title);
                
                channel = session.query(Channel).filter_by(title=channel_title).first();

                if channel:                
                    toBePushed.channels.append(channel);
        
        session.add(toBePushed);
        session.flush();
        
        if DEBUG:
            print "%s: %s" % (TAG, toBePushed);
        
        Scope.inject({"sessions_id": toBePushed.id}, None, Scope.level() - 0.5);
        
        for i in Session.__defaults__.keys():
            del obj[i];
        
        return session, obj, {};
    
    @staticmethod
    def tableName():
        return "Session";
