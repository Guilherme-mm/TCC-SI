from enum import Enum, unique
from .SimilarityAlgorithm import SimilarityAlgorithm
from .SimpleEuclidean import SimpleEuclidean
from .PearsonCorrelation import PearsonCorrelation
from .ManhattanDistance import ManhattanDistance
from .CosineSimilarity import CosineSimilarity
from .JaccardSimilarity import JaccardSimilarity

@unique
class SimilarityAlgorithmsTypes(Enum):
    SIMPLE_EUCLIDEAN = "simpleEuclidean"
    PEARSON_CORRELATION = "pearsonCorrelation"
    MANHATTAN_DISTANCE = "manhattanDistance"
    COSINE_SIMILARITY = "cosineSimilarity"
    JACCARD_SIMILARITY = "jaccardSimilarity"

    def instantiateSimilarityAlgorithm(self) -> SimilarityAlgorithm:
        instanceValue = self.value
        if instanceValue == "simpleEuclidean": # pylint: disable=comparison-with-callable
            return SimpleEuclidean()

        if instanceValue == "pearsonCorrelation": # pylint: disable=comparison-with-callable
            return PearsonCorrelation()

        if instanceValue == "manhattanDistance": # pylint: disable=comparison-with-callable
            return ManhattanDistance()

        if instanceValue == "cosineSimilarity": # pylint: disable=comparison-with-callable
            return CosineSimilarity()

        if instanceValue == "jaccardSimilarity": # pylint: disable=comparison-with-callable
            return JaccardSimilarity()
