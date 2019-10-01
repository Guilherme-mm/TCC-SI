
from scipy import stats # pylint: disable=import-error
from .SimilarityAlgorithm import SimilarityAlgorithm

class PearsonCorrelation(SimilarityAlgorithm):
    def __init__(self):
        pass

    def calculateSimilarityScore(self, vector, secondVector):
        simScore = stats.pearsonr(vector, secondVector)
        return simScore[0]
