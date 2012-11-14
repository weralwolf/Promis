'''
Created on Nov 14, 2012

@author: weralwolf
'''

from injectiveTable import Base
from sqlalchemy import Integer, String , Float
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.orm import relationship, relation

class Satellite(Base):
    """`satellites`
    
    `title` VARCHAR(255) NOT NULL ,
    `description` TEXT NOT NULL ,
    PRIMARY KEY (`title`) ,
    UNIQUE INDEX `title_UNIQUE` (`title` ASC)
    """
    
    __tablename__ = "satellites";
    
    title = Column(String(255), primary_key=True, unique=True);
    description = Column(String);
    
class Device(Base):
    """`devices`
    
    `title` VARCHAR(255) NOT NULL ,
    `description` TEXT NOT NULL ,
    `satellites_title` VARCHAR(255) NOT NULL ,
    PRIMARY KEY (`title`) ,
    UNIQUE INDEX `title_UNIQUE` (`title` ASC) ,
    INDEX `fk_devices_satellites1` (`satellites_title` ASC) ,
    CONSTRAINT `fk_devices_satellites1`
        FOREIGN KEY (`satellites_title` )
        REFERENCES `promis`.`satellites` (`title` )
    """
    __tablename__ = 'devices';
    
    title = Column(String(255), primary_key=True, unique=True);
    description = Column(String);
    satellites_title = Column(String(255), ForeignKey('satellites.title'));
    satellite = relationship('Satellite', backref='devices');
    

class Unit(Base):
    """`units`
    
    `title` VARCHAR(255) NOT NULL ,
    PRIMARY KEY (`title`) )
    """
    __tablename__ = 'units';
    
    title = Column(String(255), primary_key=True, unique=True);

"""`parameters_has_parameters`

`parent_title` VARCHAR(255) NOT NULL ,
`child_title` VARCHAR(255) NOT NULL ,
PRIMARY KEY (`parent_title`, `child_title`) ,
INDEX `fk_parameters_has_parameters_parameters2` (`child_title` ASC) ,
INDEX `fk_parameters_has_parameters_parameters1` (`parent_title` ASC) ,
CONSTRAINT `fk_parameters_has_parameters_parameters1`
    FOREIGN KEY (`parent_title` )
    REFERENCES `promis`.`parameters` (`title` )
CONSTRAINT `fk_parameters_has_parameters_parameters2`
    FOREIGN KEY (`child_title` )
    REFERENCES `promis`.`parameters` (`title` )
"""

parameters_has_parameters = Table('parameters_has_parameters', Base.metadata,
                                  Column('parent_title', String(255), ForeignKey('parameters.title')),
                                  Column('child_title', String(255), ForeignKey('parameters.title'))
                                  );

class Parameter(Base):
    """`parameters`
    
    `title` VARCHAR(255) NOT NULL ,
    `units_title` VARCHAR(255) NOT NULL ,
    PRIMARY KEY (`title`, `units_title`) ,
    UNIQUE INDEX `title_UNIQUE` (`title` ASC) ,
    INDEX `fk_parameters_units1` (`units_title` ASC) ,
    CONSTRAINT `fk_parameters_units1`
        FOREIGN KEY (`units_title` )
        REFERENCES `promis`.`units` (`title` )
    """
    __tablename__ = 'parameters';
    
    title = Column(String(255), primary_key=True, unique=True);
    unit_title = Column(String(255), ForeignKey('units.title'));
    
    unit = relationship('Unit', backref='paremeters');
    parents = relation(
                           'Parameter', 
                           secondary=parameters_has_parameters,
                           primaryjoin=(parameters_has_parameters.c.child_title == title),
                           secondaryjoin=(parameters_has_parameters.c.parent_title == title),
                           backref='children'
                       );


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
    
    device_title = Column(String(255), ForeignKey('devices.titles'));
    device = relationship('Device', backref='channel');
    
    paramenters_title = Column(String(255), ForeignKey('parameters.title'));
    paramenter = relationship('Parameters', backref='channel');
    
    sessions = relation(
                            'Channel',
                            secondary=channels_has_sessions,
                            backref='channels'
                        );
