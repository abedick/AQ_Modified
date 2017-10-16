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
        self.print_dataset(_reader.return_data())


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