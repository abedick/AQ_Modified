# @file: controlelr.py
# @author: Abraham Dick
# @date: October 2017
# @desc: Main controller for EECS 690 Programming Project


from dataset import Dataset
from lers_reader import LERS_Reader
from aq import AQ
from ruleset_printer import Printer

from itertools import izip_longest

class Controller(object):

    def __init__(self):
        self._dataset = Dataset()
        self._aq = AQ()
        self._results = None
        self._printer = Printer()

    def run(self):
        # Grab a filename from the user
        # _filename = raw_input("Please enter a filename of a LERS file format: ")

        _filename = "jgbdata6.d"

        # Start the reader
        _reader = LERS_Reader(_filename)

        _reader.read_file()

        

        # Grab the data from the file
        self._dataset = _reader.return_data()

        ##
        ## Preprocessing
        ##

        # Check if the data is symbolic or numeric
        if not(self._dataset.symbolic):
            self.compute_numeric()

        self.calculate_blocks()
        self.check_consistency_fast()
        self.get_attribute_range()

        # self.print_dataset(self._dataset)

        self._results = self._aq.run(self._dataset)

        self._printer.printer(self._results,self._dataset.attributes[1][0])


    def print_dataset(self, _dataset):
        print "\n\n\nDataset Information"
        print "---------------------------------------------------------"
        print "Data set is only symbolic: " + str(_dataset.symbolic)
        print "Data set is consistent: " + str(_dataset.consistent)
        print "{d}*: " + str(_dataset.d_star)
        print "Number of attributes: " + str(len(_dataset.attributes[0]))
        print "All Attributers: " + str(_dataset.attributes[0])
        print "Attribute Ranges: " + str(_dataset.attribute_range)
        print "Decision Name: " + str(_dataset.attributes[1][0])
        print "Number of cases in universe: " + str(len(_dataset.universe))
        print "--------------------------------------------------------"
        print str(_dataset.attributes)
        for i in range(0,len(_dataset.universe)):
            print str(_dataset.universe[i])

    ###
    ### Calculates the concept blacks {d}*
    ###
    def calculate_blocks(self):
        _case_decision = []

        for i in range(0,len(self._dataset.universe)):
            if self._dataset.universe[i][1] not in _case_decision:
                _case_decision.append(self._dataset.universe[i][1])

        _block = []
        for i in _case_decision:
            _block.append([[i[0]],[]])

        for i in range(0,len(self._dataset.universe)):
            _placed = False
            while not _placed:
                for k in range(0,len(_case_decision)):
                    if self._dataset.universe[i][1] == _case_decision[k]:
                        _block[k][1].append(i)
                        _placed = True
        self._dataset._d_star = _block

    ###
    ### Quickly checks to see if the dataset is consistent
    ### Terminates as soon as first inconsistency is found
    ###
    def check_consistency_fast(self):
        _case_decision = len(self._dataset.universe[0]) - 1

        for i in range(0,len(self._dataset.universe)):
            _test_case = self._dataset.universe[i]
            _test_case_decision = _test_case[_case_decision]
            _test_case = _test_case[:-1]

            for k in range(0,len(self._dataset.universe)):
                _compare_case = self._dataset.universe[k]
                _compare_case_decision = _compare_case[_case_decision]
                _compare_case = _compare_case[:-1]

                if ((i != k) and (_test_case == _compare_case) and (_test_case_decision != _compare_case_decision)):
                    self._dataset.consistent = False
                    break

    ###
    ### For each attribute, get all possible values
    ### This will be helpful for building rules w/out negation
    ###
    def get_attribute_range(self):
        _attribute_sets = []

        for i in range(0,len(self._dataset.attributes[0])):
            _attribute_sets.append([])

        for i in range(0,len(self._dataset.universe)):
            for k in range(0,len(self._dataset.attributes[0])):
                _attribute_sets[k].append(self._dataset.universe[i][0][k])

        for i in range(0,len(_attribute_sets)):
            _attribute_sets[i] = list(set(_attribute_sets[i]))

        self._dataset.attribute_range = _attribute_sets
    
    ###
    ### If a numeric attribute was read in from file, compute_numeric
    ### recalculates the attribute according to cutpoint method
    ###
    def compute_numeric(self):
        _number_attributes = []

        # Check each attribute and if it is a type float, add the index number to the array.
        # This should have been stored as such from LERS_Reader at data read in time.
        for i in range(0,len(self._dataset.universe[0][0])):
            try:
                float(self._dataset.universe[0][0][i])
                _number_attributes.append(i)
            except ValueError:
                continue
            
        _attribute_values = []

        # for each attribute that is numberic, append each unique case to _attribute_values[i]
        for i in range(0,len(_number_attributes)):
            _attribute_values.append([_number_attributes[i],[]])

            for k in range(0,len(self._dataset.universe)):
                if self._dataset.universe[k][0][_number_attributes[i]] not in _attribute_values[i][1]:
                    _attribute_values[i][1].append(self._dataset.universe[k][0][_number_attributes[i]])

            _attribute_values[i][1] = sorted(_attribute_values[i][1])

        _new_attributes = []

        # Create the attribute attributes that were numeric and compute their ranges and append them as block to _new_attributes
        for i in range(0,len(_attribute_values)):
            _set = _attribute_values[i][1]
            _new_attributes.append([])

            for k in range(1,len(_set)):
                _new_value = (_set[k-1]+_set[k])/2
                _base_string = self._dataset.attributes[0][_attribute_values[i][0]]
                _new_name = str(_base_string) + "_" + str(_new_value)

                _lower_range = (_set[0],_new_value)
                _upper_range = (_new_value,max(_set))
                _range = (_lower_range,_upper_range)

                _params = [_new_name,_range,[]]
                _new_attributes[i].append(_params)
        _updated_uni = []
        
        # Create a multidimensional list, one dim for each of the new attribute blocks
        # and construct the new values on a universe case by case order
        for i in range(0,len(self._dataset.universe)): 
            _updated_uni.append([])
            for k in range(0,len(_new_attributes)):
                _new_attribute_block = []
                for l in range(0,len(_new_attributes[k])):
                    _test_value =  self._dataset.universe[i][0][_number_attributes[k]]
                    _lower = _new_attributes[k][l][1][0]
                    _upper = _new_attributes[k][l][1][1]

                    if(_test_value >= _lower[0] and _test_value <= _lower[1]):
                        _new_value = str(_lower[0]) + ".." + str(_lower[1])
                    else:
                        _new_value = str(_upper[0]) + ".." + str(_upper[1])
                    _new_attribute_block.append(_new_value)

                _new_attribute_block = _new_attribute_block[::-1]
                _updated_uni[i].append(_new_attribute_block)

            _updated_uni[i] = _updated_uni[i][::-1]

        # Delete the old columns and insert the new symbolic cases
        _number_attributes = _number_attributes[::-1]
        _names = []

        for i in range(0,len(_new_attributes)):
            _name_block = []

            for j in _new_attributes[i]:
                _name_block.append(j[0])

            _name_block = _name_block[::-1]
            _names.append(_name_block)
        _names = _names[::-1]

        _count = 0

        # add the new symbolic attribute names
        for k in _number_attributes:
            if( (k+1) >= len(self._dataset.attributes[0])):
                _names[_count] = _names[_count][::-1]
                for l in _names[_count]:
                    self._dataset.attributes[0].append(l)
            else:
                for l in _names[_count]:
                    self._dataset.attributes[0].insert(k+1,l)

            # delete the old numeric attribute
            del self._dataset.attributes[0][k]

            # Keeping track of indicies
            _count = _count+1

        # Update the rows of the universe with each new case
        for i in range(0,len(self._dataset.universe)):
            _count = 0
            for k in _number_attributes:
                # add the new symbolic block
                if( (k+1) >= len(self._dataset.universe[i][0])):
                    _updated_uni[i][_count] = _updated_uni[i][_count][::-1]
                    for l in _updated_uni[i][_count]:
                        self._dataset.universe[i][0].append(l)
                else:
                    for l in _updated_uni[i][_count]:
                        self._dataset.universe[i][0].insert(k+1,l)

                # delete the old numeric entry
                del self._dataset.universe[i][0][k]

                # Keeping track of indicies
                _count = _count+1