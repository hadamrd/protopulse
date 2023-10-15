import importlib

from PyNetForge.metaclasses.Singleton import Singleton
from PyNetForge.network.messages.NetworkMessage import NetworkMessage
from PyNetForge.network.parser.ProtocolSpec import ProtocolSpec
from PyNetForge.utils.ByteArray import ByteArray


class UnknownMessageId(Exception):
    pass


class MessageParser(metaclass=Singleton):

    def __init__(self, optimise=True):
        self.infight = False
        self.discard = optimise
        self.msgLenLen = None
        self.msgLen = None
        self.msgId = None
        self.msgCount = None
        super().__init__()

    def getMessageClass(self, modulePath, clsName) -> type[NetworkMessage]:
        try:
            clsModule = globals()[modulePath]
        except:
            clsModule = importlib.import_module(modulePath)
        return getattr(clsModule, clsName)
        
    def parseMessage(self, input: ByteArray, messageId: int, messageLength: int, from_client=False, msgCount=None) -> NetworkMessage:
        try:
            clsSpec = ProtocolSpec.getClassSpecById(messageId)
        except:
            raise UnknownMessageId(f"Message {messageId}, from client {from_client} : not found in known message Ids!")
        messageType = clsSpec.cls
        message = messageType.unpack(input, messageLength)
        message.unpacked = True
        if from_client:
            message._instance_id = msgCount
        return message

    def parse(self, buffer: ByteArray, callback, from_client=False) -> None:
        while buffer.remaining():
            if self.msgLenLen is None:
                if buffer.remaining() < 2:
                    break
                staticHeader = buffer.readUnsignedShort()
                self.msgId = staticHeader >> NetworkMessage.PACKET_ID_RIGHT_SHIFT
                self.msgLenLen = staticHeader & NetworkMessage.BIT_MASK
            if from_client and self.msgCount is None:
                if buffer.remaining() < 4:
                    break
                self.msgCount = buffer.readUnsignedInt()
            if self.msgLen is None:
                if buffer.remaining() < self.msgLenLen:
                    break
                self.msgLen = int.from_bytes(buffer.read(self.msgLenLen), "big")
            if buffer.remaining() < self.msgLen:
                break
            msg_bytes = buffer.read(self.msgLen)            
            msg = self.parseMessage(msg_bytes, self.msgId, self.msgLen, from_client, self.msgCount)
            self.msgId = None
            self.msgLenLen = None
            self.msgLen = None
            self.msgCount = None
            callback(msg, from_client)
        buffer.trim()