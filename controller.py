# @file: controlelr.py
# @author: Abraham Dick
# @date: October 2017
# @desc: Main controller for EECS 690 Programming Project


from dataset import Dataset
from lers_reader import LERS_Reader

from itertools import izip_longest

class Controller(object):

    def __init__(self):
        self._dataset = Dataset()

    def run(self):
        # Grab a filename from the user
        # _filename = raw_input("Please enter a filename of a LERS file format: ")

        _filename = "test_data4.d"
        print _filename

        # Start the reader
        _reader = LERS_Reader(_filename)

        _reader.read_file()

        # Grab the data from the file
        self._dataset = _reader.return_data()

        # Check if the data is symbolic or numeric
        if not(self._dataset.symbolic):
            self.compute_numeric()

        # check for consistency
        self.check_consistency()
        self.check_consistency_fast()

        self.print_dataset(self._dataset)


    def print_dataset(self, _dataset):
        print "\n\n\nDataset Information"
        print "---------------------------------------------------------"
        print "Data set is only symbolic: " + str(_dataset.symbolic)
        print "Data set is consistent: " + str(_dataset.consistent)
        print "{d}*: " + str(_dataset.d_star)
        print "A*: " + str(_dataset.a_star)
        print "Number of attributes: " + str(len(_dataset.attributes))
        print "All Attributers: " + str(_dataset.attributes)
        print "Decision Name: " + str(_dataset.decision)
        print "Number of cases in universe: " + str(len(_dataset.universe))
        print "--------------------------------------------------------"

        print str(_dataset.attributes) + " " + str([_dataset.decision])
        
        for i in range(0,len(_dataset.universe)):
            print str(_dataset.universe[i]) # + " " + str(self._dataset.decision[i])


    def check_consistency(self):
        # compute concepts

        _Decisions = []
        _case_decision = len(self._dataset.universe[0]) - 1

        # Calculate {d}*

        # gather all the decisions present in the dataset
        for i in range (0, len(self._dataset.universe)):
            _case_decision = len(self._dataset.universe[0]) - 1
            _Decisions.append(self._dataset.universe[i][_case_decision])
        
        # filter out the duplicates 
        _list_decisions = list(set(_Decisions))

        # build concepts
        _concept_lists = []

        for i in range(0, len(_list_decisions)):
            _concept_lists.append([_list_decisions[i], []])

            for k in range(0,len(self._dataset.universe)):
                _case_decision = len(self._dataset.universe[0]) - 1
                if self._dataset.universe[k][_case_decision] == _list_decisions[i]:
                    _concept_lists[i][1].append(k)

        # assign d* to the dataset
        self._dataset.d_star = _concept_lists

        # calculate A*

        _universe_cases = []
        _covered = []

        for i in range(0,len(self._dataset.universe)):
            _test_case = self._dataset.universe[i]
            _test_case_decision = _test_case[_case_decision]
            _test_case = _test_case[:-1]

            for k in range(0,len(self._dataset.universe)):
                _compare_case = self._dataset.universe[k]
                _compare_case_decision = _compare_case[_case_decision]
                _compare_case = _compare_case[:-1]

                if((i != k) and (_test_case == _compare_case) and not(k in _covered)):
                    try:
                        _universe_cases[i].append(k)
                    except IndexError:
                        ind = len(_universe_cases)-1

                        _universe_cases[ind].append(k)
                    _covered.append(k)
                else:
                    if (not([i] in _universe_cases) and (i != k) and not(i in _covered)):
                        _covered.append(i)
                        _universe_cases.append([i])

        self._dataset.a_star = _universe_cases

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
    
    def compute_numeric(self):
        print "\n\nComputing cutpoints"

        _number_attributes = []

        for i in range(0,len(self._dataset.universe[0])):

            # Check each attribute for if it is stored as a float
            # This should have been stored as such from LERS_Reader at data read in
            try:
                float(self._dataset.universe[0][i])
                _number_attributes.append(i)
            except ValueError:
                continue
                
        _attribute_values = []
        # for each attribute that is numberic...
        for i in range(0,len(_number_attributes)):
            _attribute_values.append([_number_attributes[i],[]])

            #for each case of the universe
            for k in range(0,len(self._dataset.universe)):
                _attribute_values[i][1].append(self._dataset.universe[k][_number_attributes[i]])


        _new_attributes = []

        for i in range(0,len(_attribute_values)):

            _new_attributes.append([])
            
            _set = sorted(list(set(_attribute_values[i][1])))

            for k in range(1,len(_set)):
                _new_value = (_set[k-1]+_set[k])/2
                _j = _attribute_values[i][0]
                _new_name = str(self._dataset.attributes[_j])+ "_" + str(_new_value)

                _lower_range = _set[0],_new_value
                _upper_range = _new_value,max(_set)

                _new_attributes[i].append([_new_name,[_lower_range,_upper_range],[]])
                _set.append(_new_value)

            _attribute_values[i].append(sorted(_set))

        # For each case of the univesre
        for i in range(0,len(self._dataset.universe)):

            # For each of the numerical columns
            for k in range(0,len(_new_attributes)):

                # for each of the new attributes
                for l in range(0,len(_new_attributes[k])):
                    _case_set = set([self._dataset.universe[i][_number_attributes[k]]])
                    _lower_set = set(range(_new_attributes[k][l][1][0][0],_new_attributes[k][l][1][0][1]+1))

                    if _case_set.issubset(_lower_set):
                        _new_attributes[k][l][2].append(str(_new_attributes[k][l][1][0][0]) + ".." + str(_new_attributes[k][l][1][0][1]))
                    else:
                        _new_attributes[k][l][2].append(str(_new_attributes[k][l][1][1][0]) + ".." + str(_new_attributes[k][l][1][1][1]))

        _matrix = []

        for k in range(0,len(_new_attributes)):

            for i in range(0,len(_new_attributes[k])):
                _matrix.append(_new_attributes[k][i][2])

        _cases =  [[i for i in element] for element in list(izip_longest(*_matrix))]

        for i in range(0,len(_cases)):
            _cases[i] = _cases[i][::-1]
        _number_attributes = _number_attributes[::-1]

        print _new_attributes[0][1]


        _attribute_names = []

        for k in range(0,len(_new_attributes)):
            for i in _new_attributes[k]:
                _attribute_names.append(i[0])

            _attribute_names = _attribute_names[::-1]

            print _attribute_names
        

        for i in range(0,len(self._dataset.universe)):
            for k in _number_attributes:
                del self._dataset.universe[i][k]


        for k in _number_attributes:
            del self._dataset.attributes[k]


        for j in _number_attributes:
            for i in range(0,len(self._dataset.universe)):
                for k in range(0,len(_cases[i])):
                    self._dataset.universe[i].insert(j,_cases[i][k])

            for i in range(0,len(_new_attributes)):
                for k in range(0,len(_new_attributes[i])):
                    self._dataset.attributes.insert(j,_attribute_names[k])
    
