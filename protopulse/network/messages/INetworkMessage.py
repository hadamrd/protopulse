from typing import TYPE_CHECKING

from protopulse.network.messages.IQueueableMessage import IQueueableMessage
from protopulse.network.parser.ByteArray import ByteArray

if TYPE_CHECKING:
    from protopulse.network.messages.NetworkMessage import NetworkMessage

class INetworkMessage(IQueueableMessage):
    def pack(self, param1: ByteArray) -> None:
        raise NotImplementedError("This method must be overriden")

    def unpack(self, param1: ByteArray, param2: int) -> "NetworkMessage":
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
