'''
Created on Nov 1, 2012

@author: weralwolf
'''

from conf.local import DEBUG

from common import Singleton

from math import floor

from db.injectors import injectors
"""
    @todo: create methods pushLevel, pullLevel to automate scope work, delegated
           to next release cause of over-engineering fear
"""

TAG = "db.scope"

@Singleton
class _Scope:
    """
    Scope is a singleton DB primary-keys keeper.
    
    Entities
    =============
    Contributor is a JSON-file which contains satellites data information to be 
    pushed into database.
    
    Contributor-immutable tables is a tables which couldn't be edited by 
    contributor, but only by database-manager. Any contributed data should be
    connected with entities from immutable tables.
    
    List of immutable tables: satellites, devices, channels, parameters, units.
    
    Contributor-mutable tables is a tables where JSON-contributed data would be
    stored. All mutable entities dependent on entities from immutable tables.
    
    List of mutable tables: sessions, sessions_options, measurement_points,
    measurements.      
    
    DB primary-keys is a primary keys of all contributor-immutable tables or 
    keys of contributor-mutable tables required by dependencies of other 
    contributor-mutable tables.
    
    
    Primary-keys structuring
    =============
    All PK structured by levels of data-inheritance. Each level determined by
    levels of JSON-data inheritance and executed injection into database.
    
    There two types of levels integer and half-integer. Integer levels is a
    levels made by JSON-data inheritance. Half-integer levels is determined by
    db-injections. 
    
    
    Tables structure
    =============
    @ref{db.__init__}
    
    
    Scope filling
    =============
    Scope would be filled in two ways: manually and automatically.
    
    Manual filling could be done with JSON-nodes placed in any place of 
    JSON-data. Scope-nodes structure:
    "scope": {
        "tablename_pkname": "pkvalue",
        "tablename_pkname": {
            "othertablename:fieldname": "fieldvalue",
            "fieldname": "fieldvalue",
            ...
        }
        ...
    }
    
    where:
        "tablename" - name of immutable or mutable table,
        "pkname" -  could be "title" or "id",
        "pkvalue" - value of pk which,
        "fieldname" - name of table field name.
    
    Example:
    "scope": {
        "satellites_title": "DE2",
        "devices_title": "idm",
        "channels_title": "He",
        "parameters_title": "density"
        "sessions_id": {
            "iEnd": "458787546598",
            "sessions_options:title": "mode",
            "sessions_options:value": "scanning"
        }
    }
    
    Automatic filling would be made by processing script and all values would be
    pushed into half-integer levels.
    
    Scope cleaning <fix> meaning of flag </fix>
    =============
    Elements of scope would be pulled out by request and all old values would be
    restored. If you need to save some values on level upper to transfer them
    into sibling nodes, you should add special flag:
    
    "flag:up-transfer": "True"
    
    , but default is "False"-value.
    
    PK list-values
    =============
    List values would be used to work out two problems:
    1. Many-to-many relations, to connect tables
        Sessions could be connected with many channels, that's why you may need
        to define a few channels sessions would be connected with, like:
            "channels_title": ["idm", "lapi", "gas_wats", "rpa"]

    2. Bulk-injections, then we want to insert a lot of measures at once
        It much more easier to make bulk-injection of data instead one-by-one
        injections. That's why measuremnt_points ids should be saved to be used
        during measurement injections, they would be saved on half-integer level
        in a form of list.
    
    @bug: parameters should have many-to-many relation with channels
    @todo: JSON-should be used to extract read-only data
    @todo: any JSON should give respond
    """

    def __init__(self):
        """
         Initialize scope
        """
        if DEBUG:
            print "%s: init()" % (TAG);
        # Dictionary of lists of values which is ordered by levels.
        # Dictionary keys is a names of scope values
        self._container_ = {};
        
        # Dictionary of lists of levels of penetration ordered by levels
        # Lists contains keys which was overwritten/added on each level
        # Levels could be integer and half-integer.
        # Integer level indicates `scope` element injection, literally then
        #     we met a user manually-registered element
        # Half-integer level indicates non-direct injections as a result of
        #     pushing some elements into data base
        self._order_ = {};
        
        # Current highest integer level
        self._level_ = 0.;
        
    def inject(self, obj, session, transfer = False):
        """
        Push values into scope
        @param obj: dictionary of key-values needed to create other element
        @param session: should be null, present just respective to parent class
        @param level: level of current scope amendment   
        """
        if DEBUG:
            print "%s: inject()" % (TAG);
        
        level = self._level_;
        
        if (transfer):
            level -= 0.5;
        
        if self._order_.has_key(level):
            self._order_[level].extend(obj.keys());
        else:
            self._order_[level] = obj.keys();

        for key in obj.keys():
            value = None;
            # before we get value we need to be sure what it's already value 
            # but not a search criteria
            for injector in injectors:
                value = injector.find(obj[key]);
                
            if value:
                if not self._container_.has_key(key):
                    self._container_[key] = [];
                    
                if DEBUG:
                    print "%s: + [level: %i] %s = %s" % (TAG, level, 
                                                         str(key), 
                                                         str(value));
                self._container_[key].append(value);
        
        return session, {}, {};
    
    def pushLevel(self):
        if DEBUG:
            print "%s: pushLevel()" % (TAG);
            
        self._level_ += 1;
        
    def popLevel(self):
        if DEBUG:
            print "%s: popLevel()" % (TAG);
            
        self._level_ -= 1;
        self.pop();
    
    def pop(self):
        """
        Pop levels before {@link level} and restore the state of scope like 
        there was no such levels
        """
        
        if DEBUG:
            print "%s: pop()[_level_=%i]" % (TAG, self._level_);
        
        for i in self._order_.keys():
            currentLevel = float(i);
            
            # Check common condition for any kind of pop operation
            if DEBUG:
                print "%s: comparing levels %f < %i" % (TAG, currentLevel, self._level_);
                
            if currentLevel < self._level_:
                continue;
            
            removable = self._order_[i];
            
            if DEBUG:
                print "%s: removable - %s" % (TAG, str(removable));
            
            if len(removable):
                for key in removable:
                    if DEBUG:
                        print "%s: - [level: %i] %s" % (TAG, self._level_, str(key));
                    self._container_[str(key)].pop();
                
                    
            del self._order_[i];
            
            self._level_ = self._level_ - 1.;
    
    def state(self):
        """
        Calculate current state of scope from all last added data
        @return: dictionary of key:value
        """
        state = {};
        
        if len(self._order_):
            for key in self._container_.keys():
                state[key] = self._container_[key][len(self._container_[key]) - 1];
        
        return state;

    def level(self):
        """
        @return: current scope level
        """
        return self._level_;
    
    def check(self, name):
        return name in ['scope'];
    
    def tableName(self):
        return "Scope";
    
    @staticmethod
    def find(options):
        return None;

Scope = _Scope.Instance();
