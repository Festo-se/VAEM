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
    def configureValves(self, valveOpeningTimes: dict):
        pass

    @abstractmethod
    def openValve(self):
        pass

    @abstractmethod
    def closeValve(self):
        pass
