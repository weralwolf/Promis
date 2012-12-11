'''
Created on Nov 14, 2012

@author: weralwolf, elpiankova
'''

from db.__injective_table import InjectiveTable
from db.__base import Base
from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String
        
class SessionOption(Base, InjectiveTable):
    """`sessions_options`

    `id` INT(10) NOT NULL AUTO_INCREMENT ,
    `sessions_id` INT(10) UNSIGNED NOT NULL ,
    `title` VARCHAR(255) NOT NULL ,
    `value` VARCHAR(255) NULL ,
    PRIMARY KEY (`id`) ,
    INDEX `sessions_id` (`sessions_id` ASC) ,
    CONSTRAINT `sessions_options_ibfk_1`
        FOREIGN KEY (`sessions_id` )
        REFERENCES `promis`.`sessions` (`id` )
    """
    __tablename__ = 'session_options';
    
    id = Column(Integer(10, Unsigned=True), primary_key=True);
    title = Column(String(255));
    value = Column(String(255));
    sessions_id = Column(Integer(10, Unsigned=True), ForeignKey('sessions.id'));
    
    
    @staticmethod
    def check(key):
        return type(key) == type("") and key.lower() in [
               "sessionoption", "sessionoptions", "session_option", "session_options"
               ];
    
    @staticmethod
    def inject(obj, session):
        return {};   
    
    @staticmethod
    def tableName():
        return "SessionOption";  