# @file: dataset.py
# @author: Abraham Dick
# @date: October 2017
# @desc: Object to encapsulate a dataset of LERS data



## _attributes is the list of attributes associated with all cases on the _universe
## 


class Dataset(object):

    def __init__(self):
        self._name = "Dataset"
        self._attributes = []
        self._universe = []

    @property
    def attributes(self):
        return self._attributes

    @attributes.setter
    def attributes(self, value):
        self._attributes = value
    
    @property
    def universe(self):
        return self._universe

    @universe.setter
    def universe(self, value):
        self._universe = value

    def add_to_universe(self, value):
        self._universe.append(value)