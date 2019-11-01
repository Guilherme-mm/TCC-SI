import json
from .MessageType import MessageType

class NetworkMessage():
    def __init__(self):
        self.__senderAddress = ""
        self.__senderPort = None
        self.__receiverAddress = ""
        self.__receiverPort = None
        self.__messageType = MessageType.BEGIN
        self.__content = ""
        self.__status = None

    def getMessageBody(self) -> str:
        bodyDict = {}
        bodyDict["messageContent"] = self.getContent()
        bodyDict["messageType"] = self.getMessageType().value
        return json.dumps(bodyDict)

    def getSenderAddress(self) -> str:
        return self.__senderAddress

    def getSenderPort(self) -> int:
        return self.__senderPort

    def getReceiverAddress(self) -> str:
        return self.__receiverAddress

    def getReceiverPort(self) -> int:
        return self.__receiverPort

    def getMessageType(self) -> MessageType:
        return self.__messageType

    def getContent(self) -> str:
        return self.__content

    def setMessageType(self, messageType:MessageType) -> None:
        self.__messageType = messageType

    def setContent(self, content:str) -> None:
        self.__content = content

    def setSenderAddress(self, address:str) -> None:
        self.__senderAddress = address

    def setSenderPort(self, port:int) -> None:
        self.__senderPort = port

    def setReceiverAddress(self, address:str) -> None:
        self.__receiverAddress = address

    def setReceiverPort(self, port:int) -> None:
        self.__receiverPort = port

    def setStatus(self, status:int) -> None:
        self.__status = status
