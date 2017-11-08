

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
        _positive = [positive[0]]
        for seed in _positive:
            ## Check to see if seed is already covered

            ## If not covered, compute partial star
            _partial_star = self.partial_star(seed,negative)

        return _star

    def partial_star(self,seed,negative):
        _partial_star = []
        _covered_universe = []
        _seed_value = self._dataset.universe[seed]
        _attributes = self._dataset.attributes

        for case in negative:
            print "G ( " + str(seed) + " | " + str(case) + " )"
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
                    # print "New Selectors: " + str(_selectors)
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
                        # print "Set of Selectors: " + str(_selector) + "\tConjunction: " + str(conjunction)
                        if set(_selectors).issuperset(set(conjunction)):
                            _covered = True
                            # print "covered"
                            break
                    
                    if not _covered:
                        # print "New Selectors: " + str(_selectors)
                        # print "Current Partial Star: " + str(_partial_star)
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
                ## Simplify first conjunction
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

            #     print "New Partial Star: "+ str(_new_partial)

            # print
            

            _covered_universe.append(case)
                
        print _partial_star
        return _partial_star
