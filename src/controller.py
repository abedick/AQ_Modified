# @file: controlelr.py
# @author: Abraham Dick
# @date: October 2017
# @desc: Main controller for EECS 690 Programming Project


from src.dataset import Dataset
from src.lers_reader import LERS_Reader
from src.aq_modified import AQMod
from src.ruleset_printer import Printer

from itertools import izip_longest

class Controller(object):

    def __init__(self):
        self._dataset = Dataset()
        self._aq = AQMod()
        self._results = None
        self._printer = Printer()

    def run(self):
        # Grab a filename from the user
        _file = False

        while not _file:
            _filename = raw_input("Please enter a filename of a LERS file format: ")
            try:
                _file_test = open(_filename, 'r')
                _file = True
            except IOError:
                print "Invalid filename given."
                _file = False

        _ms = False
        _ms_value = None
        
        while not _ms:
            _ms_value = raw_input("Please enter an integer value for MAXSTAR: ")
            try:
                _ms_value = int(_ms_value)
                if _ms_value > 0:
                    _ms_value = int(_ms_value)
                    _ms = True
                else:
                    print "Invalid MAXSTAR value. Please enter an integer larger than 0."
            except ValueError:
                print "Invalid MAXSTAR value. Please enter an integer larger than 0."


        # Start the reader and read in the file
        _reader = LERS_Reader(_filename)
        _reader.read_file()

        # Grab the data from the file
        self._dataset = _reader.return_data()
        self._dataset.maxstar = _ms_value
        self._dataset.name = _filename

        # Check if the data is symbolic or numeric
        if not(self._dataset.symbolic):
            self.compute_numeric()

        self.calculate_blocks()
        self.check_consistency_fast()
        self.get_attribute_range()

        ## Send the dataset to AQ
        self._results = self._aq.run(self._dataset)

        ## Process the results
        _non_negated = self.results_helper(self._results)
        _negated = self.negated_results_helper(self._results)

        ## Print the results to file
        _processed_results = [_non_negated,_negated]
        self._printer.printer(_processed_results,self._dataset.name)

    ###
    ### Calculates the concept blocks {d}*
    ###
    def calculate_blocks(self):
        _case_decision = []

        for i in xrange(len(self._dataset.universe)):
            if self._dataset.universe[i][1] not in _case_decision:
                _case_decision.append(self._dataset.universe[i][1])

        _block = []
        for i in _case_decision:
            _block.append([[i[0]],[]])

        for i in xrange(len(self._dataset.universe)):
            _placed = False
            while not _placed:
                for k in xrange(len(_case_decision)):
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

        for i in xrange(len(self._dataset.universe)):
            _test_case = self._dataset.universe[i]
            _test_case_decision = _test_case[_case_decision]
            _test_case = _test_case[:-1]

            for k in xrange(len(self._dataset.universe)):
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

        for i in range(len(self._dataset.attributes[0])):
            _attribute_sets.append([])

        for i in xrange(len(self._dataset.universe)):
            for k in xrange(len(self._dataset.attributes[0])):
                _attribute_sets[k].append(self._dataset.universe[i][0][k])

        for i in xrange(len(_attribute_sets)):
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
        for i in xrange(len(self._dataset.universe[0][0])):
            try:
                float(self._dataset.universe[0][0][i])
                _number_attributes.append(i)
            except ValueError:
                continue
            
        _attribute_values = []

        # for each attribute that is numberic, append each unique case to _attribute_values[i]
        for i in xrange(len(_number_attributes)):
            _attribute_values.append([_number_attributes[i],[]])

            for k in xrange(len(self._dataset.universe)):
                if self._dataset.universe[k][0][_number_attributes[i]] not in _attribute_values[i][1]:
                    _attribute_values[i][1].append(self._dataset.universe[k][0][_number_attributes[i]])

            _attribute_values[i][1] = sorted(_attribute_values[i][1])

        _new_attributes = []

        # Create the attribute attributes that were numeric and compute their ranges and append them as block to _new_attributes
        for i in xrange(len(_attribute_values)):
            _set = _attribute_values[i][1]
            _new_attributes.append([])

            for k in xrange(1,len(_set)):
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
        for i in xrange(len(self._dataset.universe)): 
            _updated_uni.append([])
            for k in xrange(len(_new_attributes)):
                _new_attribute_block = []
                for l in xrange(len(_new_attributes[k])):
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

        for i in xrange(len(_new_attributes)):
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
        for i in xrange(len(self._dataset.universe)):
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


    def negated_results_helper(self,_results):
        _rules = []

        if(not self._dataset.consistent):
            _rules.append("! The input data set is inconsistent")

        for i in xrange(len(_results)):
            for j in xrange(len(_results[i][1])):
                _rule = ""

                for k in xrange(len(_results[i][1][j])):
                    _rule = _rule + "(" + str(_results[i][1][j][k][0]) + ", " + str(_results[i][1][j][k][1]) + ")"
                    
                    if ((len(_results[i][1][j][k]) > 1) and (k != len(_results[i][1][j])-1)):
                           _rule = _rule + " AND "

                _rule = _rule + " -> (" + str(self._dataset.attributes[1][0]) + ", " + str(_results[i][0][0]) + ")"
                _rules.append(_rule)
        return _rules
                
    
    def results_helper(self,_results):
        _new_rules = []

        ## For each concepts' rule set
        for i in xrange(len(_results)):
            _new_concept_rules = []

            ## For each rule
            for j in xrange(len(_results[i][1])):
                _current_working_rule = _results[i][1][j]
                _new_rule = []

                ## For each conjunction/selector
                for k in xrange(len(_current_working_rule)):
                    _working_attribute = _current_working_rule[k][0]
                    _working_attribute_value = _current_working_rule[k][1][4::]
                   
                    for l in xrange(len(self._dataset.attributes[0])):
                        if _working_attribute == self._dataset.attributes[0][l]:
                            _new_attribute_values = list(set(self._dataset.attribute_range[l]) - set([_working_attribute_value]))
                            _new_av_pairs = []

                            for m in xrange(len(_new_attribute_values)):
                                _new_av_pairs.append((_working_attribute,_new_attribute_values[m]))

                                if _new_av_pairs not in _new_rule:
                                    _new_rule.append(_new_av_pairs)

                    if _new_rule not in _new_concept_rules:
                        _new_concept_rules.append(_new_rule)
            
            _new_rules.append(_new_concept_rules)
        _processed_rules = []

        for i in range(len(_new_rules)):
            _concept_rules = []
            for j in range(len(_new_rules[i])):
                _working_rules = []

                for k in range(len(_new_rules[i][j])):
                    _update = []
 
                    if _working_rules == []:
                        for l in range(len(_new_rules[i][j][k])):     
                            _update.append([_new_rules[i][j][k][l]])
                    else:
                        for l in range(len(_new_rules[i][j][k])):
                            for m in range(len(_working_rules)):
                                _new = _working_rules[m]
                                _new = _new + [_new_rules[i][j][k][l]]
                                _new = list(set(_new))
                                if _new not in _update:
                                    _update.append(_new)

                    _working_rules = _update
                _concept_rules.append(_working_rules)
            _processed_rules.append(_concept_rules)

        for concept in _processed_rules:
            for rule in concept:
                if len(rule) > 1:

                    ## Simplify new expanded rules
                    for i in range(len(rule)):
                        rule[i] = list(set(rule[i]))

                    _to_remove = []

                    ## Remove rules that are supersets of other rules
                    for i in range(len(rule)):
                        for j in range(len(rule)):
                            if j != i:
                                if set(rule[i]).issubset(set(rule[j])):
                                    _to_remove.append(j)
                    _to_remove = list(set(_to_remove))
                    _to_remove.sort()
                    _to_remove = _to_remove[::-1]
                    for i in _to_remove:
                        del rule[i]

                    _to_remove = []

                    ## Remove rules that have two or more values for the same attribute
                    for j in range(len(rule)):
                        _attributes_repsrented = []

                        for i in range(len(rule[j])):
                            _attributes_repsrented.append(rule[j][i][0])

                        if len(set(_attributes_repsrented)) == 1 and len(rule[j]) > 1:
                            _to_remove.append(j)
                    _to_remove = list(set(_to_remove))
                    _to_remove.sort()
                    _to_remove = _to_remove[::-1]
                    for i in _to_remove:
                        del rule[i]

        _rule_set = []

        for concept in _processed_rules:
            _completed_concept_rules = []
            for rule in concept:
                if len(rule) > 1:
                    for subrule in rule:
                        _completed_concept_rules.append(subrule)
                else:
                    if type(rule[0]) == list:
                        _completed_concept_rules.append(rule[0])
                    else:
                        _completed_concept_rules.append(rule)

            _rule_set.append(_completed_concept_rules)

        for i in xrange(len(_rule_set)):
            _to_remove = []

            for j in xrange(len(_rule_set[i])):
                for k in xrange(len(_rule_set[i])):
                    if j != k:
                        if set(_rule_set[i][j]).issubset(set(_rule_set[i][k])):
                            _to_remove.append(k)

            _to_remove = list(set(_to_remove))
            _to_remove.sort()
            _to_remove = _to_remove[::-1]

            for j in _to_remove:
                del _rule_set[i][j]

        _non_negated_rules = []

        if(not self._dataset.consistent):
            _non_negated_rules.append("! The input data set is inconsistent")

        for i in xrange(len(_rule_set)):
            for j in xrange(len(_rule_set[i])):
                _rule = ""

                for k in xrange(len(_rule_set[i][j])):
                    _rule = _rule + "(" + str(_rule_set[i][j][k][0]) + ", " + str(_rule_set[i][j][k][1]) + ")"

                    if len(_rule_set[i][j][k]) > 1 and k != len(_rule_set[i][j])-1:
                        _rule = _rule + " AND "
                _rule = _rule + " -> (" + str(self._dataset.attributes[1][0]) + ", " + str(self._dataset.d_star[i][0][0]) + ")"
                _non_negated_rules.append(_rule)
 
        return _non_negated_rules