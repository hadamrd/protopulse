from protopulse.network.messages.Message import Message


class UnexpectedSocketClosureMessage(Message):
    
    def __init__(self) -> None:
        super().__init__()