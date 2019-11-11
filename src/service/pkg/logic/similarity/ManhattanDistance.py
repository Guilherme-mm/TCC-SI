import math
from .SimilarityAlgorithm import SimilarityAlgorithm

class ManhattanDistance(SimilarityAlgorithm):

    def calculateSimilarityScore(self, vector, secondVector):
        absoluteDistance = sum(abs(a-b) for a,b in zip(vector, secondVector))

        try:
            simIndex = 1/absoluteDistance

            if math.isinf(simIndex) and simIndex > 0:
                print("positive infinity found! {}".format(absoluteDistance))
                simIndex = 1
            else:
                if math.isinf(simIndex) and simIndex < 0:
                    print("Negative infinity foiund! {}".format(absoluteDistance))
                    simIndex = -1

        except ZeroDivisionError:
            simIndex = 1

        return simIndex
