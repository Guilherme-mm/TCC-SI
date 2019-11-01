from ...database.storage.ClientDataStorage import ClientDataStorage

class ClientDataManager():
    def __init__(self):
        pass

    def persistClientData(self, clientData, dataMap):
        clientDataStorage = ClientDataStorage()
        clientDataStorage.saveClientData(clientData, dataMap)
        return True

    def wipeClientData(self):
        clientDataStorage = ClientDataStorage()
        clientDataStorage.deleteClientData()