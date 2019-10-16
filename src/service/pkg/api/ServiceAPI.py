import json
from ..model.patterns.Observer import Observer
from ..network.UDPCommunicationManager import UDPCommunicationManager
from ..control.GERTController import GERTController
from ..control.operation.OperationCode import OperationCode
from ..exception.InvalidMessageTypeException import InvalidMessageTypeException
from ..exception.MissingParameterException import MissingParameterException
from ..model.message.ApiMessage import ApiMessage
from ..model.message.MessageType import MessageType

class ServiceAPI(Observer):
    """
        The service api for command line interactions.
    """

    def __init__(self):
        # Initializes the communication manager based on the UDP protocol
        self.communication_manager = UDPCommunicationManager()

        # Creates a instance of the application main controller
        self.__applicationController = GERTController()

    def run(self):
        """
            Makes the API start listening for incoming messages
        """
        # Starts listening for messages
        self.communication_manager.up()
        # Passes to the communication manager a instance of itself to be notified when incoming messages are ready to be processed
        self.communication_manager.registerObserver(self)

    def notify(self, message:ApiMessage):
        """
            @overridesParent
            Called every time a new message received by the communication manager is ready to be processed

            parameters
            ----------
            message: Mixed
                The message sended by the notificator.
        """
        try:
            messageBody = json.loads(message.getMessageBody())

            # Every message must have a type
            if not messageBody["messageType"]:
                raise ValueError("No message type provided")

            # If the message type is "Begin", then a new operation should be started.
            if messageBody["messageType"] == MessageType.BEGIN.value:
                # The execute method of the application main controller returns a generator. This is used to allow communication even during the operation execution.
                generator = self.execute(OperationCode(messageBody["operationCode"]), messageBody)

                # Each "i" position of the generator is a message yielded by the application main controller. Those messages are converted to ApiMessage objects and fowarded to the communication manager
                for i in generator:
                    responseBody = {}
                    responseBody["status"] = 200
                    responseBody["content"] = i.getMessageBody()
                    responseBody["messageType"] = i.getMessageType().value
                    response = ApiMessage(json.dumps(responseBody), message.getReceiverAddress(), message.getReceiverPort(), message.getSenderAddress(), message.getSenderPort(), MessageType.END)
                    self.communication_manager.sendMessage(response)
            else:
                raise InvalidMessageTypeException("No valid message type provided on the body 'messageType' attribute")
        # Raised if the body is not a JSON
        except ValueError as error:
            responseBody = {}
            responseBody["status"] = 401
            responseBody["message"] = "The message body is not a valid JSON"
            responseBody["errorMessage"] = str(error)
            responseBody["messageType"] = MessageType.END.value
            response = ApiMessage(json.dumps(responseBody), message.getReceiverAddress(), message.getReceiverPort(), message.getSenderAddress(), message.getSenderPort(), MessageType.END)
            self.communication_manager.sendMessage(response)
        # Raised if the body sends a unrecognized message type
        except InvalidMessageTypeException as error:
            responseBody = {}
            responseBody["status"] = 401
            responseBody["message"] = "Invalid message type"
            responseBody["errorMessage"] = str(error)
            responseBody["messageType"] = MessageType.END.value
            response = ApiMessage(json.dumps(responseBody), message.getReceiverAddress(), message.getReceiverPort(), message.getSenderAddress(), message.getSenderPort(), MessageType.END)
            self.communication_manager.sendMessage(response)
        # Called whenever a missing parameter is detected during operations executions
        except MissingParameterException as error:
            responseBody = {}
            responseBody["status"] = 401
            responseBody["message"] = error.message
            responseBody["errorMessage"] = error.errorMessage
            responseBody["messageType"] = MessageType.END.value
            response = ApiMessage(json.dumps(responseBody), message.getReceiverAddress(), message.getReceiverPort(), message.getSenderAddress(), message.getSenderPort(), MessageType.END)
            self.communication_manager.sendMessage(response)

    def execute(self, operationCode:OperationCode, data:dict):
        if operationCode == OperationCode.SET_LOG_PATH:
            try:
                generator = self.__applicationController.setLogPath(data["path"]) # pylint: disable=assignment-from-no-return
            except KeyError:
                raise MissingParameterException("No log path provided")

        if operationCode == OperationCode.UPDATE_MODEL:
            generator = self.__applicationController.updateModel()

        if operationCode == OperationCode.SET_SIMILARITY_ENGINE:
            generator = self.__applicationController.setSimilarityEngine(data["similarityEngineName"])

        if operationCode == OperationCode.SET_CLUSTER_ALGORITHM:
            generator = self.__applicationController.setClusterAlgorithm(data["clusterAlgorithmName"])

        if operationCode == OperationCode.SET_RECOMMENDATION_SELECTION_ALGORITHM:
            generator = self.__applicationController.setRecommendationSelectionAlgorithm(data["recommendationSelectionAlgorithmName"])

        if operationCode == OperationCode.GET_RECOMMENDATIONS:
            generator = self.__applicationController.getRecommendations(data["actorId"], data["quantity"])

        for i in generator:
            yield i
