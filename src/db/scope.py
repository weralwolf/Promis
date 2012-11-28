'''
Created on Nov 1, 2012

@author: weralwolf
'''

from conf.local import DEBUG

from common import Singleton

from math import floor
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
    
    List of immutable tables: satellites, devices, channels, parameters.
    
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
    levels made by JSON-data inheritance. Half-integer levels is determines by
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
    
    Scope cleaning
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
        # # Dictionary of lists of values which is ordered by levels.
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
        self._level_ = 0;

    def inject(self, obj, session, level = -1):
        """
            Push values into scope
            @param obj: dictionary of key-values needed to create other element
            @param session: should be null, present just respective to parent class
            @param level: level of current scope amendment   
        """
        if DEBUG:
            print "%s: inject()" % (TAG);
        
        if level == -1:
            level = self._level_ + 1;
        
        if self._level_ < floor(float(level)):
            self._level_ = floor(float(level));
        
        if self._order_.has_key(level):
            self._order_[level].extend(obj.keys());
        else:
            self._order_[level] = obj.keys();

        for key in obj.keys():
            if not self._container_.has_key(key):
                self._container_[key] = [];
                
            if DEBUG:
                print "%s: + [level: %i] %s = %s" % (TAG, self._level_, str(key), str(obj[key]));
            self._container_[key].append(obj[key]);
        
        return session, {}, {};
    
    def pop(self, level= -1, justSkim=False):
        """
            Pop levels before {@link level} and restore the state of scope like 
            there was no such levels
            
            @param level: edge level of levels to be removed, if you leave it
                   as -1 it will be replaced by last an integer level
            
            @param justSkim: flag to perform skim level cleaning, which means
                   that you wouldn't remove half-integer levels to save some
                   special keys to provide database group pushing operation
            
        """
        
        if DEBUG:
            print "%s: pop(level=%s, justSkim=%s)[_level_=%i]" % (TAG, str(level), str(justSkim), self._level_);
        
        if level == -1:
            level = self._level_;
            
        for i in self._order_.keys():
            currentLevel = float(i);
            
            # Check common condition for any kind of pop operation
            if DEBUG:
                print "%s: comparing levels %f < %i" % (TAG, currentLevel, level);
                
            if currentLevel <= level:
                continue;
            
            # Check skim-kind condition
            if DEBUG:
                print "%s: comparing skim-levels %f == %i" % (TAG, floor(currentLevel), level);
            if justSkim and floor(currentLevel) == level:
                continue;
            
            # Level which should be removed from scope
            if DEBUG:
                print "%s: level %i going to be removed" % (TAG, i);

            removable = self._order_[i];
            
            if DEBUG:
                print "%s: removable - %s" % (TAG, str(removable));
            
            if len(removable):
                for key in removable:
                    if DEBUG:
                        print "%s: - [level: %i] %s" % (TAG, level, str(key));
                    self._container_[str(key)].pop();
                
                    
            del self._order_[i];
            
            self._level_ = level;
    
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

Scope = _Scope.Instance();