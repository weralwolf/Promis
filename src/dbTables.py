'''
Created on Nov 1, 2012

@author: weralwolf
'''

from sqlalchemy import Column, Integer, String, DECIMAL  # , DateTime, ForeignKey
# from sqlalchemy.orm import relationship, backref

from injectiveTable import InjectiveTable
        
class Session(InjectiveTable):
    __tablename__ = 'sessions';
    
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
    __tablename__ = 'session_options';
    
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
    __tablename__ = 'measurement_points';
    
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
