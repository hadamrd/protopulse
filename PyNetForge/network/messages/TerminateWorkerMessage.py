from PyNetForge.network.messages.Message import Message


class TerminateWorkerMessage(Message):
    
    def __init__(self) -> None:
        super().__init__()