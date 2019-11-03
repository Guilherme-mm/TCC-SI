from math import *
from .SimilarityAlgorithm import SimilarityAlgorithm

class CosineSimilarity(SimilarityAlgorithm):

    def square_rooted(self, x):
        return round(sqrt(sum([a*a for a in x])),3)

    def calculateSimilarityScore(self, vector, secondVector):
        numerator = sum(a*b for a,b in zip(vector,secondVector))
        denominator = self.square_rooted(vector) * self.square_rooted(secondVector)
        return round(numerator/float(denominator),3)
