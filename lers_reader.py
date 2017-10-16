
# @file: lers_reader.py
# @author: Abraham Dick
# @date: October 2017
# @desc: reads in files in the lers format

from dataset import Dataset

import numbers
import decimal

class LERS_Reader:


    def __init__(self, filename):
        self._filename = filename
        self._dataset = Dataset()

    def read_file(self):

        self._file = open(self._filename, 'r')

        for line in self._file:

            __data_row = line

            # Filter out comments in a line            
            head, sep, tail = __data_row.partition('!')
            __data_row = head

            if __data_row[0] == '<':
                print "found <> row, ignoring"
            elif __data_row[0] == '[':
                _attr = __data_row.split()
                del _attr[0]
                del _attr[-1]

                self._dataset.decision = _attr[len(_attr)-1]

                del _attr[-1]

                self._dataset.attributes = _attr
            else:
                _case = __data_row.split()

                for i in range(0,len(_case)):
                    if _case[i].isdigit():
                        self._dataset.symbolic = False
                        _case[i] = float(_case[i])

                self._dataset.add_to_universe(_case)



    def return_data(self):
        return self._dataset



