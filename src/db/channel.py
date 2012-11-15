'''
Created on Nov 14, 2012

@author: weralwolf
'''

from db.__base import Base
from db.__channels_has_sessions import channels_has_sessions

from sqlalchemy import String , Float
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship, relation

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
    
    device_title = Column(String(255), ForeignKey('devices.title'));
    device = relationship('Device', backref='channel');
    
    paramenters_title = Column(String(255), ForeignKey('parameters.title'));
    paramenter = relationship('Parameter', backref='channel');
    
    sessions = relation(
                            'Channel',
                            secondary=channels_has_sessions,
                            backref='channels'
                        );
