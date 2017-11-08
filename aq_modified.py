

# @file: aq.py
# @author: Abraham Dick
# @date: October 2017
# @desc: Implements the AQ15 algorithm with modifications as specified in the EECS
#         690 semester project requirements


from dataset import Dataset

class AQMod:

    def __init__(self):
        self._dataset = None

    ##
    ## In charge of controlling AQ
    ##
    def run(self,dataset):
        self._dataset = dataset
        return self.start()

    ##
    ## calculates the concepts and runs the AQ 
    ##
    def start(self):
        _result = []

        # for i in xrange(len(self._dataset.d_star)):
        for i in xrange(1):
            _positive = list(set(self._dataset.d_star[i][1]))
            _negative = list(set(range(len(self._dataset.universe))).difference(set(self._dataset.d_star[i][1])))

            # print "C: " + str(_positive)
            # print "F: " + str(_negative)

            _result.append([self._dataset.d_star[i][0],self.aq(_positive,_negative)])

        return _result

    def aq(self, positive, negative):

        _star = []

        for seed in positive:
            print "Seed: " + str(seed)
            ## Check to see if seed is already covered

            ## If not covered, compute partial star
            _partial_star = self.partial_star(seed,negative)

            _star.append(_partial_star)


        for i in _star:
            print i

        return _star

    def partial_star(self,seed,negative):
        _partial_star = []
        _covered_universe = []
        _seed_value = self._dataset.universe[seed]
        _attributes = self._dataset.attributes

        for case in negative:
            # print "G ( " + str(seed) + " | " + str(case) + " )"
            # print "Partial Star: "+ str(_partial_star)
            _new_partial = []

            ##
            ## Gather new selectors by comparing seed case against negative case
            ##
            _selectors = []
            for i in xrange(len(_attributes[0])):
                _universe_attribute = self._dataset.universe[case][0][i]
                _seed_attribute = self._dataset.universe[seed][0][i]

                if _universe_attribute != _seed_attribute:
                    _selector = (str(self._dataset.attributes[0][i]),"NOT " + str(self._dataset.universe[case][0][i]))
                    _selectors.append(_selector)

            ##
            ## If these are the first selectors, they will each be the beginning of 
            ## a conjunction
            ##
            if len(_covered_universe) == 0:
                # print "Original Selectors: " + str(_selectors)
                for selector in _selectors:
                    _new_partial.append([selector])
                _partial_star = _new_partial

            else:
                ##
                ## First conjunction
                ##
                if len(_covered_universe) == 1:
                    for i in _partial_star:
                        for j in _selectors:
                            _conjunction = (i[0],j)
                            _new_partial.append(list(set(_conjunction)))
                    _partial_star = _new_partial
                else:
                    ##
                    ## Make sure that case isn't already covered
                    ##
                    _covered = False
                    for conjunction in _partial_star:
                        if set(_selectors).issuperset(set(conjunction)):
                            _covered = True
                            break
                    
                    if not _covered:
                        # print "New Selectors: " + str(_selectors)
                        for i in _partial_star:
                            for j in _selectors:

                                _new_conjunction = []
                                for complex in i:
                                    _new_conjunction.append(complex)
                                _new_conjunction.append(j)

                                # print _new_conjunction
                                _new_partial.append(list(set(_new_conjunction)))
                        _partial_star = _new_partial

                ##
                ## Remove complexes that are already covered
                ##
                _removable = []
                for i in xrange(len(_new_partial)):
                    for j in xrange(len(_new_partial)):
                        if i != j and set(_new_partial[i]).issubset(set(_new_partial[j])):
                            if j not in _removable:
                                _removable.append(j)

                _removable.sort()
                _removable = _removable[::-1]
            
                for j in _removable:
                    if len(_new_partial) > 1:
                        del _new_partial[j]

                ##
                ## Remove complexes until number complex = MAXSTAR
                ##
                while len(_new_partial) > self._dataset.maxstar:
                    _modified_partial = []

                    for i in _new_partial:
                        _mod = []
                        for j in i:
                            _mod.append((j[0], j[1][4::]))
                        _modified_partial.append(_mod)
                    _pos = list(set(range(len(self._dataset.universe))) - set(negative))

                    _test_universe = []
                    for j in _pos:
                        _comparison = []
                        for l in range(0,len(self._dataset.universe[j][0])):
                            _case_update = (self._dataset.attributes[0][l],self._dataset.universe[j][0][l])
                            _comparison.append(_case_update)
                        _test_universe.append(_comparison)
                    
                    _cover_list = []
                    
                    for j in _modified_partial:
                        _list = []
                        for k in xrange(len(_test_universe)):
                            _flag = True
                            for l in j:
                                for m in xrange(len(_test_universe[k])):
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
                    del _new_partial[_index_remove]
            _covered_universe.append(case)
                
        return _partial_star
