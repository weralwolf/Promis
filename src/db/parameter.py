'''
Created on Nov 14, 2012

@author: weralwolf
'''


from db.__injective_table import Base
from sqlalchemy import Table, String, Column, ForeignKey
from sqlalchemy.orm import relationship, relation

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
