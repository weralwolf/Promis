'''
Created on Nov 1, 2012

@author: weralwolf
'''

from db.__injective_table import InjectiveTable
from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String, DateTime, Float   
    
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
    
    @staticmethod
    def check(key):
        return type(key) == type("") and key.lower() in ["measurement", "measurements"];
    
    @staticmethod
    def inject(obj, session):
        return {};   
    
    @staticmethod
    def tableName():
        return "Measurement";
