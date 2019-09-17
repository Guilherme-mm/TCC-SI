from .ClusterManager import ClusterManager

class ClusterSystemFacade():
    def __init__(self):
        print("Cluster subsystem facade instantiated")

    def generateClusterFromSimMatrix(self, similarityMatrix):
        clusterManager = ClusterManager()
        clusterManager.generateCluster(similarityMatrix)
        return clusterManager.getClusterObject()

    def persistClusterStructure(self, clusterObject):
        pass
