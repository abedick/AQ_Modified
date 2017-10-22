

class Printer(object):

    def __init__(self):
        self._rules = None

    def printer(self,rules,decision):
        with open("my-data.with.negation.rul",'w') as output:


            for i in range(0,len(rules)):
                for j in range(0,len(rules[i][1])):
                    for k in range(0,len(rules[i][1][j])):
                        output.write(str(rules[i][1][j][k]))

                        if ((len(rules[i][1][j][k]) > 1) and (k != len(rules[i][1][j])-1)):
                            output.write(" AND ")
                    output.write(" -> (" + str(decision) + ", " + str(rules[i][0][0]) + ")")
                    output.write("\n")
                output.write("\n")

