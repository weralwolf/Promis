'''
Created on Nov 14, 2012

@author: weralwolf
'''

from db.__base import Base


from sqlalchemy import Integer, String 
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.orm import mapper

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

class ChannelHasSessions(object):
    def __init__(self, session, channel):
        self.channels_title = channel;
        self.session_id = session;

channels_has_sessions = Table('channels_has_sessions', Base.metadata,
                              Column('channels_title', String(255), ForeignKey('channels.title')),
                              Column('sessions_id', Integer(10, Unsigned=True), ForeignKey('sessions.id'))
                              );
mapper(ChannelHasSessions, channels_has_sessions);