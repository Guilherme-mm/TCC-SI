from .Operation import Operation
from ...model.message.NetworkMessage import NetworkMessage

class SetLogPathOperation(Operation):

    def execute(self) -> NetworkMessage:
        yield "Consegui"
        yield "a parada"
        yield "funciona!"
