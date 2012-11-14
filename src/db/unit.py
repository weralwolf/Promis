'''
Created on Nov 14, 2012

@author: weralwolf
'''

from db.__base import Base
from sqlalchemy import String, Column

class Unit(Base):
    """`units`
    
    `title` VARCHAR(255) NOT NULL ,
    PRIMARY KEY (`title`) )
    """
    __tablename__ = 'units';
    
    title = Column(String(255), primary_key=True, unique=True);
