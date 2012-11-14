'''
Created on Nov 14, 2012

@author: weralwolf
'''

from db.__injective_table import Base
from sqlalchemy import String, Column, ForeignKey
from sqlalchemy.orm import relationship

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
    