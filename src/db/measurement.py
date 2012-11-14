'''
Created on Nov 1, 2012

@author: weralwolf
'''

from db.__injective_table import InjectiveTable
from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String, LargeBinary
    
class Measurement(InjectiveTable):
    """`measurements`

    `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT ,
    `parameters_title` VARCHAR(255) NOT NULL ,
    `parameters_units_title` VARCHAR(255) NOT NULL ,
    `channels_title` VARCHAR(45) NOT NULL ,
    `measurement_points_id` INT(10) UNSIGNED NOT NULL ,
    `marker` INT(10) UNSIGNED NOT NULL ,
    `measurement` BLOB NOT NULL ,
    `rError` VARCHAR(255) NULL ,
    `lError` VARCHAR(255) NULL ,
    PRIMARY KEY (`id`, `parameters_title`, `parameters_units_title`) ,
    INDEX `measurement_points_id` (`measurement_points_id` ASC) ,
    INDEX `fk_measurements_parameters1` (`parameters_title` ASC, `parameters_units_title` ASC) ,
    INDEX `fk_measurements_channels1` (`channels_title` ASC) ,
    CONSTRAINT `measurements_ibfk_2`
        FOREIGN KEY (`measurement_points_id` )
        REFERENCES `promis`.`measurament_points` (`id` )
    CONSTRAINT `fk_measurements_parameters1`
        FOREIGN KEY (`parameters_title` , `parameters_units_title` )
        REFERENCES `promis`.`parameters` (`title` , `units_title` )
    CONSTRAINT `fk_measurements_channels1`
        FOREIGN KEY (`channels_title` )
        REFERENCES `promis`.`channels` (`title` )
    """
    __tablename__ = 'measurements';
    
    id = Column(Integer(10, Unsigned=True), primary_key=True);
    parameters_title = Column(String(255), ForeignKey('parameters.title'));
    parameters_units_title = Column(String(255), ForeignKey('parameters.units_title'));
    channels_title = Column(String(255), ForeignKey('channles.title'));
    measurement_points_id = Column(Integer(10, Unsigned=True), ForeignKey('measurement_points.id'));
    marker = Column(Integer(10));
    measurement = Column(LargeBinary);
    right_error = Column('rError', LargeBinary);
    left_error = Column('lError', LargeBinary);
    
    @staticmethod
    def check(key):
        return type(key) == type("") and key.lower() in ["measurement", "measurements"];
    
    @staticmethod
    def inject(obj, session):
        return {};   
    
    @staticmethod
    def tableName():
        return "Measurement";
