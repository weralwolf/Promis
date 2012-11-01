############### DB CONNECTION ##################################################

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DBConnection:
    __engine__ = None;
    def __init__(self, user, password, db_name, host='localhost', driver='mysql'):
        if (DBConnection.__engine__ == None):
            DBConnection.__engine__ = create_engine('%s://%s:%s@%s/%s' % (driver, user, password, host, db_name));

    def connection(self):
        return DBConnection.__engine__.connect(); 

    def execute(self, query):
        try:
            return self.connection().execute(query);
        except:
            return None;

    def session(self):
        Session = sessionmaker(bind=self.__engine__);
        return Session();

############### SCOPE ##########################################################
class Scope(object):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Scope, cls).__new__(cls, *args, **kwargs);
        return cls._instance;
    
    def __init__(self):
        self._container_ = {};
        self._order_ = [];

    @staticmethod
    def push(sub):
        self = Scope();
        self._order_.append(sub.keys());
        for key in sub.keys():
            if (not self._container_.has_key(key)):
                self._container_[key] = [];
            self._container_[key].append(sub[key]);
    
    @staticmethod
    def pop():
        self = Scope();
        if (not len(self._order_)):
            keys = self._order_.pop();
            for key in keys:
                self._container_[key].pop();
    
    @staticmethod
    def state():
        self = Scope();
        state = {};
        for i in self._container_.keys():
            state[i] = self._container_[key][len(self._container_[key]) - 1];
    

############### DB TABLES ######################################################

from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base();

class PITable(Base):
    @staticmethod
    def check(key):
        return false;
    
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
            "title": "",
            "description": ""
        };
        data.update(obj);

        s = Satellite();
        s.title = obj["title"];
        s.description = obj["description"];
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
        return "<Satellite(%s, %p)>" % (self.title, self);

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
        return false;
    
    @staticmethod
    def inject(scope, obj, session):
        return (scope, {});

class SessioOption(PITable):
    __tablename__ = 'session_options';
    
    @staticmethod
    def check(key):
        return false;
    
    @staticmethod
    def inject(scope, obj, session):
        return (scope, {});
    
############### ALGO ###########################################################

import json;
data = json.load(open("example.json"));

# List of classes which could be used as
__classes__ = [Satellite, Device, Session, SessionOption];

__connection__ = DBConnection('root', 'littlelover', 'de2', 'localhost', 'mysql');

"""
@param key: element-name of some list or dictionary which should be processed
@param obj: element-value which should be processed
"""
def process(key, obj, session=None):
    __session = None;
    __emitter = False;
    __new_scope = False;

    if (session == None):
        __session = __connection__.session();
        __emitter = True;
    else:
        __session = session;

    if (obj == None) :
        return;

    # process list of objects with same key
    if (type(obj) == type([])):
        for i in obj:
            process(key, i);
    # process dictionary of multiple objects 
    elif (type(obj) == type({})):
        for i in obj.keys():
            
            if (i == "scope"):
              Scope.push(obj);
              __new_scope = True;
            
            for i in __classes__:
                if (i.check(key)):
                    _scope, _children = i.inject(obj, scope, __session__);
                    for i in _children.keys():
                        process(i, i[key]);
                    break;
                
    if (__emitter) :
        __session.save();
        __session.close();
    
    if (__new_scope):
        Scope.pop();
    return;

