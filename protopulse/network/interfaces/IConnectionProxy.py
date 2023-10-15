from protopulse.network.messages.INetworkMessage import INetworkMessage
from protopulse.utils.ByteArray import ByteArray


class IConnectionProxy:
    def processAndSend(self, param1: INetworkMessage, param2: ByteArray) -> None:
        raise NotImplementedError("This method must be overriden")

    def processAndReceive(self, param1: ByteArray) -> INetworkMessage:
        raise NotImplementedError("This method must be overriden")
