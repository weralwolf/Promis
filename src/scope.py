'''
Created on Nov 1, 2012

@author: weralwolf
'''

from math import floor

class Scope(object):

    # # Instance of Scope
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Scope, cls).__new__(cls, *args, **kwargs);
        return cls._instance;
    
    def __init__(self):
        """
         Initialize scope. 
        """
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

    @staticmethod
    def push(sub, level):
        """
            Push values into scope
            @param sub: dictionary of key-values needed to create other element
            @param level: level of current scope amendment  
        """
        self = Scope();
        
        if self._level_ < floor(float(level)):
            self._level_ = floor(float(level));
        
        if (self._order_.has_key(level)):
            self._order_[level].extend(sub.keys());
        else:
            self._order_[level] = sub.keys();

        for key in sub.keys():
            if (not self._container_.has_key(key)):
                self._container_[key] = [];
            self._container_[key].append(sub[key]);
    
    @staticmethod
    def pop(level= -1, justSkim=False):
        """
            Pop levels before {@link level} and restore the state of scope like 
            there was no such levels
            
            @param level: edge level of levels to be removed, if you leave it
                   as -1 it will be replaced by last an integer level
            
            @param justSkim: flag to perform skim level cleaning, which means
                   that you wouldn't remove half-integer levels to save some
                   special keys to provide database group pushing operation
            
        """
        self = Scope();
        if (level == -1):
            level = self._level_;
            
        for i in self._order_.keys():
            currentLevel = float(i);
            
            # Check common condition for any kind of pop operation
            if (currentLevel <= self._level_):
                continue;
            
            # Check skim-kind condition 
            if (justSkim and floor(currentLevel) == self._level_):
                continue;
            
            # Level which should be removed from scope
            removable = self._order_[i];
            
            if (not len(removable)):
                keys = removable.pop();
                for key in keys:
                    self._container_[key].pop();
                    
            del self._order_[i];
    
    @staticmethod
    def state():
        """
            Calculate current state of scope from all last added data
            @return: dictionary of key:value
        """
        self = Scope();
        state = {};
        for key in self._container_.keys():
            state[key] = self._container_[key][len(self._container_[key]) - 1];
