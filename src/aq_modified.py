

# @file: aq.py
# @author: Abraham Dick
# @date: October 2017
# @desc: Implements the AQ15 algorithm with modifications as specified in the EECS
#         690 semester project requirements


from src.dataset import Dataset

class AQMod:

    def __init__(self):
        self._dataset = None
        self._covered = []

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

        first_con = [0]

        # len(self._dataset.d_star)

        # for i in xrange(len(self._dataset.d_star)):
        for i in xrange(len(first_con)):
            _positive = list(set(self._dataset.d_star[i][1]))
            _negative = list(set(range(len(self._dataset.universe))).difference(set(self._dataset.d_star[i][1])))

            print "C = " + str(_positive)
            print "F = " + str(_negative)

            _result.append([self._dataset.d_star[i][0],self.aq(_positive,_negative)])

        return _result

    def aq(self, positive, negative):
        _star = []

        pos1 = [positive[0]]

        for seed in pos1:
            print "Seed: " + str(seed)


            ## compute partial star
            _partial_star = self.partial_star(seed,negative)

            _covered = False
            for i in xrange(len(_partial_star)):
                for k in xrange(len(_star)):
                    if _star[k] == _partial_star[i]:
                        _covered = True
                        break
                if _covered:
                    break

            if not _covered:
                _star += _partial_star

        return _star

    def partial_star(self,seed,negative):
        _partial_star = []
        _dct_partial_star = []
        _covered_universe = []
        _seed_value = self._dataset.universe[seed]
        _attributes = self._dataset.attributes

        for case in negative:
            _new_partial = []
            _dct_new_partial = []
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
            ## Possible Dictionary Implementation
            ##
            _selector_dictionary = dict()

            for i in xrange(len(_attributes)):
                _universe_attribute = self._dataset.universe[case][0][i]
                _seed_attribute = self._dataset.universe[seed][0][i]

                if _universe_attribute != _seed_attribute:
                    _selector_dictionary.update({self._dataset.attributes[0][i]:"NOT " + str(self._dataset.universe[case][0][i])})

            print "New Selectors: " + str(_selectors)
            print "Dictionary: " + str(_selector_dictionary)

            ##
            ## If these are the first selectors, they will each be the beginning of 
            ## a conjunction
            ##
            if len(_covered_universe) == 0:
                for selector in _selectors:
                    _new_partial.append([selector])
                _partial_star = _new_partial

                _dct_new_partial.append( _selector_dictionary )
                _dct_partial_star.append(_dct_new_partial)

            else:
                ##
                ## First conjunction
                ##
                if len(_covered_universe) == 1:
                    for i in _partial_star:
                        for j in _selectors:
                            _conjunction = (i[0],j)
                            _new_partial.append(list(set(_conjunction)))

                    _partial_star =_new_partial
                    
                    _updated_dict = dict()
                    print "hjere"
                    # print
                    # print "Current Selectors: " + str(_selector_dictionary)                
                    # print "DCT: " + str(_dct_partial_star)
                    # print "Comp to: " + str(_partial_star)
                    # print
                    # print

                    for i in [_selector_dictionary]:
                        for j in _dct_partial_star:
                            print "conj: " + str([i,j])



                else:
                    ##
                    ## Make sure that case isn't already covered
                    ##
                    _covered = False
                    for conjunction in _partial_star:
                        if set(_selectors) == set(conjunction):
                            continue
                        elif set(_selectors).issuperset(set(conjunction)):
                            _covered = True
                            break
                    
                    if not _covered:

                        for i in _partial_star:
                            for j in _selectors:

                                _new_conjunction = []
                                for complex in i:
                                    _new_conjunction.append(complex)
                                _new_conjunction.append(j)

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
