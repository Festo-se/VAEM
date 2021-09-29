from abc import ABC, abstractmethod


class pvControl(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def configureValves(self, valveOpeningTimes: dict):
        pass

    @abstractmethod
    def openValve(self):
        pass

    @abstractmethod
    def closeValve(self):
        pass
