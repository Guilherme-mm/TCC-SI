from .SimilarityManager import SimilarityManager
from ...database.storage.SimilarityGraphManager import SimilarityGraphManager
from ...utils.ClientCommunicationUtils import ClientCommunicationUtils

class SimilaritySystemFacade():
    def __init__(self):
        print("Similarity subsystem facade instantiated")

    def calculateSimilarities(self, logEntriesGenerator, generatorSize:int):
        similarityManager = SimilarityManager()
        print("iterating over generator...", generatorSize)
        entriesCounter = 0
        for entry in logEntriesGenerator:
            entriesCounter = entriesCounter + 1
            if generatorSize:
                print("updating progress...", entriesCounter)
                ClientCommunicationUtils.sendProgress((entriesCounter * 100)/generatorSize)

            similarityManager.putVectorCoordinate(entry.getActor(), entry.getActionObject(), entry.getValue())

        ClientCommunicationUtils.sendMessage("Generating similarity matrix")
        similarityManager.generateSimilarityMatrix()

        return {
            "similarityMatrix":similarityManager.getSimilarityMatrix(),
            "rowActorsMap":similarityManager.getSimMatrixMap(),
            "clientExtractedData":similarityManager.getDataMatrix(),
            "clientExtractedDataMap": similarityManager.getDimensionsIndentificators()
        }

    def generateClusters(self):
        pass

    def persistSimilarities(self, similarityMatrix, rowActorMap):
        simGraphManager = SimilarityGraphManager()
        return simGraphManager.generateGraphFromSimMatrix(similarityMatrix, rowActorMap)

    def getRecommendation(self):
        pass

    def clearPersistedSimData(self):
        simGraphManager = SimilarityGraphManager()
        return simGraphManager.clearGraph()
