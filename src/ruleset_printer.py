# @file: ruleset_printer.py
# @author: Abraham Dick
# @date: October 2017
# @desc: Creates the two files needed for processed rules

class Printer(object):

    def __init__(self):
        self._rules = None
        self._name = ""

    def printer(self,rules,name):
        self._name = name
        self.rules(rules[0])
        self.negation(rules[1])

    def negation(self,rules):
        with open("results/" + self._name + ".with.negation.rul",'w') as output:
            for i in rules:
                output.write(str(i) + "\n")

    def rules(self,rules):
        with open("results/" + self._name + ".without.negation.rul",'w') as output:
            for i in rules:
                output.write(str(i) + "\n")