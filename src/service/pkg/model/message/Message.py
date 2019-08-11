from .MessageType import MessageType

class Message():
    def __init__(self, messageBody:str="", messageType:MessageType=None):
        self.__body = messageBody
        self.__type = messageType

    def getMessageBody(self) -> str:
        return self.__body

    def getMessageType(self) -> MessageType:
        return self.__type
