import scipy.spatial.distance as ssd
import scipy.cluster.hierarchy as sch

class HierarchicalCluster():
    def __init__(self):
        pass

    def condenseMatrix(self, similarityMatrix):
        return ssd.squareform(similarityMatrix)

    def cluster(self, similarityMatrix):
        condensedSimMatrix = self.condenseMatrix(similarityMatrix)
        return sch.linkage(condensedSimMatrix, method="ward")
 