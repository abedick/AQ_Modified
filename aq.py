
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

        # for i in range(0,len(self._dataset.d_star)):

        #     _pos = set(self._dataset.d_star[i][1])
        #     _neg = set(range(0,len(self._dataset.universe)))

        #     _neg = list(_neg.difference(_pos))
        #     _pos = list(_pos)

        #     print "C = " + str(_pos)
        #     print "F = " + str(_neg)

        #     _result.append([[self._dataset.d_star[i][0]],self.AQ_star(_pos,_neg)])



        _pos = set(self._dataset.d_star[0][1])
        _neg = set(range(0,len(self._dataset.universe)))

        _neg = list(_neg.difference(_pos))
        _pos = list(_pos)

        print "C = " + str(_pos)
        print "F = " + str(_neg)

        _result.append([[self._dataset.d_star[0][0]],self.AQ_star(_pos,_neg)])

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
        _covered_universe = []

        _partial_star = []
        _complex = None


        seed_value = self._dataset.universe[seed]
        _attributes = self._dataset.attributes

        

        for i in neg:
            print "G ( " + str(seed) + " | " + str(i) + " )"

            _covered = False

            ##
            ## Grab the new availiable selectors
            ##
            _selectors = []

            for j in range(0,len(_attributes[0])):
                _universe_attribute = self._dataset.universe[i][0][j]
                _seed_attribute = self._dataset.universe[seed][0][j]

                # If the universe attribute is different than the seed attribute, form a tuple
                # This tuple uses negate and concatenates "NOT" to the second position of the tuple
                if _universe_attribute != _seed_attribute:
                    _selector = (str(self._dataset.attributes[0][j]),"NOT " + str(self._dataset.universe[i][0][j]))
                    _selectors.append(_selector)


            # ##
            # ## If this is the first run, we will store the new selectors in _initial_selectors
            # ##

            # if _complex == None:
            #     _complex = _selectors
            
            # ##
            # ## Otherwise, build the complexes and then add them to the partial star
            # ##

            # else:

            if len(_covered_universe) == 0 :
                _complex = _selectors

            elif len(_covered_universe) == 1:
                _new_complex = []

                for j in _complex:
                    for k in _selectors:
                        _new_complex.append([j,k])

                _complex = _new_complex

            else:
                
                _complex_set = []

                for j in _complex:
                    _complex_set.append(set(j))

                _selector_set = set(_selectors)

                for j in _complex_set:
                    if j.issubset(_selector_set):
                        print "Case Covered: " + str(i)
                        _covered = True

                if not _covered:
                    print str(i)

                    print _complex
                    print _selectors



            
            _covered_universe.append(i)


        return _partial_star






#################################################################################################
        # ERROR OF MY WAYS
        
        # _seed_value = self._dataset.universe[seed]
        # _attributes = self._dataset.attributes

        # _covered_universe = []
        # _partial_star = []
        # _ext = []

        # # Test each negative case against the seed
        # for i in neg:
        #     print "G ( " + str(seed) + " | " + str(i) + " )"

        #     ## Flagged as true when selector is determined to be covered by current complex
        #     _covered = False


        #     _local_rule = []

        #     # Check across all the attributes in the negative universe
        #     for j in range(0,len(_attributes[0])):
        #         _universe_attribute = self._dataset.universe[i][0][j]
        #         _seed_attribute = self._dataset.universe[seed][0][j]

        #         # If the universe attribute is different than the seed attribute, form a tuple
        #         # This tuple uses negate and concatenates "NOT" to the second position of the tuple
        #         if _universe_attribute != _seed_attribute:
        #             _selector = (str(self._dataset.attributes[0][j]),"NOT " + str(self._dataset.universe[i][0][j]))
        #             _local_rule.append(_selector)

        #     print "Selectors : " + str(_local_rule)

        #     # If covered at least one case
        #     # Go through and construct new rules from all existing rules and the local rule that is computed above
        #     if _covered_universe != []:

        #         _conjunction_rule = []
        #         _new_rules = []

        #         _complex_set = []
        #         _local_set = set(_local_rule)

        #         for j in range(0,len(_ext)):
        #             _complex_set.append(set(_ext[j]))
        #             # print "_ext @ " + str(j) + " " + str(_complex_set[j])

        #         for j in range(0,len(_complex_set)):
        #             if not _covered:
        #                 if _complex_set[j].issubset(_local_set):
        #                     # print "found subset, case should be covered"
        #                     _covered = True
        #                 else:                        
        #                     _new_rules = []

        #                     for k in _complex_set[j]:
        #                         for l in _local_set:
        #                             _new_rules.append(set((k,l)))
        #                             # print "new rule: " + str(list(set((k,l))))
                            
        #                     print str(_new_rules)

        #                     _single_rules_index = []
        #                     _del_index = []

        #                     for k in range(0,len(_new_rules)):
        #                         if len(_new_rules[k]) == 1:
        #                             _single_rules_index.append(k)
                            
        #                     for k in _single_rules_index:
        #                         for l in range(0,len(_new_rules)):
        #                             print _new_rules[l]

        #                             if _new_rules[k].issubset(_new_rules[l]) and _new_rules[k] != _new_rules[l]:
        #                                 _del_index.append(l)

        #                     for k in _del_index:
        #                         _new_rules = _new_rules[:k]


        #         if not _covered:
        #             for k in range(0,len(_new_rules)):
        #                 _new_rules[k] = list(_new_rules[k])
        #             _ext = _new_rules

        #         # print "_local_set " + str(_local_set)

        #         print "\n\n\n"
        #         print "_ext : " + str(_ext)
        #         print "_local_rule : " + str(_local_rule)
        #         print "\n\n\n"

        #     else:
        #         _ext.append(_local_rule)

        #     # _test = raw_input("")

        #     _covered_universe.append(i)
        #     print "Covered: " + str(_covered_universe)

        # return _ext






































# Another failure
##########################################################################################################
       

        # _seed_value = self._dataset.universe[seed]
        # _attributes = self._dataset.attributes

        # _covered_universe = []
        # _negative_universe = []

        # for i in neg:
        #     _negative_universe.append(self._dataset.universe[i][:-1])

        # _partial_star = []

        # _ext = []

        # # Test each negative case against the seed
        # for i in neg:

        #     _covered = False

        #     print "Checking against Negative Case : " + str(i)

        #     _local_rule = []

        #     # Check across all the attributes in the negative universe
        #     for j in range(0,len(_attributes[0])):
        #         _universe_attribute = self._dataset.universe[i][0][j]
        #         _seed_attribute = self._dataset.universe[seed][0][j]

        #         # If the universe attribute is different than the seed attribute, form a tuple
        #         # This tuple uses negate and concatenates "NOT" to the second position of the tuple
        #         if _universe_attribute != _seed_attribute:
        #             # _selector = "(" + str(self._dataset.attributes[0][j]) + ", NOT " + str(self._dataset.universe[i][0][j]) + ")"
        #             _selector = (str(self._dataset.attributes[0][j]),"NOT " + str(self._dataset.universe[i][0][j]))
        #             _local_rule.append(_selector)

        #     print _local_rule

        #     # If covered at least one case
        #     # Go through and construct new rules from all existing rules and the local rule that is computed above
        #     if _covered_universe != []:

        #         _conjunction_rule = []
        #         _new_rules = []

        #         _complex_set = []
        #         _local_set = set(_local_rule)

        #         for j in range(0,len(_ext)):
        #             _complex_set.append(set(_ext[j]))
        #             print "_ext @ " + str(j) + " " + str(_complex_set[j])

        #         for j in range(0,len(_complex_set)):
        #             if not _covered:
        #                 if _complex_set[j].issubset(_local_set):
        #                     print "found subset, case should be covered"
        #                     _covered = True
        #                 else:                        
        #                     _new_rules = []

        #                     for k in _complex_set[j]:
        #                         for l in _local_set:
        #                             _new_rules.append(set((k,l)))
        #                             # print "new rule: " + str(list(set((k,l))))
                            
        #                     print _new_rules

        #                     _single_rules_index = []
        #                     _del_index = []

        #                     for k in range(0,len(_new_rules)):
        #                         if len(_new_rules[k]) == 1:
        #                             _single_rules_index.append(k)
                            
        #                     for k in _single_rules_index:
        #                         for l in range(0,len(_new_rules)):
        #                             print _new_rules[l]

        #                             if _new_rules[k].issubset(_new_rules[l]) and _new_rules[k] != _new_rules[l]:
        #                                 _del_index.append(l)

        #                     for k in _del_index:
        #                         _new_rules = _new_rules[:k]


        #         if not _covered:
        #             for k in range(0,len(_new_rules)):
        #                 _new_rules[k] = list(_new_rules[k])
        #             _ext = _new_rules

        #         print "_local_set " + str(_local_set)

        #         print "\n\n\n"
        #         print "_ext : " + str(_ext)
        #         print "_local_rule : " + str(_local_rule)
        #         print "\n\n\n"

        #     else:
        #         _ext.append(_local_rule)

        #     # _test = raw_input("")

        #     _covered_universe.append(i)
        #     print "Covered: " + str(_covered_universe)

#############################################################################################################################






















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