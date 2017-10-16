
# @file: lers_reader.py
# @author: Abraham Dick
# @date: October 2017
# @desc: reads in files in the lers format

from dataset import Dataset

class LERS_Reader:


    def __init__(self, filename):
        self._filename = filename
        self._dataset = Dataset()

    def read_file(self):

        self._file = open(self._filename, 'r')

        for line in self._file:
            line.split()

            if line[0] == '<':
                print "found <"
            elif line[0] == '[':
                _attr = line.split()
                del _attr[0]
                del _attr[-1]

                self._dataset.decision = _attr[len(_attr)-1]

                del _attr[-1]

                self._dataset.attributes = _attr
            else:
                self._dataset.add_to_universe(line.split())



        




    def return_data(self):
        return self._dataset



