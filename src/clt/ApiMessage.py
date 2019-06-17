class ApiMessage:
    def __init__(self, messageBody, senderAddress, senderPort, receiverAddress, receiverPort):
        self.messageBody = messageBody
        self.senderAddress = senderAddress
        self.senderPort = senderPort
        self.receiverAddress = receiverAddress
        self.receiverPort = receiverPort

    def getMessageBody(self):
        return self.messageBody

    def getSenderAddress(self):
        return self.senderAddress

    def getSenderPort(self):
        return self.senderPort

    def getReceiverAddress(self):
        return self.receiverAddress

    def getReceiverPort(self):
        return self.receiverPort