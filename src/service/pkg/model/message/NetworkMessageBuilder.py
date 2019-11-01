from .NetworkMessage import NetworkMessage
from .MessageType import MessageType
from ..patterns.Builder import Builder

class NetworkMessageBuilder(Builder):

    def __init__(self):
        self.networkMessage = NetworkMessage()

    def content(self, content:str) -> 'NetworkMessageBuilder':
        self.networkMessage.setContent(content)
        return self

    def senderAddress(self, address:str) -> 'NetworkMessageBuilder':
        self.networkMessage.setSenderAddress(address)
        return self

    def senderPort(self, port:int) -> 'NetworkMessageBuilder':
        self.networkMessage.setSenderPort(port)
        return self

    def receiverAddress(self, address:str) -> 'NetworkMessageBuilder':
        self.networkMessage.setReceiverAddress(address)
        return self

    def receiverPort(self, port:int) -> 'NetworkMessageBuilder':
        self.networkMessage.setReceiverPort(port)
        return self

    def messageType(self, messageType:MessageType) -> 'NetworkMessageBuilder':
        self.networkMessage.setMessageType(messageType)
        return self

    def status(self, status:int) -> 'NetworkMessageBuilder':
        self.networkMessage.setStatus(status)
        return self

    def build(self):
        return self.networkMessage
