import numpy
from .SimilarityAlgorithm import SimilarityAlgorithm

class SimpleEuclidean(SimilarityAlgorithm):
    def __init__(self):
        pass

    def calculateSimilarityScore(self, vector, secondVector):
        return float(format(numpy.sqrt(numpy.sum((vector-secondVector)**2)), '.2f'))

    def calculateSimilarityMatrix(self, dataMatrix):
        rowsNumber = numpy.size(dataMatrix, 0)
        similarityMatrix = numpy.zeros(shape=(rowsNumber, rowsNumber))

        print("Iterating over {} rows".format(rowsNumber))
        index = 0
        while index  < rowsNumber:
            secondIndex = 0
            while secondIndex < rowsNumber:
                if index == secondIndex:
                    secondIndex += 1
                    continue

                simScore = self.calculateSimilarityScore(dataMatrix[index], dataMatrix[secondIndex])

                similarityMatrix[index, secondIndex] = simScore
                secondIndex += 1

            index += 1

        print("Similarity matrix calculated successfully")
        return similarityMatrix
