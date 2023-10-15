from PyNetForge.network.messages.Message import Message


class IIdentifiedMessage(Message):
    def getMessageId() -> int:
        raise NotImplementedError("This method must be overriden")
