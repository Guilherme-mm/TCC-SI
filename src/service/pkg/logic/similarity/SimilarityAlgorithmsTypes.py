from enum import Enum, unique
from .SimilarityAlgorithm import SimilarityAlgorithm
from .SimpleEuclidean import SimpleEuclidean
from .PearsonCorrelation import PearsonCorrelation

@unique
class SimilarityAlgorithmsTypes(Enum):
    SIMPLE_EUCLIDEAN = "simpleEuclidean"
    PEARSON_CORRELATION = "pearsonCorrelation"

    def instantiateSimilarityAlgorithm(self) -> SimilarityAlgorithm:
        instanceValue = self.value
        if instanceValue == "simpleEuclidean": # pylint: disable=comparison-with-callable
            return SimpleEuclidean()

        if instanceValue == "pearsonCorrelation": # pylint: disable=comparison-with-callable
            return PearsonCorrelation()
