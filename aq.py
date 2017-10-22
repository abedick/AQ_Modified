
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

            # print "C = " + str(_pos)
            # print "F = " + str(_neg)

            _result.append([[self._dataset.d_star[i][0]],self.AQ(_pos,_neg)])

        return _result

    def AQ(self,pos,neg):
        
        cover = []

        for i in neg:
            _partical = self.star(pos[0],i)
            cover.append(_partical)

        return cover

    def star(self,seed,neg):

        _star = []

        _aq_complex = []
        for i in range(0,len(self._dataset.attributes)):

            if self._dataset.universe[seed][i] != self._dataset.universe[neg][i]:
                _complex_name = "(" + self._dataset.attributes[i] + ", NOT " + self._dataset.universe[neg][i] + ")"
                _aq_complex.append(_complex_name)

        _star = _aq_complex

        # remove all complexes that are subsumed by other complexes in star


        # Remove worst complexes (fewest number of covers)
        #  STAR <= user-defined Maximum Star (maxstar)


        return _star