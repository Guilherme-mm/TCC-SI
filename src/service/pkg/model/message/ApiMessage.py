from .MessageType import MessageType
from .Message import Message

class ApiMessage(Message):
    def __init__(self, messageBody:str, senderAddress:str, senderPort:int, receiverAddress:str, receiverPort:int, messageType:MessageType = MessageType.BEGIN):
        self.messageBody = messageBody
        self.senderAddress = senderAddress
        self.senderPort = senderPort
        self.receiverAddress = receiverAddress
        self.receiverPort = receiverPort
        self.messageType = messageType

    def getMessageBody(self) -> str:
        return self.messageBody

    def getSenderAddress(self) -> str:
        return self.senderAddress

    def getSenderPort(self) -> int:
        return self.senderPort

    def getReceiverAddress(self) -> str:
        return self.receiverAddress

    def getReceiverPort(self) -> int:
        return self.receiverPort

    def getMessageType(self) -> MessageType:
        return self.messageType

    def setMessageType(self, messageType:MessageType) -> None:
        self.messageType = messageType
