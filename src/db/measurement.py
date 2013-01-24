'''
Created on Nov 1, 2012

@author: weralwolf
'''
from db import Scope
from db.__injective_table import InjectiveTable
from db.__base import Base
from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String, LargeBinary
from conf.local import DEBUG

TAG = "db.measurement"
 
class Measurement(Base, InjectiveTable):
    """`measurements`

    `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT ,
    `parameters_title` VARCHAR(255) NOT NULL ,
    `channels_title` VARCHAR(45) NOT NULL ,
    `measurement_points_id` INT(10) UNSIGNED NOT NULL ,
    `marker` INT(10) UNSIGNED NOT NULL ,
    `measurement` BLOB NOT NULL ,
    `rError` VARCHAR(255) NULL ,         # This means relative error                         
    PRIMARY KEY (`id`, `parameters_title`, `parameters_units_title`) ,
    INDEX `measurement_points_id` (`measurement_points_id` ASC) ,       
    INDEX `fk_measurements_parameters1` (`parameters_title` ASC) , 
    INDEX `fk_measurements_channels1` (`channels_title` ASC) ,
    CONSTRAINT `measurements_ibfk_2`
        FOREIGN KEY (`measurement_points_id` )
        REFERENCES `promis`.`measurament_points` (`id` )
    CONSTRAINT `fk_measurements_parameters1`
        FOREIGN KEY (`parameters_title` )
        REFERENCES `promis`.`parameters` (`title` )
    CONSTRAINT `fk_measurements_channels1`
        FOREIGN KEY (`channels_title` )
        REFERENCES `promis`.`channels` (`title` )
    """
    __tablename__ = 'measurements';
    
    __defaults__ = {'marker': None, 'measurement': None, 'relative_error': None};     
    
    id = Column(Integer(10, Unsigned=True), primary_key=True);
    parameters_title = Column(String(255), ForeignKey('parameters.title'));
    channels_title = Column(String(255), ForeignKey('channles.title'));
    measurement_points_id = Column(Integer(10, Unsigned=True), ForeignKey('measurement_points.id'));
    marker = Column(Integer(10));
    measurement = Column(LargeBinary);
    relative_error = Column('rError', LargeBinary);

    def __init__(self, measurement, marker=0, relative_error=None):
        self.measurement = measurement;
        self.marker = marker;
        self.relative_error = relative_error;
            
    @staticmethod
    def check(key):
        return type(key) == type("") and key.lower() in ["measurement", "measurements"];
    
    @staticmethod
    def inject(obj, session):
        if DEBUG:
            print "%s: input information: %s " % (TAG, obj);
            
        errors = {};
        preset = Measurement.__defaults__;
        preset.update(obj);
        
        # Perform errors check
        if (preset['measurement'] == None):
            errors['measurement'] = "Measurement couldn't have Null value, please check it";
            
        toBePushed = Measurement(preset['measurement'], preset['marker'], preset["relative_error"]);
       
        # Perform connection measurement with measurement_point, parameter and channel
        scope = Scope.state(); 

        if DEBUG:
            print "%s: current scope %s" % (TAG, str(scope));    
        
        if scope.has_key("measurement_point_id"):
            toBePushed.measurement_points_id = scope["measurement_point_id"]
        else:
            errors["measurement_point_id"] = "Measurement point for Measurement couldn't have Null value, please check it";
            
        return {};   
    
    @staticmethod
    def tableName():
        return "Measurement";
