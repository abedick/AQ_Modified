
# @file: aq.py
# @author: Abraham Dick
# @date: October 2017
# @desc: Implements the AQ15 algorithm with modifications as specified in the EECS
#         690 semester project requirements


from dataset import Dataset


class AQ:

    def __init__(self):
        self._dataset = None
        self._maxstar = None
        self._completed_concepts = []

        self._pos = None
        self._neg = None

    def run(self, dataset):
        self._dataset = dataset
        self._maxstar = dataset.maxstar

        _result = []

        for i in range(0,len(self._dataset.d_star)):

            _pos = set(self._dataset.d_star[i][1])
            _neg = set(range(0,len(self._dataset.universe)))

            _neg = list(_neg.difference(_pos))
            _pos = list(_pos)

            self._neg = _neg
            self._pos = _pos

            # print "C = " + str(_pos)
            # print "F = " + str(_neg)

            _result.append([[self._dataset.d_star[i][0]],self.AQ_star(_pos,_neg)])

        return _result

    def AQ_star(self,pos,neg):
        
        _cover = []

        ## For each case, send the seed only if the seed is not already covered by the 
        ## exsiting partial star
        for b in pos:
            # print "Seed: " + str(b)

            ## Calculate the new partial
            _partial = self.partial_star(b,neg)

            ## Check if the new partial is already covered by the cover
            _covered = False

            for i in xrange(len(_partial)):
                for k in xrange(len(_cover)):
                    if _cover[k] == _partial[i]:
                        _covered = True
                        break

            if not _covered:
                ## Add the new partial to the cover
                _cover += _partial

        return _cover

    def partial_star(self,seed,neg):
        _covered_universe = []

        _partial_star = []
        _complex = []

        seed_value = self._dataset.universe[seed]
        _attributes = self._dataset.attributes

        for i in neg:
            # print "G ( " + str(seed) + " | " + str(i) + " )"
            # print "Current Complex: " + str(_complex)

            _new_complex = []


            ## Updated to true if new selectors are deemed to have already been covered by the
            ## current working complex
            _covered = False
            
            ## Grab the new availiable selectors
            ## - If the universe attribute is different than the seed attribute, form a tuple
            ## - This tuple uses negate and concatenates "NOT" to the second position of the tuple
            _selectors = []

            for j in  xrange(len(_attributes[0])):
                _universe_attribute = self._dataset.universe[i][0][j]
                _seed_attribute = self._dataset.universe[seed][0][j]

                if _universe_attribute != _seed_attribute:
                    _selector = (str(self._dataset.attributes[0][j]),"NOT " + str(self._dataset.universe[i][0][j]))
                    _selectors.append(_selector)


            ## If testing against the first negative case, each selector should be stored as if it will 
            ## be an individual rule if the length of all false cases is one
            if len(_covered_universe) == 0 :
                for j in _selectors:
                    _new_complex.append([j])
                _complex = _new_complex

            ## - If the current neg comparison case is covered by an already existing complex, mark it as covered
            ##   and continue to the next case 
            ## - If testing against the other rules, recompute the complex with the addition of each new selector
            ##   for each additional negative case in neg. Then remove the complexes covered by other cases.

            ## if the list of negative cases is at least one, this will be the first time tuples are built of the
            ## conjoined selectors from the first iteration
            elif len(_covered_universe) == 1:
                for j in _complex:
                    for k in _selectors:
                        _conjunction = (j[0],k)
                        _new_complex.append(list(set(_conjunction)))

                ## Remove complexes already covered and remove worst complexes until _new_complex <= MAXSTAR
                ## Then updated the partial star, labeled as _complex
                _new_complex = self.covered_helper(_new_complex)
                _new_complex = self.maxstar_helper(_new_complex)
                _complex = _new_complex

            ## The negative universe is at least 3 cases long
            ## The tuples of conjunctions have already been built
            else: 
                ## Check if the new selectors are already covered in the complex
                ## updateds _covered to reflect accordingly
                for k in _complex:   
                    if set(_selectors) == set(k):
                        continue
                    elif set(_selectors).issuperset(set(k)) and len(_covered_universe) > 1:
                        _covered = True
                        break

                ## If not already covered, compute the new complexes
                if not _covered:
                    ## Compute new complex
                    for j in _selectors:
                        for k in _complex:
                            if j != k:
                                _new_conjunction = []

                                for each in k:
                                    _new_conjunction.append(each)

                                _new_conjunction += (j, )
                                _new_complex.append(list(set(_new_conjunction)))

                    ## Remove complexes already covered and remove worst complexes until _new_complex <= MAXSTAR.
                    ## Then updated the partial star, labeled as _complex
                    _new_complex = self.covered_helper(_new_complex)
                    _new_complex = self.maxstar_helper(_new_complex)
                    _complex = _new_complex

            ## Updated the covered universe 
            _covered_universe.append(i)

        ## Return _complex as the working partial star
        return _complex

    def covered_helper(self, new_complex):
        _removable = []

        for j in xrange(len(new_complex)):
            for k in xrange(len(new_complex)):
                if j != k:
                    if set(new_complex[j]).issubset(set(new_complex[k])):
                        _removable.append(k)

        _removable = list(set(_removable))
        _removable.sort()
        _removable = _removable[::-1]

        for j in _removable:
            if len(new_complex) > 1:
                del new_complex[j]

        return new_complex
        
    def maxstar_helper(self, new_complex):
        while len(new_complex) > self._maxstar:
            _new_complex_mod = []

            for j in new_complex:
                _mod = []
                for k in j:
                    _new = (k[0], k[1][4::])
                    _mod.append(_new)
                _new_complex_mod.append(_mod)
            _pos = list(set(range(0,len(self._dataset.universe))) - set(self._neg))
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

            for j in xrange(len(_cover_list)):
                _cover_list[j] = len(_cover_list[j])
            _index_remove = -1
            _count = 0

            for j in xrange(len(_cover_list)):
                if _cover_list[j] > _count:
                    _count = _cover_list[j]
                    _index_remove = j
            del new_complex[_index_remove]
        
        return new_complex