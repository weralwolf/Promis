'''
Created on Nov 14, 2012

@author: weralwolf
'''

from db.__injective_table import InjectiveTable
from sqlalchemy import Column
from sqlalchemy import Integer, DateTime
        
class Session(InjectiveTable):
    """`sessions`

    `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT ,
    `iBegin` TIMESTAMP NOT NULL ,
    `iEnd` TIMESTAMP NOT NULL ,
    PRIMARY KEY (`id`)
    """
    __tablename__ = 'sessions';
    
    id = Column(10, Integer(Unsigned=True), primary_key=True);
    iBegin = Column(DateTime);
    iEnd = Column(DateTime);
    
    @staticmethod
    def check(key):
        return type(key) == type("") and key.lower() in ["session", "sessions"];
    
    @staticmethod
    def inject(obj, session):
        return {};
    
    @staticmethod
    def tableName():
        return "Session";
