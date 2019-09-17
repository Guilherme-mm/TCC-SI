class LogEntry():
    def __init__(self, actor:str = "", action:str = "", actionObject:str = "", value:int = 1):
        self.__actor = actor
        self.__action = action
        self.__actionObject = actionObject
        self.__value = value

    def setActor(self, actor:str) -> bool:
        self.__actor = actor
        return True

    def setAction(self, action:str) -> bool:
        self.__action = action
        return True

    def setActionObject(self, actionObject:str) -> bool:
        self.__actionObject = actionObject
        return True

    def setValue(self, value:int) -> bool:
        self.__value = value
        return True

    def getActor(self) -> str:
        return self.__actor

    def getAction(self) -> str:
        return self.__action

    def getActionObject(self) -> str:
        return self.__actionObject

    def getValue(self) -> int:
        return self.__value
