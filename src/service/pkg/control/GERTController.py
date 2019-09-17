import os.path

from typing import Generator

from ..model.message.Message import Message
from ..model.message.MessageType import MessageType
from ..database.storage.ConfigurationsManager import ConfigurationsManager
from ..logic.similarity.SimilarityAlgorithmsTypes import SimilarityAlgorithmsTypes
from ..logic.similarity.SimilaritySystemFacade import SimilaritySystemFacade
from ..logic.data.DataManipulationSystemFacade import DataManipulationSystemFacade
from ..logic.clusters.ClusterAlgorithmsTypes import ClusterAlgorithmsTypes
from ..logic.recomendation.RecommendationSystemFacade import RecommendationSystemFacade
from ..logic.recomendation.SelectionAlgorithmsTypes import SelectionAlgorithmsTypes

class GERTController():

    def setLogPath(self, logPath:str) -> Generator:
        yield Message("Validating provided path...", MessageType.CONTINUATION)

        if not os.path.exists(logPath):
            pass

        yield Message("Path is valid!", MessageType.CONTINUATION)
        yield Message("Persisting provided path in {} key...".format("clientLogPath"), MessageType.CONTINUATION)
        configManager = ConfigurationsManager()

        result = configManager.setConfiguration("clientLogPath", logPath)

        if result["updated"] == 0 and result["inserted"] == 0:
            yield Message("The new provided path is identical to the current value. No changes were made.", MessageType.CONTINUATION)
        else:
            if result["updated"] > 0:
                yield Message("The client data logs path was successfully updated!", MessageType.CONTINUATION)

            if result["inserted"] > 0:
                yield Message("The client data logs path was saved in a new configuration key", MessageType.CONTINUATION)

        if result["cached_in_memory"]:
            yield Message("Configuration cached in memory with success", MessageType.END)
        else:
            yield Message("Configuration could not be cached in memory", MessageType.END)

    def updateModel(self) -> Generator:
        print("Starting model atualization routine")
        yield Message("Starting model update logic...", MessageType.CONTINUATION)

        print("Starting sub-systems facades")
        dataSystemFacade = DataManipulationSystemFacade()
        similaritySystemFacade = SimilaritySystemFacade()

        print("Opening data file and creating generator")
        logEntriesGenerator = dataSystemFacade.collectClientLogData()

        print("Calculating similarities from log entries readed")
        similarityData = similaritySystemFacade.calculateSimilarities(logEntriesGenerator)
        similaritySystemFacade.persistSimilarities(similarityData["similarityMatrix"], similarityData["rowActorsMap"])
        dataSystemFacade.persistClientData(similarityData["clientExtractedData"], similarityData["clientExtractedDataMap"])

        yield Message("Model update complete!", MessageType.END)
        print("Model successfully updated")

    def setSimilarityEngine(self, engineName:str) -> Generator:
        yield Message("Checking engine...", MessageType.CONTINUATION)

        # validating the provided engine name
        try:
            SimilarityAlgorithmsTypes(engineName)
            yield Message("Selected engine is valid!", MessageType.CONTINUATION)
        except ValueError:
            yield Message("Invalid engine name provided. Exiting.", MessageType.END)
            return

        configManager = ConfigurationsManager()
        print("setting {}".format(engineName))
        result = configManager.setConfiguration("similarityEngine", engineName)

        if result["updated"] == 0 and result["inserted"] == 0:
            yield Message("The provided engine and the previusly configured are the same. No changes were made.", MessageType.CONTINUATION)
        else:
            if result["updated"] > 0 or result["inserted"] > 0:
                yield Message("Similarity engine successfully configured!", MessageType.CONTINUATION)

        if result["cached_in_memory"]:
            yield Message("Configuration cached in memory with success", MessageType.END)
        else:
            yield Message("Configuration could not be cached in memory", MessageType.END)

    def setClusterAlgorithm(self, algorithmName:str) -> Generator:
        yield Message("Validating algorithm name...", MessageType.CONTINUATION)

        try:
            ClusterAlgorithmsTypes(algorithmName)
            yield Message("OK", MessageType.CONTINUATION)
        except ValueError:
            yield Message("Invalid engine name provided. Exiting.", MessageType.END)
            return

        configManager = ConfigurationsManager()
        print("setting {}".format(algorithmName))
        result = configManager.setConfiguration("clusterAlgorithm", algorithmName)

        if result["updated"] == 0 and result["inserted"] == 0:
            yield Message("The provided algorithm and the previusly configured are the same. No changes were made.", MessageType.CONTINUATION)
        else:
            if result["updated"] > 0 or result["inserted"] > 0:
                yield Message("Cluster algorithm successfully configured!", MessageType.CONTINUATION)

        if result["cached_in_memory"]:
            yield Message("Configuration cached in memory with success", MessageType.END)
        else:
            yield Message("Configuration could not be cached in memory", MessageType.END)

    def setRecommendationSelectionAlgorithm(self, algorithmName:str) -> Generator:
        yield Message("Validating algorithm name...", MessageType.CONTINUATION)

        try:
            SelectionAlgorithmsTypes(algorithmName)
            yield Message("OK", MessageType.CONTINUATION)
        except ValueError:
            yield Message("Invalid engine name provided. Exiting.", MessageType.END)
            return

        configManager = ConfigurationsManager()
        print("setting {}".format(algorithmName))
        result = configManager.setConfiguration("selectionAlgorithm", algorithmName)

        if result["updated"] == 0 and result["inserted"] == 0:
            yield Message("The provided algorithm and the previusly configured are the same. No changes were made.", MessageType.CONTINUATION)
        else:
            if result["updated"] > 0 or result["inserted"] > 0:
                yield Message("Recommendation selection algorithm successfully configured!", MessageType.CONTINUATION)

        if result["cached_in_memory"]:
            yield Message("Configuration cached in memory with success", MessageType.END)
        else:
            yield Message("Configuration could not be cached in memory", MessageType.END)

    def getRecommendations(self, actorId:str, quantity:int) -> Generator:
        recommendationFacade = RecommendationSystemFacade()
        recommendations = recommendationFacade.getRecommendations(actorId, quantity)

        yield Message(recommendations, MessageType.END)
