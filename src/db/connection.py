'''
Created on Nov 1, 2012

@author: weralwolf, elpiankova
'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DBConnection:
    __engine__ = None;
    def __init__(self, user, password, db_name, host='localhost', driver='mysql'):
        if (self.__engine__ == None):
            self.__engine__ = create_engine('%s://%s:%s@%s/%s' % (driver, user, password, host, db_name));

    def connection(self):
        return self.__engine__.connect(); 

    def execute(self, query):
        try:
            return self.connection().execute(query);
        except:
            return None;

    def session(self):
        # Session in this current case doesn't connected with promis db-table
        # `Session`, cause this one is a db-connection session object and uses for
        # <strike>good</strike> pushing data into db
        Session = sessionmaker(bind=self.__engine__);
        return Session();
