'''
Created on Nov 1, 2012

@author: weralwolf
'''

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
