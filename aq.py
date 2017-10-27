
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
        _complex = None


        seed_value = self._dataset.universe[seed]
        _attributes = self._dataset.attributes

        

        for i in neg:
            # print "G ( " + str(seed) + " | " + str(i) + " )"

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

            if len(_covered_universe) == 0 :
                _complex = _selectors

            elif len(_covered_universe) == 1:
                _new_complex = []

                for k in _complex:
                    for l in _selectors:
                        _new_complex.append(list(set((k,l))))


                _complex = _new_complex
                # print _new_complex

            else:   
                _complex_set = []

                for j in _complex:
                    _complex_set.append(set(j))

                _selector_set = set(_selectors)

                # print _complex_set

                for j in _complex_set:
                    if j.issubset(_selector_set):
                        _covered = True

                if not _covered:
                    _new_complex = []

                    for j in range(0,len(_complex)):
                        _new_selectors = []

                        for k in _selectors:
                            _new_selectors.append(k)
                            for l in range(0,len(_complex[j])):
                                _new_selectors.append(_complex[j][l])
                        _new_complex.append(list(set(_new_selectors)))
                        
                    _complex = _new_complex 
                       
            _covered_universe.append(i)
        
        _partial_star = _complex


        return _partial_star