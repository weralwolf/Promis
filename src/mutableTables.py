'''
Created on Nov 1, 2012

@author: weralwolf
'''

from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String, DateTime, Float
# from sqlalchemy.orm import relationship, backref

from injectiveTable import InjectiveTable
        
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

class SessionOption(InjectiveTable):
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
    
class MeasurementPoint(InjectiveTable):
    """`measurament_points`

    `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT ,
    `time` DOUBLE NOT NULL ,
    `sessions_id` INT(10) UNSIGNED NULL ,
    `lattitude` DOUBLE NULL ,
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
