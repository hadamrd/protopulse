from PyNetForge.utils.ByteArray import ByteArray
from PyNetForge.network.messages.INetworkMessage import INetworkMessage


class IConnectionProxy:
    def processAndSend(self, param1: INetworkMessage, param2: ByteArray) -> None:
        raise NotImplementedError("This method must be overriden")

    def processAndReceive(self, param1: ByteArray) -> INetworkMessage:
        raise NotImplementedError("This method must be overriden")
