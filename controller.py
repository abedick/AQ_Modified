# @file: controlelr.py
# @author: Abraham Dick
# @date: October 2017
# @desc: Main controller for EECS 690 Programming Project


from dataset import Dataset
from lers_reader import LERS_Reader

class Controller(object):

    def __init__(self):
        self._dataset = Dataset()

    def run(self):
        # Grab a filename from the user
        # _filename = raw_input("Please enter a filename of a LERS file format: ")

        _filename = "test_data.d"
        print _filename

        # Start the reader
        _reader = LERS_Reader(_filename)

        _reader.read_file()

        # Grab the data from the file
        self._dataset = _reader.return_data()
        # self.print_dataset(_reader.return_data())

        self.check_consistency()

        self.print_dataset(self._dataset)


    def print_dataset(self, _dataset):
        print "\n\n\nDataset Information"
        print "---------------------------------------------------------"
        print "Data set is only symbolic: " + str(_dataset.symbolic)
        print "Data set is consistent: " + str(_dataset.consistent)
        print "{d}*: " + str(_dataset.d_star)
        print "A*: " + str(_dataset.a_star)
        print "Number of attributes: " + str(len(_dataset.attributes))
        print "Number of cases in universe: " + str(len(_dataset.universe))
        print "--------------------------------------------------------"

        print _dataset.attributes
        
        for i in range(0,len(_dataset.universe)):
            print _dataset.universe[i]


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

                if((i != k) and (_test_case == _compare_case) and (_test_case_decision != _compare_case_decision) and not(k in _covered)):
                    _universe_cases[i].append(k)
                    _covered.append(k)
                    self._dataset.consistent = False
                else:
                    if (not([i] in _universe_cases) and (i != k) and not(i in _covered)):
                        _covered.append(i)
                        _universe_cases.append([i])

        self._dataset.a_star = _universe_cases
                


        # for i in range(0,len(self._dataset.universe)):
        #     _test_case = self._dataset.universe[i]
        #     _test_case_decision = _test_case[_case_decision]
        #     _test_case = _test_case[:-1]

        #     for k in range(0,len(self._dataset.universe)):
        #         _compare_case = self._dataset.universe[k]
        #         _compare_case_decision = _compare_case[_case_decision]
        #         _compare_case = _compare_case[:-1]

        #         if ((i != k) and (_test_case == _compare_case) and (_test_case_decision != _compare_case_decision)):
        #             self._dataset.consistent = False