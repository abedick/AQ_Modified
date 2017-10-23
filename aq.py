
# @file: aq.py
# @author: Abraham Dick
# @date: October 2017
# @desc: Implements the AQ15 algorithm with modifications as specified in the EECS
#         690 semester project requirements


from dataset import Dataset


class AQ:

    def __init__(self):
        self._dataset = None

        self._completed_concepts = []



    def run(self, dataset):
        self._dataset = dataset

        _result = []

        for i in range(0,len(self._dataset.d_star)):

            _pos = set(self._dataset.d_star[i][1])
            _neg = set(range(0,len(self._dataset.universe)))

            _neg = list(_neg.difference(_pos))
            _pos = list(_pos)

            print "C = " + str(_pos)
            print "F = " + str(_neg)

            _result.append([[self._dataset.d_star[i][0]],self.AQ_star(_pos,_neg)])

        return _result

    def AQ_star(self,pos,neg):
        
        _cover = []

        _uncovered = neg

        # # for b in pos:
        # for i in neg:

            # print "Seed: " + str(b)
        _partial = self.partial_star(pos[0],neg)

            # # Computing the set of covers
            # if _cover != []:

            #     for j in range(0,len(_cover)):
            #         for k in range(0,len(_cover[j])):
            #             for l in range(0,len(_partial)):

            #                 print "Cover: " + str(_cover[j][k])
            #                 print "Partial: " + str(_partial[l])

        _cover.append(_partial)

        return _partial

    def partial_star(self,seed,neg):

        

        _seed_value = self._dataset.universe[seed]
        _attributes = self._dataset.attributes

        _covered_universe = []
        _negative_universe = []

        for i in neg:
            _negative_universe.append(self._dataset.universe[i][:-1])

        _partial_star = []

        _ext = []

        # Test each negative case against the seed
        for i in neg:

            _covered = False

            print "Checking against Negative Case : " + str(i)
            _local_rule = []

            # Check across all the attributes in the negative universe
            for j in range(0,len(_attributes)):
                if self._dataset.universe[seed][j] != self._dataset.universe[i][j]:
                    _selector = "(" + str(self._dataset.attributes[j]) + ", NOT " + str(self._dataset.universe[i][j]) + ")"
                    _local_rule.append(_selector)

            if _covered_universe != []:
                _conjunction_rule = []

                for j in _ext:
                    print "\nchecking here : " + str(j) + " versus " + str(_local_rule)  + " Value of _covered = " + str(_covered)
                    print "if true, match found : " + str(j == _local_rule)
                    if j == _local_rule:
                        print "matched"
                        _covered = True

                if not _covered:
                    for n in _ext:
                        _new_rule = []
                        for m in _local_rule:
                            print "New value : " +str(n) + ", " + str(m) 
                            _new_rule.append(n)
                            _new_rule.append(m)

                        _conjunction_rule.append(_new_rule)

                    _ext = _conjunction_rule

                print "\n\n\n"
                print "_ext : " + str(_ext)
                print "_local_rule : " + str(_local_rule)
                print "\n\n\n"

            else:
                _ext.append(_local_rule)

            _test = raw_input("")

            _covered_universe.append(i)
            print "Covered: " + str(_covered_universe)

        # _partial_star.append(_ext)

        return _ext































































        #     _complex = []
        
        # _covered_universe = []
 

        # # For each the negative cases
        # for i in neg:

        #     _selectors = []

        #     _already_covered = False

        #     # Check the range of attributes
        #     for j in xrange(0,len(self._dataset.attributes)):

                

        #         # If the attribute value of the seed does not match the negative case, record the attribute value of the negative case
        #         if self._dataset.universe[seed][j] != self._dataset.universe[i][j]:
        #             _selector = "(" + str(self._dataset.attributes[j]) + ", NOT " + str(self._dataset.universe[i][j]) + ")"

        #             #add the negative case to the list of selectors
        #             _selectors.append(_selector)


        #     # Update the complex
        #     _new_complex = []
        #     _covered_universe.append(i)
        #     print _covered_universe

        #     if _complex != []:

        #         # print _selectors[0]

        #         # for j in range(0,len(_complex)):
        #             # for k in range(0,len(_selectors)):

        #         print _complex

        #         _complex_set = set(_complex)
        #         _selector_set = set(_selectors)
                

        #         print "complex_set : " + str(list(_complex_set))
        #         print "selector_set : " + str(list(_selector_set))

        #         if _selector_set.issubset(_complex_set):
        #             print "subset branch taken"

        #             print str(_selector_set) + " is subset of " + str(_complex_set)




        #             _new_complex = _complex

        #             # print "anti-flag selectors = " + str(list(_selector_set))
        #         else:
        #             print "nxm branch taken"
        #             for n in _complex_set:
        #                 for m in _selector_set:
        #                     _new_complex.append([n] + [m])


        #                 # print _new_complex

        #         # for j in range(0,len(_complex)):
        #         #     for k in range(0,len(_selectors)):

        #         #         _complex_set = set(_complex[j])
        #         #         _selector_set = set([_selectors[k]])
                        

        #         #         # print "complex_set : " + str(list(_complex_set))
        #         #         # print "selector_set : " + str(list(_selector_set))

        #         #         if _selector_set.issubset(_complex_set):
        #         #             print "subset branch taken"

        #         #             print str(_selector_set) + " is subset of " + str(_complex_set)




        #         #             _new_complex = _complex

        #         #             # print "anti-flag selectors = " + str(list(_selector_set))
        #         #         else:
        #         #             print "nxm branch taken"
        #         #             for n in _complex_set:
        #         #                 for m in _selector_set:
        #         #                     _new_complex.append([n] + [m])


        #         #         # print _new_complex

        #         _complex = _new_complex
        #         print _complex

        #         _test = raw_input("")

        #     # Add the result to the complex
                
            
        #     else :
        #         _complex.append(_selectors)

        #     # check the new complex against all the previous




        # _star.append(_complex)


        # # remove all complexes that are subsumed by other complexes in star


        # # Remove worst complexes (fewest number of covers)
        # #  STAR <= user-defined Maximum Star (maxstar)