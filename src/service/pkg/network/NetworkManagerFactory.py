from .UDPCommunicationManager import UDPCommunicationManager
from.NetworkCommunicationManager import NetworkCommunicationManager
from ..database.storage.ConfigurationsStorage import ConfigurationsStorage

class NetworkManagerFactory:

    @staticmethod
    def create()->NetworkCommunicationManager:
        configurationStorage = ConfigurationsStorage()
        internalNetworkProtocol = configurationStorage.getConfiguration("InternalNetworkProtocol")

        if internalNetworkProtocol is None:
            internalNetworkProtocol = "UDP"

        if internalNetworkProtocol == "UDP":
            return UDPCommunicationManager.getInstance()
