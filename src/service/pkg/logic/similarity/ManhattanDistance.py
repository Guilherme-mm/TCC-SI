from .SimilarityAlgorithm import SimilarityAlgorithm

class ManhattanDistance(SimilarityAlgorithm):

    def calculateSimilarityScore(self, vector, secondVector):
        absoluteDistance = sum(abs(a-b) for a,b in zip(vector, secondVector))

        try:
            simIndex = 1/absoluteDistance
        except ZeroDivisionError:
            simIndex = 1

        return simIndex
