from PyNetForge.network.interfaces.IIdentifiedMessage import IdentifiedMessage
from PyNetForge.network.messages.IQueueableMessage import IQueueableMessage
from PyNetForge.utils.ByteArray import ByteArray


class INetworkMessage(IdentifiedMessage, IQueueableMessage):
    def pack(self, param1: ByteArray) -> None:
        raise NotImplementedError("This method must be overriden")

    def unpack(self, param1: ByteArray, param2: int) -> None:
        raise NotImplementedError("This method must be overriden")

    @property
    def isInitialized(self) -> bool:
        raise NotImplementedError("This method must be overriden")

    @property
    def unpacked(self) -> bool:
        raise NotImplementedError("This method must be overriden")

    @unpacked.setter
    def unpacked(self, param1: bool) -> None:
        raise NotImplementedError("This method must be overriden")
