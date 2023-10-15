from time import perf_counter

from protopulse.events.EventsHandler import Event, EventsHandler, Listener
from protopulse.events.KernelEvent import KernelEvent
from protopulse.metaclasses.Singleton import Singleton


class KernelEventsManager(EventsHandler, metaclass=Singleton):
    def __init__(self):
        super().__init__()

    def onFramePush(self, frameName, callback, args=[], originator=None):
        def onEvt(e, frame):
            if str(frame) == frameName:
                callback(*args)

        return self.on(KernelEvent.FramePushed, onEvt, originator=originator)

    def onceFramePushed(self, frameName, callback, args=[], originator=None):
        def onEvt(evt: Event, frame):
            if str(frame) == frameName:
                evt.listener.delete()
                callback(*args)

        return self.on(KernelEvent.FramePushed, onEvt, originator=originator)

    def onceFramePulled(self, frameName, callback, args=[], originator=None):
        def onEvt(e: Event, frame):
            if str(frame) == frameName:
                e.listener.delete()
                callback(*args)

        return self.on(KernelEvent.FramePulled, onEvt, originator=originator)

    def onceMapProcessed(
        self, callback, args=[], mapId=None, timeout=None, ontimeout=None, originator=None
    ) -> "Listener":
        once = mapId is None
        startTime = perf_counter()

        def onEvt(event: Event, processedMapId):
            if mapId is not None:
                if processedMapId == mapId:
                    event.listener.delete()
                    return callback(*args)
                if timeout:
                    remaining = timeout - (perf_counter() - startTime)
                    if remaining > 0:
                        event.listener.armTimer(remaining)
                    else:
                        ontimeout(event.listener)
            else:
                callback(*args)

        return self.on(
            KernelEvent.MapDataProcessed, onEvt, once=once, timeout=timeout, ontimeout=ontimeout, originator=originator
        )

    def send(self, event_id: KernelEvent, *args, **kwargs):
        if event_id == KernelEvent.ClientCrashed:
            self._crashMessage = kwargs.get("message", None)
        super().send(event_id, *args, **kwargs)
