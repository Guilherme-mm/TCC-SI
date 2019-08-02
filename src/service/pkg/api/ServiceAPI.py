import json
from ..model.patterns.Observer import Observer
from ..network.UDPComunicationManager import UDPComunicationManager
from ..control.GERTController import GERTController
from ..exception.InvalidMessageType import InvalidMessageType
from .ApiMessage import ApiMessage
from .MessageType import MessageType

class ServiceAPI(Observer):
    """
        The service api for command line interactions.
    """

    def __init__(self):
        self.udp_manager = UDPComunicationManager()
        self.__applicationController = GERTController()

    def run(self):
        """
            Makes the API start listening for incoming messages
        """
        self.udp_manager.up()
        self.udp_manager.registerObserver(self)

    def notify(self, data:ApiMessage):
        """
            Implementation of the abstract method for being notificated given a event subscription

            parameters
            ----------
            data: Mixed
                The data sended by the notificator.
        """
        try:
            messageBody = json.loads(data.getMessageBody())
            if not messageBody["operationCode"]:
                raise ValueError("No operation code provided")
            if not messageBody["messageType"]:
                raise ValueError("No message type provided")

            if messageBody["messageType"] == MessageType.BEGIN.value:
                generator = self.__applicationController.execute(messageBody["operationCode"])
                for i in generator:
                    print(i)
            else:
                raise InvalidMessageType("No valid message type provided on the body 'messageType' attribute")

        except ValueError as error:
            responseBody = {}
            responseBody["status"] = 401
            responseBody["message"] = "The message body is not a valid JSON"
            responseBody["errorMessage"] = str(error)
            responseBody["messageType"] = MessageType.END.value
            response = ApiMessage(json.dumps(responseBody), data.getReceiverAddress(), data.getReceiverPort(), data.getSenderAddress(), data.getSenderPort(), MessageType.END)
            self.udp_manager.sendMessage(response)
        except InvalidMessageType as error:
            responseBody = {}
            responseBody["status"] = 401
            responseBody["message"] = "Invalid message type"
            responseBody["errorMessage"] = str(error)
            responseBody["messageType"] = MessageType.END.value
            response = ApiMessage(json.dumps(responseBody), data.getReceiverAddress(), data.getReceiverPort(), data.getSenderAddress(), data.getSenderPort(), MessageType.END)
            self.udp_manager.sendMessage(response)
