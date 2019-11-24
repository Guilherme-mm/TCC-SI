from ..model.patterns.Observer import Observer
from ..network.NetworkManagerFactory import NetworkManagerFactory
from ..control.GERTController import GERTController
from ..control.operation.OperationCode import OperationCode
from ..exception.InvalidMessageTypeException import InvalidMessageTypeException
from ..exception.MissingParameterException import MissingParameterException
from ..model.message.NetworkMessage import NetworkMessage
from ..model.message.MessageType import MessageType
from ..model.message.NetworkMessageBuilder import NetworkMessageBuilder

class ServiceAPI(Observer):
    def __init__(self):
        # Initializes the communication manager based on the current configurations (default is UDP)
        self.__communication_manager = NetworkManagerFactory.create()

        # Creates a instance of the application main controller
        self.__applicationController = GERTController()

    # Instantiates a new network manager and registers itself to be notified on every message received
    def run(self):
        # Starts listening for messages
        self.__communication_manager.up()

        # Passes to the communication manager a instance of itself to be notified when incoming messages are ready to be processed
        self.__communication_manager.registerObserver(self)

    # Called everytime the network manager receives a message
    def notify(self, data:object):
        try:
            # Every message must have a type
            if not data.getMessageType():
                raise ValueError("No message type provided")

            # If the message type is "Begin", then a new operation should be started.
            if data.getMessageType() == MessageType.BEGIN:
                content = data.getContent()
                self.__communication_manager.defineClient(data.getSenderAddress(), data.getSenderPort())
                self.execute(OperationCode(content["operationCode"]), content, data)

            else:
                raise InvalidMessageTypeException("No valid message type provided on the body 'messageType' attribute")

        # Raised if the body is not a JSON
        except ValueError as error:
            responseMessage = NetworkMessageBuilder() \
            .content("The message body is not a valid JSON") \
            .status(401) \
            .messageType(MessageType.END) \
            .senderAddress(data.getReceiverAddress()) \
            .senderPort(data.getReceiverPort()) \
            .receiverAddress(data.getSenderAddress()) \
            .receiverPort(data.getSenderPort()) \
            .build()

            self.__communication_manager.sendMessage(responseMessage)

        # Raised if the body sends a unrecognized message type
        except InvalidMessageTypeException as error:
            responseMessage = NetworkMessageBuilder() \
            .content("Invalid message type") \
            .status(401) \
            .messageType(MessageType.END) \
            .senderAddress(data.getReceiverAddress()) \
            .senderPort(data.getReceiverPort()) \
            .receiverAddress(data.getSenderAddress()) \
            .receiverPort(data.getSenderPort()) \
            .build()

            self.__communication_manager.sendMessage(responseMessage)

        # Called whenever a missing parameter is detected during operations executions
        except MissingParameterException as error:
            responseMessage = NetworkMessageBuilder() \
            .content(error.message) \
            .status(401) \
            .messageType(MessageType.END) \
            .senderAddress(data.getReceiverAddress()) \
            .senderPort(data.getReceiverPort()) \
            .receiverAddress(data.getSenderAddress()) \
            .receiverPort(data.getSenderPort()) \
            .build()

            self.__communication_manager.sendMessage(responseMessage)

    # Simulates a routing phase to determine wich method the application controller must execute.
    def execute(self, operationCode:OperationCode, data:dict, networkMessage:NetworkMessage):
        if operationCode == OperationCode.SET_LOG_PATH:
            self.__applicationController.setLogPath(data["path"], data["hasHeader"], data["separator"])

        if operationCode == OperationCode.UPDATE_MODEL:
            self.__applicationController.updateModel()

        if operationCode == OperationCode.SET_SIMILARITY_ENGINE:
            self.__applicationController.setSimilarityEngine(data["similarityEngineName"])

        if operationCode == OperationCode.SET_CLUSTER_ALGORITHM:
            self.__applicationController.setClusterAlgorithm(data["clusterAlgorithmName"])

        if operationCode == OperationCode.SET_RECOMMENDATION_SELECTION_ALGORITHM:
            self.__applicationController.setRecommendationSelectionAlgorithm(data["recommendationSelectionAlgorithmName"])

        if operationCode == OperationCode.GET_RECOMMENDATIONS:
            self.__applicationController.getRecommendations(data["actorId"], data["quantity"])

        if operationCode == OperationCode.SET_TEST_DATA_PATH:
            self.__applicationController.setTestDataPath(data["path"])

        if operationCode == OperationCode.TEST_RECOMMENDATIONS_ACCURACY:
            self.__applicationController.testRecommendationsAccuracy(data["quantity"], data["K"])

        if operationCode == OperationCode.CLEAR_GRAPH_DB:
            self.__applicationController.clearGraphDB(networkMessage)

        if operationCode == OperationCode.CLEAR_DATA_DB:
            self.__applicationController.clearDataDB(networkMessage)

        if operationCode == OperationCode.GET_CONFIGURATION_VALUE:
            self.__applicationController.getConfigurationValue(data["configurationName"])
