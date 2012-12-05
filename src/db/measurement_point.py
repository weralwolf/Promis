'''
Created on Nov 14, 2012

@author: weralwolf
'''

from db.__injective_table import InjectiveTable
from db.__base import Base
from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, Float   
    
class MeasurementPoint(Base, InjectiveTable):
    """`measurament_points`

    `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT ,
    `time` DOUBLE NOT NULL ,
    `sessions_id` INT(10) UNSIGNED NULL ,
    `latitude` DOUBLE NULL ,
    `longitude` DOUBLE NULL ,
    `altitude` DOUBLE NULL ,
    PRIMARY KEY (`id`) ,
    INDEX `fk_measurament_points_sessions1` (`sessions_id` ASC) ,
    CONSTRAINT `fk_measurament_points_sessions1`
        FOREIGN KEY (`sessions_id` )
        REFERENCES `promis`.`sessions` (`id` )
    """
    __tablename__ = 'measurement_points';
    
    id = Column(Integer(10, Unsigned=True), primary_key=True);
    time = Column(Float);
    sessions_id = Column(Integer(10, Unsigned=True), ForeignKey('sessions.id'));
    lattitude = Column(Float, default=None);
    longitude = Column(Float, default=None);
    altitude = Column(Float, default=None);
    
    @staticmethod
    def check(key):
        return type(key) == type("") and key.lower() in [
               "measurementpoint", "measurementpoints", 
               "measurement_point", "measurement_points"
               ];
    
    @staticmethod
    def inject(obj, session):
        return {};   
    
    @staticmethod
    def tableName():
        return "MeasurementPoint"; 