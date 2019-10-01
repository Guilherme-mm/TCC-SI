import numpy # pylint: disable=import-error
from .SimilarityAlgorithmsTypes import SimilarityAlgorithmsTypes
from ...database.storage.ConfigurationsManager import ConfigurationsManager

class SimilarityManager():
    def __init__(self):
        print("Similarity manager startup routine started:")
        # Looking for the configured similarity engine
        self.__configManager = ConfigurationsManager()
        configuredSimilarityEngineName = self.__configManager.getConfiguration("similarityEngine")
        print("Using the [{}] engine".format(configuredSimilarityEngineName))
        simAlgorithmsTypes = SimilarityAlgorithmsTypes(configuredSimilarityEngineName)

        # Instantiating the correct algorithm abstraction based on the system configuration
        self.__similarityAlgorithm = simAlgorithmsTypes.instantiateSimilarityAlgorithm()
        print("Engine successfully instantiated")

        # This dictionary relationates the dimensions indentificator with a position that must be respected for every vector entry on the data matrix
        self.__dimensionsIdentificators = {}

        # holds the line index of each vector id on the distance matrix
        self.__vectorsMap = {}

        # Each position of this array is a n-dimensional vector
        self.__dataMatrix = {}

        self.__similarityMatrix = None

    def putVectorCoordinate(self, vectorId:str, dimensionId:str, coordinate:int) -> bool:
        #Checks if a vector with this id alredy exists and instantiates it if not
        if self.__dataMatrix.get(vectorId, None) is None:
            self.__dataMatrix[vectorId] = []

        # Checks if the dimensionId has alredy been added to the vector and therefore has an definde index
        coordinateIndex = -1
        if self.__dimensionsIdentificators.get(dimensionId, None) is not None:
            coordinateIndex = self.__dimensionsIdentificators[dimensionId]

        # If the dimension being added has no defined index it must be one index bigger that the bigger item on the dict. Also, its important to check if the dictionary is empty
        if coordinateIndex == -1:
            try:
                coordinateIndex = max(self.__dimensionsIdentificators.values()) +1
            except ValueError:
                coordinateIndex = 0

            # self.__dataMatrix[vectorId].append(coordinate)
            self.__dimensionsIdentificators[dimensionId] = coordinateIndex

        while not 0 <= coordinateIndex < len(self.__dataMatrix[vectorId]):
            self.__dataMatrix[vectorId].append(0)

        self.__dataMatrix[vectorId][coordinateIndex] = coordinate

    def generateSimilarityMatrix(self) -> bool:
        biggestVectorKey, biggestVector = max(self.__dataMatrix.items(), key = lambda x: len(x[1]))
        biggestVectorLen = len(biggestVector)
        # numberOfVectors = len(self.__dataMatrix.keys())

        print("Normalizing data matrix shape")
        # Grants that every vector of the data matrix has the same lenght
        for key in self.__dataMatrix:
            # print("Appending zeros at {}".format(key))
            while len(self.__dataMatrix[key]) < biggestVectorLen:
                self.__dataMatrix[key].append(0)

        print("vectors normalized at the same lenght with success")

        temporaryMatrix = []

        # Creates a list of lists (matrix) to be provided to numpy and simultaneously creates the vectorsXline map
        count = 0
        for key in self.__dataMatrix:
            temporaryMatrix.append(self.__dataMatrix[key])
            self.__vectorsMap[count] = key
            count += 1

        print("Converting data matrix to numpy arrayd")
        # Generates numpy matrix of the data array
        temporaryMatrix = numpy.array(temporaryMatrix, dtype=int)
        self.__similarityMatrix =  self.__similarityAlgorithm.calculateSimilarityMatrix(temporaryMatrix)

    def getDataMatrix(self) -> dict:
        return self.__dataMatrix

    def getDimensionsIndentificators(self) -> dict:
        return self.__dimensionsIdentificators

    def getSimMatrixMap(self) -> dict:
        return self.__vectorsMap

    def getSimilarityMatrix(self):
        return self.__similarityMatrix
