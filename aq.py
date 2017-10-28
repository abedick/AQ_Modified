
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
            print "Current Complex: " + str(_complex)

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
                    _selector = "(" + str(self._dataset.attributes[0][j]) + ", NOT " + str(self._dataset.universe[i][0][j]) + ")"
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
            else: 

                ##
                ## Check if the new selectors are already covered in the complex
                ## updateds _covered to reflect accordingly
                ##
                # for j in _selectors:
                for k in _complex:   
                    print "\nSelectors " + str(_selectors) + "\n_complex " + str(k)
                    # print "(selectors).issubet(complex) " + str(set(_selectors).issubset(set(k)))
                    print "(selectors).issuperset(complex) " + str(set(_selectors).issuperset(set(k)))
                    # print "Len condition: " + str((len(_selectors) > len(k))) + "\n\n"

                    if set(_selectors) == set(k):
                        _covered = True
                        print "Case : " + str(i) + " is covered by equality condition."
                        break
                    elif set(_selectors).issuperset(set(k)) and len(_covered_universe) > 1:
                        _covered = True
                        print "Case : " + str(i) + " is covered by superset condition."
                        break

                    # if set(_selectors).issubset(set(k)):
                    #     _covered = True
                    #     print "Case : " + str(i) + " is covered."
                    #     break
                    # elif set(_selectors).issuperset(set(k)) and (len(_selectors) > len(k)):
                    #     _covered = True
                    #     print "Case : " + str(i) + " is covered."
                    #     break

                ##
                ## If not already covered, compute the new complexes
                ##

                if not _covered:
                    ##
                    ## Compute new complex
                    ##

                    for j in _selectors:
                        for l in _complex:
                            _new_conjunction = (l,j)
                            print "New conjunction: " + str(_new_conjunction) + "\n\n\n"
                            _new_complex.append(_new_conjunction)

                    ##
                    ## Remove subsumed complexes
                    ##

                    ##
                    ## Remove worse complexes from the partial star until size STAR <= MAXSTAR
                    ##

                    ##
                    ## Update the partial star 
                    ##
                    _complex = _new_complex


            ##
            ## Updated the covered universe 
            ##
            _covered_universe.append(i)

            test = raw_input()

        ##
        ## Return _complex as the working partial star
        ##
        return _complex

        ##
        ## END PARTIAL STAR PROCEDURE
        ##

                # _new_complex = []

                # for k in _complex:
                #     for l in _selectors:
                #         _new_complex.append(list(set((k,l))))
                    
                # print _new_complex
                # _complex = _new_complex

            # elif len(_covered_universe) == 1:
            #     _new_complex = []

            #     for k in _complex:
            #         for l in _selectors:
            #             _new_complex.append(list(set((k,l))))

            #     ##
            #     ## Calculate subsets to be removed and then remove them
            #     ##
            #     _removable = []

            #     for k in range(0,len(_new_complex)):
            #         for l in range(0,len(_new_complex)):
            #             if k != l:
            #                 _outer_set = set(_new_complex[k])
            #                 _inner_set = set(_new_complex[l])
            #                 if _outer_set.issubset(_inner_set):
            #                     _removable.append(l)
            #     _removable = _removable[::-1]

            #     for k in _removable:
            #         del _new_complex[k]
            #     print _selectors
            #     _complex = _new_complex
            # else:
                # print _selectors   
                # _complex_set = []

                # for j in _complex:
                #     _complex_set.append(set(j))

                # _selector_set = set(_selectors)

                # for j in _complex_set:
                #     if j.issubset(_selector_set) and j != _selector_set:
                #         _covered = True
                # if not _covered:
                #     _new_complex = []

                #     for j in range(0,len(_complex)):
                #         _new_selectors = []

                #         for k in _selectors:
                #             _new_selectors.append(k)
                #             for l in range(0,len(_complex[j])):
                #                 _new_selectors.append(_complex[j][l])
                #         _new_complex.append(list(set(_new_selectors)))
                        
                #     _complex = _new_complex  
            # _covered_universe.append(i)
        # _partial_star = _complex

        # return _partial_star