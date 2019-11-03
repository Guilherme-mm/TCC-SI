import socket
import threading
import json

from .NetworkCommunicationManager import NetworkCommunicationManager
from ..model.message.NetworkMessage import NetworkMessage
from ..model.message.NetworkMessageBuilder import NetworkMessageBuilder
from ..model.message.MessageType import MessageType
from ..model.patterns.Observer import Observer


class UDPCommunicationManager(NetworkCommunicationManager):
    __instance = None

    @staticmethod
    def getInstance():
        if UDPCommunicationManager.__instance is None:
            UDPCommunicationManager()

        return UDPCommunicationManager.__instance

    def __init__(self):
        if UDPCommunicationManager.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            UDPCommunicationManager.__instance = self

            # Create a UDP socket
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.__serverAddress = ('python-daemon', 10000)
            self.__messagesQueue = []
            self.__observers = []
            self.__responsesQueue = []
            self.__clientAddress = None
            self.__clientPort = None

    def up(self):
        # Bind the socket to the port
        self.__socket.bind(self.__serverAddress)

        # starts the message processing threads
        threading.Thread(target=self.__messageListener).start()
        threading.Thread(target=self.__messageQueueProcessor).start()
        threading.Thread(target=self.__responsesQueueProcessor).start()

    def registerObserver(self, observer:Observer):
        """
            Adds a observer object to be notified when a message is in process phase

            Parameters
            ----------
            observer: Observer
                The observer object in wich the notify() method will be called

            Returns
            -------
            boolean
        """
        if observer not in self.__observers:
            self.__observers.append(observer)
            return True
        return False

    def unregisterObserver(self, observer:Observer):
        """
            Removes a observer from the notifying list

            Parameters
            ----------
            observer: Observer
                The observer instance that will be removed from the notifying list

            Returns
            -------
            boolean
        """
        try:
            self.__observers.remove(observer)
            return True
        except ValueError:
            return False

    def sendMessage(self, message:NetworkMessage):
        if not message.getReceiverAddress():
            if not self.__clientAddress:
                raise ValueError("The message object do not contain a valid target address and there is no default client defined.")
            else:
                message.setReceiverAddress(self.__clientAddress)

        if not message.getReceiverPort():
            if not self.__clientPort:
                raise ValueError("The message object do not contain a valid target port and there is no default client defined.")
            else:
                message.setReceiverPort(self.__clientPort)

        self.__responsesQueue.append(message)

    def defineClient(self, clientAddress:str, clientPort:int):
        self.__clientAddress = clientAddress
        self.__clientPort = clientPort

    def __messageListener(self):
        while True:
            data, address = self.__socket.recvfrom(4096)
            data = json.loads(data.decode('utf-8'))

            messageBuilder = NetworkMessageBuilder() \
                .senderAddress(address[0]) \
                .senderPort(address[1]) \
                .receiverAddress(self.__serverAddress[0]) \
                .receiverPort(self.__serverAddress[1])

            if data.get("messageType", False):
                messageBuilder = messageBuilder.messageType(MessageType(data["messageType"]))

            if data.get("messageContent", False):
                messageBuilder = messageBuilder.content(data["messageContent"])

            message = messageBuilder.build()
            self.__messagesQueue.append(message)

    def __messageQueueProcessor(self):
        while True:
            if self.__messagesQueue:
                message = self.__messagesQueue[0]
                for observer in self.__observers:
                    observer.notify(message)
                self.__messagesQueue.pop(0)

    def __responsesQueueProcessor(self):
        while True:
            if self.__responsesQueue:
                message = self.__responsesQueue[0]
                self.__socket.sendto(message.getMessageBody().encode('utf-8'), (message.getReceiverAddress(), message.getReceiverPort()))
                self.__responsesQueue.pop(0)
