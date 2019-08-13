"""
@author Guilherme Muller Moreira <guilherme.muller.m@gmail.com>
@version 0.1
@creation 16/07/2019

Description
-----------
    This module contains the UDPCommunicationManager class.
"""
import socket
import threading
from .NetworkCommunicationManager import NetworkCommunicationManager
from ..model.message.ApiMessage import ApiMessage
from ..model.patterns.Observer import Observer


class UDPCommunicationManager(NetworkCommunicationManager):
    """
        Implements NetworkCommunicationManager. Handles and abstracts the send/receive packages process in 
        the UDP network protocol.

        Attributes
        ----------
        __socket: Socket
            The udp socket object.
        __serverAddress: Tuple
            The pair of address and port where the socket will be listening for packages.
        __messagesQueue: Array[ApiMessage]
            Holds the messages received by the socket and are waiting to be fowarded to the 
            registered observers.
        __observers: Array[Observer]
            An array that contains the currently registered observers. Every observer on the list will be
            notified when a message is received by the socket.

        Methods
        -------
        up()
            Triggers the start process of the communication structure. This process is: 1. Bind the socket to
            the server address (__serverAddress); 2. Start a thread that keeps listening for messages on the
            socket; 3. Start a second thread that notify the registered observers of the received messages.
        registerObserver(observer)
            Adds a observer that will be notified when a message arrives.
        unregisterObserver(observer)
            Removes the given observer from the messsage notify list
        __messageListener()
            Continuously listens to the socket for incoming messages. When one is detect, its appended to the
            __messagesQueue array.
        __messageQueueProcessor()
            Monitors the __messagesQueue for messages to be sended to the registered observers. Pops the
            message from the queue everytime when it concludes the notification proccess.
    """
    def __init__(self):
        # Create a UDP socket
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__serverAddress = ('python-daemon', 10000)
        self.__messagesQueue = []
        self.__observers = []
        self.__responsesQueue = []

    def up(self):
        """
            Starts the communication structure. Binds the socket to the server address. Starts two threads
            that are responsible for catching incoming messages and for notifying them to the observers.
        """
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

    def sendMessage(self, message:ApiMessage):
        """
            Sends a message to a target host

            Parameters
            ----------
            message: ApiMessage
                The message object that will be sended

            Raises
            ------
            ValueError: If no valid target host address is provided
        """
        if not message.getReceiverAddress():
            raise ValueError("The message object do not contain a valid target address.")

        self.__responsesQueue.append(message)

    def __messageListener(self):
        while True:
            data, address = self.__socket.recvfrom(4096)
            message = ApiMessage(data.decode('utf-8'), address[0], address[1], self.__serverAddress[0], self.__serverAddress[1])
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