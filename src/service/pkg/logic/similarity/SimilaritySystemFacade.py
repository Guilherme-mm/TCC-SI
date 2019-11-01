from .SimilarityManager import SimilarityManager
from ...database.storage.SimilarityGraphManager import SimilarityGraphManager

class SimilaritySystemFacade():
    def __init__(self):
        print("Similarity subsystem facade instantiated")

    def calculateSimilarities(self, logEntriesGenerator):
        similarityManager = SimilarityManager()

        print("Reading lines and adding data to the vectors coordinate matrix...")
        for entry in logEntriesGenerator:
            similarityManager.putVectorCoordinate(entry.getActor(), entry.getActionObject(), entry.getValue())

        print("Data extraction done!")

        print("Generating the similarity matrix...")
        similarityManager.generateSimilarityMatrix()

        print("Returning generated sim data")
        return {
            "similarityMatrix":similarityManager.getSimilarityMatrix(),
            "rowActorsMap":similarityManager.getSimMatrixMap(),
            "clientExtractedData":similarityManager.getDataMatrix(),
            "clientExtractedDataMap": similarityManager.getDimensionsIndentificators()
        }

    def generateClusters(self):
        pass

    def persistSimilarities(self, similarityMatrix, rowActorMap):
        print("Starting sim data persist")
        simGraphManager = SimilarityGraphManager()
        return simGraphManager.generateGraphFromSimMatrix(similarityMatrix, rowActorMap)

    def getRecommendation(self):
        pass

    def clearPersistedSimData(self):
        simGraphManager = SimilarityGraphManager()
        return simGraphManager.clearGraph()
