'''
Created on Nov 14, 2012

@author: weralwolf
'''

from db.__injective_table import Base
from sqlalchemy import String, Column

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
