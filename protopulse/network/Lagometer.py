from protopulse.logger.Logger import Logger
from protopulse.network.interfaces.ILagometer import ILagometer
from protopulse.network.messages.INetworkMessage import INetworkMessage
from protopulse.utils.BenchmarkTimer import BenchmarkTimer


class Lagometer(ILagometer):
    SHOW_LAG_DELAY: int = 2

    def __init__(self):
        super().__init__()
        self._lagging = False
        self._timer = None

    def ping(self, msg: INetworkMessage = None) -> None:
        self._timer = BenchmarkTimer(self.SHOW_LAG_DELAY, self.onTimerComplete)
        self._timer.start()

    def pong(self, msg: INetworkMessage = None) -> None:
        if self._lagging:
            self.stopLag()
        self.stop()

    def stop(self) -> None:
        self._timer.cancel()

    def onTimerComplete(self) -> None:
        self.stop()
        self.startLag()

    def startLag(self) -> None:
        self._lagging = True
        Logger().debug("Lagometer: lagging as duck :(")

    def stopLag(self) -> None:
        self._lagging = False
        Logger().debug("Lagometer: not lagging :)")
