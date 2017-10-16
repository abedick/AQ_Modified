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
        self._dataset = Dataset()

        self._dataset.attributes = [2,3,4]

        # print _dataset.attributes

        self._dataset.universe = [4,5,6]

        # print _dataset.universe

        self._dataset.add_to_universe(5)

        # print _dataset.universe

        self.print_dataset()


#     # # Grab a filename from the user
#     # _filename = raw_input("Please enter a filename of a LERS file format: ")

#     # # Start the reader
#     # _reader = LERS_Reader(_filename)

#     # # Grab the data from the file
#     # _data = _reader.return_data()

#     # print _data

    def print_dataset(self):
        print self._dataset.attributes
        
        for i in range(0,len(self._dataset.attributes)):
            print self._dataset.universe[i]