import os.path
from typing import Generator
from ..model.message.Message import Message
from ..model.message.MessageType import MessageType
from ..database.managers.ConfigurationsManager import ConfigurationsManager

class GERTController():

    def setLogPath(self, logPath:str) -> Generator:
        yield Message("Validating provided path...", MessageType.CONTINUATION)

        if not os.path.exists(logPath):
            pass

        yield Message("Path is valid!", MessageType.CONTINUATION)
        yield Message("Persisting provided path in {} key...".format("clientLogPath"), MessageType.CONTINUATION)
        configManager = ConfigurationsManager()

        result = configManager.setConfiguration("clientLogPath", logPath)

        if result["updated_count"] == 0 and result["upserted_count"] == 0:
            yield Message("The new provided path is identical to the current value. No changes were made.", MessageType.END)
        else:
            if result["updated_count"] > 0:
                yield Message("The client data logs path was successfully updated!", MessageType.END)

            if result["upserted_count"] > 0:
                yield Message("The client data logs path was saved in a new configuration key", MessageType.END)
