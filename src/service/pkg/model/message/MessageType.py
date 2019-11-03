from enum import Enum

class MessageType(Enum):
    BEGIN = 1
    CONTINUATION = 2
    END = 3
    PROGRESS = 4