'''
Created on Nov 14, 2012

@author: weralwolf
'''

from db.__injective_table import InjectiveTable
from db.__base import Base
from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, Float

from conf.local import DEBUG
from db import Scope

TAG = "db.measurement_point"
    
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
    
    __defaults__ = {'time': None, 'sessions_id': None, 
                    'latitude': None, 'longitude': None, 'altitude': None};     
    
    id = Column(Integer(10, Unsigned=True), primary_key=True);
    time = Column(Float);
    sessions_id = Column(Integer(10, Unsigned=True), ForeignKey('sessions.id'));
    latitude = Column(Float, default=None);
    longitude = Column(Float, default=None);
    altitude = Column(Float, default=None);

    def __init__(self, time, latitide=None, longitude=None, altitude=None):
        self.time = time;
        self.latitude = latitide;
        self.longitude = longitude;
        self.altitude = altitude;
     
    @staticmethod
    def check(key):
        return type(key) == type("") and key.lower() in [
               "measurementpoint", "measurementpoints", 
               "measurement_point", "measurement_points"
               ];
    
    @staticmethod
    def inject(obj, session):
        if DEBUG:
            print "%s: input information: %s " % (TAG, obj);
            
        errors = {};
        preset = MeasurementPoint.__defaults__;
        preset.update(obj);

        # Perform errors check
        if (preset['time'] == None):
            errors['time'] = "Time of Measurement point couldn't have Null value, please check it";
 
        # Create measurement point element
        # DESIGNING_QUATION: Can be set latitude and longitude without altitude in Measurement points?
        toBePushed = MeasurementPoint(preset['time'], preset['latitude'], preset["longitude"], preset["altitude"]);
        
        # Perform connection session option with session into 'session_id' field
        scope = Scope.state(); 
           
        if DEBUG:
            print "%s: current scope %s" % (TAG, str(scope));
                    
        if scope.has_key("sessions_id"):
            toBePushed.sessions_id = scope["session_id"]
        else:
            pass
            #WARNING: "Session id for Measurement points have zero value, is this not mistake?";

        if (len(errors)):
            return session, obj, errors;
        
        session.add(toBePushed);
        session.flush();
        
        Scope.inject({"measurement_point_id": toBePushed.id}, None, Scope.level() - 0.5);

        if DEBUG:
            print "%s: %s" % (TAG, toBePushed);
        
        return session, obj, {};                            
 
    
    @staticmethod
    def tableName():
        return "MeasurementPoint"; 