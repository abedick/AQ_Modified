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


    def print_dataset(self, _dataset):
        print "\n\n\nDataset Information"
        print "Data set is onyl symbolic: " + str(_dataset.symbolic)
        print "Decision name: " + str(_dataset.decision)
        print "Number of attributes: " + str(len(_dataset.attributes))
        print "Number of cases in universe: " + str(len(_dataset.universe))
        print "\n\n\n"

        print _dataset.attributes
        
        for i in range(0,len(_dataset.universe)):
            print _dataset.universe[i]


    def check_consistency(self):
        # compute concepts

        _Decisions = []

        # gather all the decisions present in the dataset
        for i in range (0, len(self._dataset.universe)):
            _case_decision = len(self._dataset.universe[0]) - 1
            _Decisions.append(self._dataset.universe[i][_case_decision])
        
        # filter out the duplicates 
        _list_decisions = list(set(_Decisions))

        # build concepts
        _concept_lists = []

        for i in range(0, len(_list_decisions)):
            # _concept_lists[i] = _list_decisions[i]
            _concept_lists.append([_list_decisions[i], []])

            for k in range(0,len(self._dataset.universe)):
                _case_decision = len(self._dataset.universe[0]) - 1
                if self._dataset.universe[k][_case_decision] == _list_decisions[i]:
                    _concept_lists[i][1].append(k)

        self._dataset.d_star = _concept_lists

        print self._dataset.d_star
