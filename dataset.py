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
        self._decision = None
        self._universe = []
        self._attribute_range = []
        self._symbolic = True
        self._d_star = None
        self._a_star = None
        self._consistent = True

    @property
    def attributes(self):
        return self._attributes

    @attributes.setter
    def attributes(self, value):
        self._attributes = value

    @property
    def decision(self):
        return self._decision

    @decision.setter
    def decision(self, value):
        self._decision = value
    
    @property
    def universe(self):
        return self._universe

    @universe.setter
    def universe(self, value):
        self._universe = value

    def add_to_universe(self, value):
        self._universe.append(value)

    @property
    def symbolic(self):
        return self._symbolic

    @symbolic.setter
    def symbolic(self, value):
        self._symbolic = value

    @property
    def d_star(self):
        return self._d_star

    @d_star.setter
    def d_star(self, value):
        self._d_star = value

    @property
    def a_star(self):
        return self._a_star

    @a_star.setter
    def a_star(self, value):
        self._a_star = value

    @property
    def consistent(self):
        return self._consistent

    @consistent.setter
    def consistent(self, value):
        self._consistent = value

    @property
    def attribute_range(self):
        return self._attribute_range

    @attribute_range.setter
    def attribute_range(self, value):
        self._attribute_range = value