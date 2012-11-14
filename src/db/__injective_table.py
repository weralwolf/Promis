'''
Created on Nov 14, 2012

@author: weralwolf
'''

class InjectiveTable:
    """
        Table which could be easily injected into database
    """
    
    @staticmethod
    def check(key):
        """
            Verifying key to affiliation to this kind of date this table could
            process
            @param key: key which should be verified 
            @return: boolean indicator
        """
        return False;
    
    @staticmethod
    def inject(obj, session):
        """
            Injecting exact data into data base
            @param obj: container of all information to be parsed for creation 
                   of table entry.
            @param session: data base session which would be used to inject
                   collected data 
        """
        return {};
    
    @staticmethod
    def tableName():
        """
            Name of data destination
        """
        return "InjectiveTable";
