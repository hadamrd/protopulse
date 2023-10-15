from protopulse.network.interfaces.ILagometer import ILagometer
from protopulse.network.interfaces.IRawDataParser import RawDataParser
from protopulse.network.messages.INetworkMessage import INetworkMessage


class IServerConnection:
    @property
    def rawParser(self) -> RawDataParser:
        raise NotImplementedError()

    @rawParser.setter
    def rawParser(self, param1: RawDataParser) -> None:
        raise NotImplementedError()

    def pauseBuffer(self) -> list:
        raise NotImplementedError()

    @property
    def connected(self) -> bool:
        raise NotImplementedError()

    @property
    def connecting(self) -> bool:
        raise NotImplementedError()

    def latencyAvg(self) -> int:
        raise NotImplementedError()

    def latencySamplesCount(self) -> int:
        raise NotImplementedError()

    def latencySamplesMax(self) -> int:
        raise NotImplementedError()

    @property
    def lagometer(self) -> ILagometer:
        raise NotImplementedError()

    @lagometer.setter
    def lagometer(self, param1: ILagometer) -> None:
        raise NotImplementedError()

    def connect(self, param1: str, param2: int) -> None:
        raise NotImplementedError()

    def close(self) -> None:
        raise NotImplementedError()

    def pause(self) -> None:
        raise NotImplementedError()

    def resume(self) -> None:
        raise NotImplementedError()

    def send(self, param1: INetworkMessage, param2: str = "") -> None:
        raise NotImplementedError()

    def stopConnectionTimeout(self) -> None:
        raise NotImplementedError()

    def checkClosed(self) -> None:
        raise NotImplementedError()
