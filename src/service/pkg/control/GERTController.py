from .operation.OperationCode import OperationCode

class GERTController():
    def execute(self, operationCode:int):
        operationCodeObject = OperationCode(operationCode)
        operationObject = operationCodeObject.instantiateOperation()
        generator = operationObject.execute()

        for i in generator:
            yield i
