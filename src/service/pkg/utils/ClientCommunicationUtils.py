from ..network.NetworkManagerFactory import NetworkManagerFactory
from ..model.message.NetworkMessageBuilder import NetworkMessageBuilder
from ..model.message.MessageType import MessageType

class ClientCommunicationUtils():

    @staticmethod
    def sendMessage(content:str):
        networkManager = NetworkManagerFactory.create()
        message = NetworkMessageBuilder().content(content) \
                                            .messageType(MessageType.CONTINUATION) \
                                            .build()
        networkManager.sendMessage(message)


    @staticmethod
    def sendProgress(progress:int):
        networkManager = NetworkManagerFactory.create()
        message = NetworkMessageBuilder().content(progress) \
                                            .messageType(MessageType.PROGRESS) \
                                            .build()
        networkManager.sendMessage(message)

    @staticmethod
    def sendEndMessage(content:str):
        networkManager = NetworkManagerFactory.create()
        message = NetworkMessageBuilder().content(content) \
                                            .messageType(MessageType.END) \
                                            .build()
        networkManager.sendMessage(message)
