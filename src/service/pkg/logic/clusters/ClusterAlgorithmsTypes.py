from enum import Enum, unique
from .ClusterAlgorithm import ClusterAlgorithm
from .HierarchicalCluster import HierarchicalCluster

@unique
class ClusterAlgorithmsTypes(Enum):
    NO_CLUSTER = "noCluster"
    HIERARCHICAL_CLUSTER = "hierarchicalCluster"

    def instantiateClusterAlgorithm(self) -> ClusterAlgorithm:
        instanceValue = self.value
        if instanceValue == "hierarchicalCluster": # pylint: disable=comparison-with-callable
            return HierarchicalCluster()

        if instanceValue == "noCluster":
            return NoCluster()
