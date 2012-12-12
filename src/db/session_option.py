'''
Created on Nov 14, 2012

@author: weralwolf, elpiankova
'''

from db.__injective_table import InjectiveTable
from db.__base import Base
from db import Scope

from conf.local import DEBUG

from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String

TAG = "db.session_option"
        
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
    
    __defaults__ = { 'sessions_id': None, 'title': None, 'value': None, }; # Is it necessary????
    
    id = Column(Integer(10, Unsigned=True), primary_key=True);
    title = Column(String(255));
    value = Column(String(255));
    sessions_id = Column(Integer(10, Unsigned=True), ForeignKey('sessions.id'));
    
    def __init__(self, title, value):
        self.title = title;
        self.value = value;
    
    @staticmethod
    def check(key):
        return type(key) == type("") and key.lower() in [
               "sessionoption", "sessionoptions", "session_option", "session_options"
               ];
    
    @staticmethod
    def inject(obj, session):
        if DEBUG:
            print "%s: input information: %s " % (TAG, obj);

        errors = {};
        preset = SessionOption.__defaults__;
        preset.update(obj);
        
        # Perform errors check
        if (obj['title'] == None):
            errors['title'] = "Session option title couldn't have zero value, please check it";
            
        if (len(errors)):
            return session, obj, errors;
        
        # Create session option element
        toBePushed = SessionOption(obj['title'], obj['value']);
        
        # Perform connection session option with session into 'session_id' field
        scope = Scope.state();
        
        return {};   
    
    @staticmethod
    def tableName():
        return "SessionOption";  