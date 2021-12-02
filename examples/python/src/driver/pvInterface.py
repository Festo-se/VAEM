__author__ = "Kolev, Milen"
__copyright__ = "Copyright 2021, Festo Life Tech"
__credits__ = [""]
__license__ = "Apache"
__version__ = "0.0.1"
__maintainer__ = "Kolev, Milen"
__email__ = "milen.kolev@festo.com"
__status__ = "Development"

from abc import ABC, abstractmethod


class pvControl(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def saveSettings(self):
        pass

    @abstractmethod
    def readStatus(self):
        pass

    @abstractmethod
    def selectValve(self, valve_id: int):
        pass

    @abstractmethod
    def deselectValve(self, valve_id: int):
        pass

    @abstractmethod
    def setOpeningTime(self, valve_id: int, opening_time: int):
        pass

    @abstractmethod
    def openValve(self):
        pass

    @abstractmethod
    def closeValve(self):
        pass

    @abstractmethod
    def clearError(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass
