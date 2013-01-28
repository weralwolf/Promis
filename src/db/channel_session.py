"""
Created on Nov 14, 2012

@author: weralwolf
"""

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

channels_has_sessions = Table("channels_has_sessions", Base.metadata,
                              Column("channels_title", String(255), ForeignKey("channels.title")),
                              Column("sessions_id", Integer(10, Unsigned=True), ForeignKey("sessions.id"))
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
    __tablename__ = "channels";
    
    title = Column(String(255), primary_key=True, unique=True);
    description = Column(String);
    sampling_frequency = Column(Float);
    
    devices_title = Column(String(255), ForeignKey("devices.title"));
    device = relationship("Device", backref="channel");
    
    parameters_title = Column(String(255), ForeignKey("parameters.title"));
    parameter = relationship("Parameter", backref="channel");
    
    sessions = relation(
                            "Session",
                            secondary=channels_has_sessions,
                            backref="channels"
                        );

    @staticmethod
    def find(options, session):
        pass;

class Session(Base, InjectiveTable):
    """`sessions`

    `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT ,
    `iBegin` TIMESTAMP NOT NULL ,
    `iEnd` TIMESTAMP NOT NULL ,
    PRIMARY KEY (`id`)
    """
    __tablename__ = "sessions";
    
    __defaults__ = { "iBegin": None, "iEnd": None, };
    
    id = Column(Integer(10, Unsigned=True), primary_key=True);
    interval_begin = Column("iBegin", DateTime);
    interval_end = Column("iEnd", DateTime);
    
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
    def find(options, session):
        """
        Find object id on different options
        @param options: value of same parameter of Session which id should be known 
        @param session: session of connection to db   
        """
        collector = session.query(Session.id);
        
        collected = [];
        
        if (type(options) != type({})):
            # Verify given key is it exists
            collected = collector.filter(Session.id == int(options)).all();
        
        elif (type(options) == type({})):
            for i in options.keys():
                splited = i.split(".");
                splited.append("eq");
                if (len(splited) > 1):
                    key = splited[0];
                    operator = splited[1];
                     
                    if (key in Session.__defaults__.keys()):
                        if (key == "iBegin"):
                            if (operator == "eq"):
                                collector = collector.filter(Session.interval_begin == options[i]);
                            if (operator == "lt"):
                                collector = collector.filter(Session.interval_begin < options[i]);
                            if (operator == "gt"):
                                collector = collector.filter(Session.interval_begin > options[i]);

                        if (key == "iEnd"):
                            if (operator == "eq"):
                                collector = collector.filter(Session.interval_end == options[i]);
                            if (operator == "lt"):
                                collector = collector.filter(Session.interval_end < options[i]);
                            if (operator == "gt"):
                                collector = collector.filter(Session.interval_end > options[i]);
                else:
                    #@todo: create an exception
                    pass;
            collected = collector.all();
        
        if (not len(collected)):
            return None;
        elif (len(collected) > 1):
            #@todo: make an exception
            return None;
        else:
            return collected[0];
            
    
    @staticmethod
    def inject(obj, session):
        if DEBUG:
            print "%s: input information: %s " % (TAG, obj);

        errors = {};
        preset = Session.__defaults__;
        preset.update(obj);           
        
        # Perform errors check
        if (preset["iBegin"] == None):    
            errors["iBegin"] = "iBegine couldn't have zero value, please check it";
            
        if (preset["iEnd"] == None):      
            errors["iEnd"] = "iEnd couldn't have zero value, please check it";
            
        if (len(errors)):
            return session, obj, errors;
        
        # Create session element
        toBePushed = Session(obj["iBegin"], obj["iEnd"]);  
        
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
        
        Scope.inject({"sessions_id": toBePushed.id}, None, True);
        
        for i in Session.__defaults__.keys():
            del obj[i];
        
        return session, obj, {};
    
    @staticmethod
    def tableName():
        return "Session";
