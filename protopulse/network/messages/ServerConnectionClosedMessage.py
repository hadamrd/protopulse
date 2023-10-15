from protopulse.network.messages.Message import Message
from protopulse.network.ServerConnection import ServerConnection


class ServerConnectionClosedMessage(Message):

    _closedConnection: ServerConnection

    def __init__(self, closedConnection: str):
        super().__init__()
        self._closedConnection = closedConnection

    @property
    def closedConnection(self) -> str:
        return self._closedConnection
