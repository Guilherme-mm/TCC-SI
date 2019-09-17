from enum import Enum, unique
from .SelectionAlgorithm import SelectionAlgorithm
from .KNN import KNN

@unique
class SelectionAlgorithmsTypes(Enum):
    KNN = "KNN"

    def instantiateSelectionAlgorithm(self) -> SelectionAlgorithm:
        instanceValue = self.value
        if instanceValue == "KNN": # pylint: disable=comparison-with-callable
            return KNN()
