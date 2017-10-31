
# @file: aq.py
# @author: Abraham Dick
# @date: October 2017
# @desc: Implements the AQ15 algorithm with modifications as specified in the EECS
#         690 semester project requirements


from dataset import Dataset


class AQ:

    def __init__(self):
        self._dataset = None
        self._maxstar = 1
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



        # _pos = set(self._dataset.d_star[0][1])
        # _neg = set(range(0,len(self._dataset.universe)))

        # _neg = list(_neg.difference(_pos))
        # _pos = list(_pos)

        # print "C = " + str(_pos)
        # print "F = " + str(_neg)

        # _result.append([[self._dataset.d_star[0][0]],self.AQ_star(_pos,_neg)])

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
        _complex = []

        seed_value = self._dataset.universe[seed]
        _attributes = self._dataset.attributes

        for i in neg:
            print "G ( " + str(seed) + " | " + str(i) + " )"
            # print "Current Complex: " + str(_complex)

            _new_complex = []

            ##
            ## Updated to true if new selectors are deemed to have already been covered by the
            ## current working complex
            ##
            _covered = False
            
            ##
            ## Grab the new availiable selectors
            ## - If the universe attribute is different than the seed attribute, form a tuple
            ## - This tuple uses negate and concatenates "NOT" to the second position of the tuple
            ##
            _selectors = []

            for j in range(0,len(_attributes[0])):
                _universe_attribute = self._dataset.universe[i][0][j]
                _seed_attribute = self._dataset.universe[seed][0][j]

                if _universe_attribute != _seed_attribute:
                    _selector = (str(self._dataset.attributes[0][j]),"NOT " + str(self._dataset.universe[i][0][j]))
                    _selectors.append(_selector)

            ##
            ## If testing against the first negative case, each selector should be stored as if it will 
            ## be an individual rule if the length of all false cases is one
            ##
            if len(_covered_universe) == 0 :
                for j in _selectors:
                    _new_complex.append([j])
                _complex = _new_complex

            ##
            ## - If the current neg comparison case is covered by an already existing complex, mark it as covered
            ##   and continue to the next case 
            ## - If testing against the other rules, recompute the complex with the addition of each new selector
            ##   for each additional negative case in neg. Then remove the complexes covered by other cases.
            ##

            ##
            ## if the list of negative cases is at least one, this will be the first time tuples are built of the
            ## conjoined selectors from the first iteration
            ##

            
            elif len(_covered_universe) == 1:
                for j in _complex:
                    for k in _selectors:
                        _conjunction = (j[0],k)
                        _new_complex.append(list(set(_conjunction)))

                ##
                ## Remove subsumed complexes
                ##
                _removable = []

                for j in range(0,len(_new_complex)):
                    for k in range(0,len(_new_complex)):
                        print str(j) + " " + str(k)
                        if j != k and set(_new_complex[j]).issubset(set(_new_complex[k])):
                            _removable.append(k)

                _removable = list(set(_removable))
                _removable.sort()
                _removable = _removable[::-1]

                for j in _removable:
                    if len(_new_complex) > 1:
                        del _new_complex[j]
                
                ##
                ## Remove worse complexes from the partial star until size STAR <= MAXSTAR
                ##
                while len(_new_complex) > self._maxstar:
                    _new_complex_mod = []

                    for j in _new_complex:
                        _mod = []
                        for k in j:
                            _new = (k[0], k[1][4::])
                            _mod.append(_new)
                        _new_complex_mod.append(_mod)
                    _pos = list(set(range(0,len(self._dataset.universe))) - set(neg))
                    _test_universe = []
                
                    for j in _pos:
                        _comparison = []

                        for l in range(0,len(self._dataset.universe[j][0])):
                            _case_update = (self._dataset.attributes[0][l],self._dataset.universe[j][0][l])
                            _comparison.append(_case_update)
                        _test_universe.append(_comparison)
                    _cover_list = []
                    
                    for j in _new_complex_mod:
                        _list = []
                        for k in range(0,len(_test_universe)):
                            _flag = True
                            for l in j:
                                for m in range(0,len(_test_universe[k])):
                                    if l == _test_universe[k][m]:
                                        _flag = False
                            if _flag:
                                _list.append(k)
                        _cover_list.append(_list)

                    for j in range(0,len(_cover_list)):
                        _cover_list[j] = len(_cover_list[j])
                    _index_remove = -1
                    _count = 0

                    for j in range(0,len(_cover_list)):
                        if _cover_list[j] > _count:
                            _count = _cover_list[j]
                            _index_remove = j
                    del _new_complex[_index_remove]

                _complex = _new_complex

            ##
            ## The negative universe is at least 3 cases long
            ## The tuples of conjunctions have already been built
            ##
            else: 

                ##
                ## Check if the new selectors are already covered in the complex
                ## updateds _covered to reflect accordingly
                ##
                for k in _complex:   
                    if set(_selectors) == set(k):
                        _covered = True
                        print "Case : " + str(i) + " is covered by equality condition."
                        break
                    elif set(_selectors).issuperset(set(k)) and len(_covered_universe) > 1:
                        _covered = True
                        print "Case : " + str(i) + " is covered by superset condition."
                        break

                ##
                ## If not already covered, compute the new complexes
                ##
                if not _covered:
                    ##
                    ## Compute new complex
                    ##

                    for j in _selectors:
                        for k in _complex:
                            if j != k:
                                _new_conjunction = []

                                for each in k:
                                    _new_conjunction.append(each)

                                _new_conjunction += (j, )
                                _new_complex.append(list(set(_new_conjunction)))

                    # ##
                    # ## Remove subsumed complexes
                    # ##
                    _removable = []

                    for j in range(0,len(_new_complex)):
                        for k in range(0,len(_new_complex)):
                            if j != k and set(_new_complex[j]).issubset(set(_new_complex[k])):
                                _removable.append(k)

                    _removable = list(set(_removable))
                    _removable.sort()
                    _removable = _removable[::-1]

                    for j in _removable:
                        if len(_new_complex) > 1:
                            del _new_complex[j]

                    ##
                    ## Remove worse complexes from the partial star until size STAR <= MAXSTAR
                    ##
                    while len(_new_complex) > self._maxstar:
                        _new_complex_mod = []

                        for j in _new_complex:
                            _mod = []
                            for k in j:
                                _new = (k[0], k[1][4::])
                                _mod.append(_new)
                            _new_complex_mod.append(_mod)
                        _pos = list(set(range(0,len(self._dataset.universe))) - set(neg))
                        _test_universe = []
                    
                        for j in _pos:
                            _comparison = []

                            for l in range(0,len(self._dataset.universe[j][0])):
                                _case_update = (self._dataset.attributes[0][l],self._dataset.universe[j][0][l])
                                _comparison.append(_case_update)
                            _test_universe.append(_comparison)
                        _cover_list = []
                        
                        for j in _new_complex_mod:
                            _list = []
                            for k in range(0,len(_test_universe)):
                                _flag = True
                                for l in j:
                                    for m in range(0,len(_test_universe[k])):
                                        if l == _test_universe[k][m]:
                                            _flag = False
                                if _flag:
                                    _list.append(k)
                            _cover_list.append(_list)

                        for j in range(0,len(_cover_list)):
                            _cover_list[j] = len(_cover_list[j])
                        _index_remove = -1
                        _count = 0

                        for j in range(0,len(_cover_list)):
                            if _cover_list[j] > _count:
                                _count = _cover_list[j]
                                _index_remove = j
                        del _new_complex[_index_remove]

                    ##
                    ## Update the partial star 
                    ##
                    _complex = _new_complex


            ##
            ## Updated the covered universe 
            ##
            _covered_universe.append(i)

            ##
            ## DEBUG ONLY
            ##
            # test = raw_input()

        ##
        ## Return _complex as the working partial star
        ##
        # print "Partial star: " + str(_complex) + "\n\n\n"
        return _complex

        ##
        ## END PARTIAL STAR PROCEDURE
        ##