'''
Created on Nov 1, 2012

@author: weralwolf
'''

from sqlalchemy import Column, Integer, String, DECIMAL #, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.orm import relationship, backref

Base = declarative_base();

class PITable(Base):
    @staticmethod
    def check(key):
        return False;
    
    @staticmethod
    def inject(scope, obj, session):
        return (scope, {});

class Satellite(PITable):
    __tablename__ = 'satellites';
    
    @staticmethod
    def check(key):
        return key == 'satellite' or key == 'satellites';
    
    @staticmethod
    def inject(scope, obj, session):
        data = {
            'title': '',
            'description': ''
        };
        data.update(obj);

        s = Satellite();
        s.title = obj['title'];
        s.description = obj['description'];
        # save into db_session

        children = {
            'device': None,
            'devices': None,
            'session': None,
            'sessions': None
        };
        
        children.update(obj);
        return (scope, children);
        
    def __repr__(self):
        return "<Satellite('%s', '%p')>" % (self.title, self);

class Device(Base):
    __tablename__ = 'devices';

    id = Column(Integer(unsigned=True), primary_key=True);
    title = Column(String);
    description = Column(String);
    frequency = Column(DECIMAL);

    def __init__(self, device_data):
        self.title = device_data['title'];
        self.description = device_data['description'];
        self.frequency = device_data['frequency'];

    def __repr__(self):
        return "<Device('%s','%s', '%s')>" % (self.title, self.secription, str(self.frequency));
        
class Session(PITable):
    __tablename__ = 'sessions';
    
    @staticmethod
    def check(key):
        return False;
    
    @staticmethod
    def inject(scope, obj, session):
        return (scope, {});

class SessionOption(PITable):
    __tablename__ = 'session_options';
    
    @staticmethod
    def check(key):
        return False;
    
    @staticmethod
    def inject(scope, obj, session):
        return (scope, {});        