from .SimilarityAlgorithm import SimilarityAlgorithm

class JaccardSimilarity(SimilarityAlgorithm):
    def calculateSimilarityScore(self, vector, secondVector):
        intersection_cardinality = len(set.intersection(*[set(vector), set(secondVector)]))
        union_cardinality = len(set.union(*[set(vector), set(secondVector)]))
        return intersection_cardinality/float(union_cardinality)
