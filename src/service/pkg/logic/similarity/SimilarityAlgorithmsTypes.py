from enum import Enum, unique
from .SimilarityAlgorithm import SimilarityAlgorithm
from .SimpleEuclidean import SimpleEuclidean

@unique
class SimilarityAlgorithmsTypes(Enum):
    SIMPLE_EUCLIDEAN = "simpleEuclidean"

    def instantiateSimilarityAlgorithm(self) -> SimilarityAlgorithm:
        instanceValue = self.value
        if instanceValue == "simpleEuclidean": # pylint: disable=comparison-with-callable
            return SimpleEuclidean()
