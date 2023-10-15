from protopulse.network.messages.Message import Message


class IFrame:
    def process(self, msg: Message) -> bool:
        raise NotImplementedError("This method must be overriden")

    def pushed(self) -> bool:
        raise NotImplementedError("This method must be overriden")

    def pulled(self) -> bool:
        raise NotImplementedError("This method must be overriden")

    def __str__(self):
        return self.__class__.__name__

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __lt__(self, other: "IFrame") -> bool:
        return self.priority.value > other.priority.value
