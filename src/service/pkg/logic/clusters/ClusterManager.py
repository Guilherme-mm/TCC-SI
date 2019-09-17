from .ClusterAlgorithmsTypes import ClusterAlgorithmsTypes
from ...database.storage.ConfigurationsManager import ConfigurationsManager

class ClusterManager():
    def __init__(self):
        self.__configManager = ConfigurationsManager()
        configuredClusterAlgorithm = self.__configManager.getConfiguration("clusterAlgorithm")
        clusterAlgorithmsTypes = ClusterAlgorithmsTypes(configuredClusterAlgorithm)
        self.__clusterAlgorithm = clusterAlgorithmsTypes.instantiateClusterAlgorithm()
        self.__clusterObject = None

    def generateCluster(self, similarityMatrix):
        self.__clusterObject = self.__clusterAlgorithm.cluster(similarityMatrix)

    def getClusterObject(self):
        return self.__clusterObject
