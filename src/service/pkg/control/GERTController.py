import os.path
import json

from typing import Generator

from ..model.message.MessageType import MessageType
from ..model.message.NetworkMessage import NetworkMessage
from ..database.storage.ConfigurationsStorage import ConfigurationsStorage
from ..logic.similarity.SimilarityAlgorithmsTypes import SimilarityAlgorithmsTypes
from ..logic.similarity.SimilaritySystemFacade import SimilaritySystemFacade
from ..logic.data.DataManipulationSystemFacade import DataManipulationSystemFacade
from ..logic.clusters.ClusterAlgorithmsTypes import ClusterAlgorithmsTypes
from ..logic.recomendation.RecommendationSystemFacade import RecommendationSystemFacade
from ..logic.recomendation.SelectionAlgorithmsTypes import SelectionAlgorithmsTypes
from ..network.NetworkManagerFactory import NetworkManagerFactory
from ..model.message.NetworkMessageBuilder import NetworkMessageBuilder

class GERTController():

    def __init__(self):
        self.networkManager = NetworkManagerFactory.create()

    def __sendMessageToRequester(self, messageContent:str, messageType:MessageType, requestNetworkMessage:NetworkMessage, status:int=200):
        responseMessage = NetworkMessageBuilder() \
            .content(messageContent) \
            .status(status) \
            .messageType(messageType) \
            .senderAddress(requestNetworkMessage.getReceiverAddress()) \
            .senderPort(requestNetworkMessage.getReceiverPort()) \
            .receiverAddress(requestNetworkMessage.getSenderAddress()) \
            .receiverPort(requestNetworkMessage.getSenderPort()) \
            .build()

        self.networkManager.sendMessage(responseMessage)

    def setLogPath(self, logPath:str, requestNetworkMessage:NetworkMessage) -> Generator:
        self.__sendMessageToRequester(messageContent="Validating provided path...", messageType=MessageType.CONTINUATION, requestNetworkMessage=requestNetworkMessage)

        if not os.path.exists(logPath):
            pass

        self.__sendMessageToRequester(messageContent="Path is valid!", messageType=MessageType.CONTINUATION, requestNetworkMessage=requestNetworkMessage)
        configManager = ConfigurationsStorage()

        result = configManager.setConfiguration("clientLogPath", logPath)

        if result["updated"] == 0 and result["inserted"] == 0:
            self.__sendMessageToRequester(messageContent="The new provided path is identical to the current value. No changes were made.", messageType=MessageType.CONTINUATION, requestNetworkMessage=requestNetworkMessage)
        else:
            if result["updated"] > 0:
                self.__sendMessageToRequester(messageContent="The client data logs path was successfully updated!", messageType=MessageType.CONTINUATION, requestNetworkMessage=requestNetworkMessage)

            if result["inserted"] > 0:
                self.__sendMessageToRequester(messageContent="The client data logs path was saved in a new configuration key", messageType=MessageType.CONTINUATION, requestNetworkMessage=requestNetworkMessage)

        if result["cached_in_memory"]:
            self.__sendMessageToRequester(messageContent="Configuration cached in memory with success", messageType=MessageType.END, requestNetworkMessage=requestNetworkMessage)
        else:
            self.__sendMessageToRequester(messageContent="Configuration could not be cached in memory", messageType=MessageType.END, requestNetworkMessage=requestNetworkMessage)

    def updateModel(self, requestNetworkMessage:NetworkMessage) -> Generator:
        print("Starting model atualization routine")
        self.__sendMessageToRequester(messageContent="Starting model update logic...!", messageType=MessageType.CONTINUATION, requestNetworkMessage=requestNetworkMessage)

        print("Starting sub-systems facades")
        dataSystemFacade = DataManipulationSystemFacade()
        similaritySystemFacade = SimilaritySystemFacade()

        print("Opening data file and creating generator")
        logEntriesGenerator = dataSystemFacade.collectClientLogData()

        print("Calculating similarities from log entries readed")
        similarityData = similaritySystemFacade.calculateSimilarities(logEntriesGenerator)
        similaritySystemFacade.persistSimilarities(similarityData["similarityMatrix"], similarityData["rowActorsMap"])
        dataSystemFacade.persistClientData(similarityData["clientExtractedData"], similarityData["clientExtractedDataMap"])

        self.__sendMessageToRequester(messageContent="Model update complete!", messageType=MessageType.END, requestNetworkMessage=requestNetworkMessage)
        print("Model successfully updated")

    def setSimilarityEngine(self, engineName:str, requestNetworkMessage:NetworkMessage):
        self.__sendMessageToRequester(messageContent="Checking engine...", messageType=MessageType.CONTINUATION, requestNetworkMessage=requestNetworkMessage)

        # validating the provided engine name
        try:
            SimilarityAlgorithmsTypes(engineName)
            self.__sendMessageToRequester(messageContent="Selected engine is valid!", messageType=MessageType.CONTINUATION, requestNetworkMessage=requestNetworkMessage)
        except ValueError:
            self.__sendMessageToRequester(messageContent="Invalid engine name provided. Exiting.", messageType=MessageType.END, requestNetworkMessage=requestNetworkMessage)

        configManager = ConfigurationsStorage()
        result = configManager.setConfiguration("similarityEngine", engineName)

        if result["updated"] == 0 and result["inserted"] == 0:
            self.__sendMessageToRequester(messageContent="The provided engine and the previusly configured are the same. No changes were made.", messageType=MessageType.CONTINUATION, requestNetworkMessage=requestNetworkMessage)
        else:
            if result["updated"] > 0 or result["inserted"] > 0:
                self.__sendMessageToRequester(messageContent="Similarity engine successfully configured!", messageType=MessageType.CONTINUATION, requestNetworkMessage=requestNetworkMessage)

        if result["cached_in_memory"]:
            self.__sendMessageToRequester(messageContent="Configuration cached in memory with success", messageType=MessageType.END, requestNetworkMessage=requestNetworkMessage)
        else:
            self.__sendMessageToRequester(messageContent="Configuration could not be cached in memory", messageType=MessageType.END, requestNetworkMessage=requestNetworkMessage)

    def setClusterAlgorithm(self, algorithmName:str) -> Generator:
        yield Message("Validating algorithm name...", MessageType.CONTINUATION)

        try:
            ClusterAlgorithmsTypes(algorithmName)
            yield Message("OK", MessageType.CONTINUATION)
        except ValueError:
            yield Message("Invalid engine name provided. Exiting.", MessageType.END)
            return

        configManager = ConfigurationsStorage()
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

        configManager = ConfigurationsStorage()
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

    def setTestDataPath(self, path:str, requestNetworkMessage:NetworkMessage):
        self.__sendMessageToRequester(messageContent="Validating provided path...", messageType=MessageType.CONTINUATION, requestNetworkMessage=requestNetworkMessage)

        if not os.path.exists(path):
            self.__sendMessageToRequester(messageContent="The provided path is invalid. The file does not exists.", messageType=MessageType.END, requestNetworkMessage=requestNetworkMessage)
            return

        self.__sendMessageToRequester(messageContent="Path is valid!", messageType=MessageType.CONTINUATION, requestNetworkMessage=requestNetworkMessage)
        self.__sendMessageToRequester(messageContent="Persisting the configuration", messageType=MessageType.CONTINUATION, requestNetworkMessage=requestNetworkMessage)

        configManager = ConfigurationsStorage()
        result = configManager.setConfiguration("testDataPath", path)

        if result["updated"] == 0 and result["inserted"] == 0:
            self.__sendMessageToRequester(messageContent="The new provided path is identical to the current value. No changes were made.", messageType=MessageType.CONTINUATION, requestNetworkMessage=requestNetworkMessage)
        else:
            if result["updated"] > 0:
                self.__sendMessageToRequester(messageContent="The client data logs path was successfully updated!", messageType=MessageType.CONTINUATION, requestNetworkMessage=requestNetworkMessage)

            if result["inserted"] > 0:
                self.__sendMessageToRequester(messageContent="The client data logs path was saved in a new configuration key", messageType=MessageType.CONTINUATION, requestNetworkMessage=requestNetworkMessage)

        if result["cached_in_memory"]:
            self.__sendMessageToRequester(messageContent="Configuration cached in memory with success", messageType=MessageType.END, requestNetworkMessage=requestNetworkMessage)
        else:
            self.__sendMessageToRequester(messageContent="Configuration could not be cached in memory", messageType=MessageType.END, requestNetworkMessage=requestNetworkMessage)

    def testRecommendationsAccuracy(self, requestNetworkMessage:NetworkMessage):
        # self.__sendMessageToRequester(messageContent="Checking for a test data file...", messageType=MessageType.CONTINUATION, requestNetworkMessage=requestNetworkMessage)

        # configManager = ConfigurationsStorage()
        # testDataFilePath = configManager.getConfiguration("testDataPath")

        recommendationFacade = RecommendationSystemFacade()
        result = recommendationFacade.testRecommendationsAccuracy()
        self.__sendMessageToRequester(messageContent="Testing completed", messageType=MessageType.CONTINUATION, requestNetworkMessage=requestNetworkMessage)
        self.__sendMessageToRequester(messageContent="Average variation: {}. Missed recommendations: {}".format(result["variationAvg"], result["missedRecommendations"]), messageType=MessageType.END, requestNetworkMessage=requestNetworkMessage)

    def clearGraphDB(self, requestNetworkMessage:NetworkMessage):
        simSystemFacade = SimilaritySystemFacade()
        simSystemFacade.clearPersistedSimData()

        self.__sendMessageToRequester(messageContent="Data wipe completed!", messageType=MessageType.END, requestNetworkMessage=requestNetworkMessage)

    def clearDataDB(self, requestNetworkMessage:NetworkMessage):
        dataSystemFacade = DataManipulationSystemFacade()

        dataSystemFacade.clearClientData()
        self.__sendMessageToRequester(messageContent="Data wipe completed!", messageType=MessageType.END, requestNetworkMessage=requestNetworkMessage)

    def getConfigurationValue(self, configurationName:str, requestNetworkMessage:NetworkMessage):
        configStorage = ConfigurationsStorage()
        result = configStorage.getConfiguration(configurationName)

        self.__sendMessageToRequester(messageContent=result, messageType=MessageType.END, requestNetworkMessage=requestNetworkMessage)