
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

            if head == "" or head.isspace():
                __data_row = tail
            else:    
                __data_row = head

                if __data_row[0] == '<':
                    continue
                elif __data_row[0] == '[':
                    _attributes_decision = [[],[]]

                    # Split the row and trim the brackets
                    _attr = __data_row.split()
                    del _attr[0]
                    del _attr[-1]

                    _attributes_decision[1].append(_attr[len(_attr)-1])
                    del _attr[-1]
                    _attributes_decision[0] = _attr

                    self._dataset.attributes = _attributes_decision
                else:
                    _case = __data_row.split()

                    _universe_case = [[],[]]

                    _universe_case[1].append(_case[len(_case)-1])
                    del _case[-1]
                    
                    for i in range(0,len(_case)):

                        try:
                            float(_case[i])
                            _case[i] = float(_case[i])
                            self._dataset.symbolic = False
                        except ValueError:
                            continue

                    _universe_case[0] = _case

                    self._dataset.add_to_universe(_universe_case)

    def return_data(self):
        return self._dataset



