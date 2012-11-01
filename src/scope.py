'''
Created on Nov 1, 2012

@author: weralwolf
'''

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
        for key in self._container_.keys():
            state[key] = self._container_[key][len(self._container_[key]) - 1];
