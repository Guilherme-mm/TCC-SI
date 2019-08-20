import os.path
from typing import Generator
from ..model.message.Message import Message
from ..model.message.MessageType import MessageType
from ..database.managers.ConfigurationsManager import ConfigurationsManager
from ..logic.similarity.SimilarityAlgorithmsTypes import SimilarityAlgorithmsTypes
from ..logic.similarity.SimilaritySystemFacade import SimilaritySystemFacade

class GERTController():

    def setLogPath(self, logPath:str) -> Generator:
        yield Message("Validating provided path...", MessageType.CONTINUATION)

        if not os.path.exists(logPath):
            pass

        yield Message("Path is valid!", MessageType.CONTINUATION)
        yield Message("Persisting provided path in {} key...".format("clientLogPath"), MessageType.CONTINUATION)
        configManager = ConfigurationsManager()

        result = configManager.setConfiguration("clientLogPath", logPath)

        if result["updated"] == 0 and result["inserted"] == 0:
            yield Message("The new provided path is identical to the current value. No changes were made.", MessageType.CONTINUATION)
        else:
            if result["updated"] > 0:
                yield Message("The client data logs path was successfully updated!", MessageType.CONTINUATION)

            if result["inserted"] > 0:
                yield Message("The client data logs path was saved in a new configuration key", MessageType.CONTINUATION)

        if result["cached_in_memory"]:
            yield Message("Configuration cached in memory with success", MessageType.END)
        else:
            yield Message("Configuration could not be cached in memory", MessageType.END)

    def updateModel(self) -> Generator:
        yield Message("Starting model update logic...", MessageType.CONTINUATION)
        similaritySystemFacade = SimilaritySystemFacade()
        similaritySystemFacade.calculateSimilarities()
        yield Message("Model update complete!", MessageType.CONTINUATION)

    def setSimilarityEngine(self, engineName:str) -> Generator:
        yield Message("Checking engine...", MessageType.CONTINUATION)

        # validating the provided engine name
        try:
            SimilarityAlgorithmsTypes(engineName)
            yield Message("Selected engine is valid!", MessageType.CONTINUATION)
        except ValueError:
            yield Message("Invalid engine name provided. Exiting.", MessageType.END)
            return

        configManager = ConfigurationsManager()
        print("setting {}".format(engineName))
        result = configManager.setConfiguration("similarityEngine", engineName)

        if result["updated"] == 0 and result["inserted"] == 0:
            yield Message("The provided engine and the previusly configured are the same. No changes were made.", MessageType.CONTINUATION)
        else:
            if result["updated"] > 0 or result["inserted"] > 0:
                yield Message("Similarity engine successfully configured!", MessageType.CONTINUATION)

        if result["cached_in_memory"]:
            yield Message("Configuration cached in memory with success", MessageType.END)
        else:
            yield Message("Configuration could not be cached in memory", MessageType.END)
