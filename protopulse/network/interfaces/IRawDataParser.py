from types import FunctionType

from protopulse.network.interfaces.INetworkMessage import INetworkMessage
from protopulse.utils.ByteArray import ByteArray


class RawDataParser:
    _messagesTypes = dict()

    def parse(self, data: ByteArray, msgId: int, msgLen: int) -> INetworkMessage:
        raise NotImplementedError()

    def parseAsync(self, data: ByteArray, messageId: int, msgLen: int, compute: FunctionType) -> INetworkMessage:
        raise NotImplementedError()

    def getUnpackMode(self, param1: int) -> int:
        raise NotImplementedError()
