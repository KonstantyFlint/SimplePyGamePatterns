class Event:
    pass


class Observer:

    def on_notify(self, event: Event):
        raise NotImplementedError()


class Observable:

    def __init__(self):
        self._observers = set()

    def notify(self, event: Event):
        for observer in self._observers:
            observer.on_notify(event)

    def add_observer(self, observer: Observer):
        self._observers.add(observer)

    def remove_observer(self, observer: Observer):
        if observer in self._observers:
            self._observers.remove(observer)


class KillEvent:

    def __init__(self, killer, killed):
        self.killer = killer
        self.killed = killed
