__author__ = "Kolev, Milen"
__copyright__ = "Copyright 2021, Festo Life Tech"
__credits__ = [""]
__license__ = "Apache"
__version__ = "0.0.1"
__maintainer__ = "Kolev, Milen"
__email__ = "milen.kolev@festo.com"
__status__ = "Development"
import logging
from pymodbus.client.sync import ModbusTcpClient as TcpClient
import struct
from time import sleep

from config.data_types import Vaem
from drivers.pvGen.drvVaem.pvInterface import pvControl
from drivers.pvGen.drvVaem.vaemHelper import *

readParam = {
    'address' : 0,
    'length' : 0x07,
}

writeParam = {
    'address' : 0,
    'length' : 0x07,
}

def constructFrame(data):
    frame = []
    tmp = struct.pack('>BBHBBQ', data['access'], data['dataType'], data['paramIndex'], data['paramSubIndex'], data['errorRet'], data['transferValue'])
    for i in range(0, len(tmp)-1, 2):
    	frame.append((tmp[i] << 8) + tmp[i+1])
    return frame

def deconstructFrame(frame):
    data = {}
    if frame is not None:
        data['access'] = (frame[0] & 0xff00) >> 8
        data['dataType'] = frame[0] & 0x00ff
        data['paramIndex'] = frame[1]
        data['paramSubIndex'] = (frame[2] & 0xff00) >> 8
        data['errorRet'] = frame[2] & 0x00ff
        data['transferValue'] = 0
        for i in range(4):
             data['transferValue'] += (frame[len(frame)-1-i] << (i*16))

    return data


class vaemDriver(pvControl):
    def __init__(self, vaemConfig: Vaem, logger: logging):
        self._config = vaemConfig
        self._log = logger
        
        self.client = TcpClient(host=self._config.ip, port=self._config.port)

        for _ in range(5):

            if self.client.connect():
                break
            else:
                self._log.warn(f'Failed to connect VAEM. Reconnecting attempt: {_}')
            if _ == 4:
                self._log.error(f'Could not connect to VAEM: {self._config}')
                raise ConnectionError(f'Could not connect to VAEM: {self._config}')

        self._log.info(f'Connected to VAEM : {self._config}')

    def init(self):
        data = {}
        frame = []
        #set operating mode
        data['access'] = VaemAccess.Write.value
        data['dataType'] = VaemDataType.UINT8.value
        data['paramIndex'] = VaemIndex.OperatingMode.value
        data['paramSubIndex'] = 0
        data['errorRet'] = 0
        data['transferValue'] = VaemOperatingMode.OpMode1.value
        frame = constructFrame(data)
        self.transfer(frame)

        #clear errors
        data['access'] = VaemAccess.Write.value
        data['dataType'] = VaemDataType.UINT16.value
        data['paramIndex'] = VaemIndex.ControlWord.value
        data['transferValue'] = VaemControlWords.ResetErrors.value
        frame = constructFrame(data)
        self.transfer(frame)


    def configureVaem(self):
        """
        Configure all the parameters for all valves with some default values
        """
        data = {}
        frame = []
        paramIndex = [0x04, 0x05, 0x06, 0x07, 0x08, 0x16, 0x2e]

        try:
            for i in VaemIndex:
                if i.value in paramIndex:
                    for v in vaemValveIndex.values():
                        data = getValveSetting(i, v)
                        frame = constructFrame(data)
                        self.transfer(frame)
        except Exception as e:
            print(f'Unable to configure {data}: {e}')

        self.saveSettings()


    def saveSettings(self):
        data = {}
        frame = []
        #save settings
        data['access'] = VaemAccess.Write.value
        data['dataType'] = VaemDataType.UINT32.value
        data['paramIndex'] = VaemIndex.SaveParameters.value
        data['paramSubIndex'] = 0
        data['errorRet'] = 0
        data['transferValue'] = 99999
        frame = constructFrame(data)
        self.transfer(frame)

    #read write oppeartion is constant and custom modbus is implemented on top
    def transfer(self, writeData):
        data = 0
        try:
            data = self.client.readwrite_registers(read_address=readParam['address'],read_count=readParam['length'],write_address=writeParam['address'], write_registers=writeData, unit=self._config.slave_id)
            return data.registers
        except Exception as e:
            self._log.error(f'Something went wrong with read opperation VAEM : {e}')

    async def configureValves(self, valve_id: int, openning_time: int):
        """Configure the valves with pre selected parameters"""
        data = {}
        try:
            if (openning_time in range(0, 2000)) and (valve_id in range(0, 8)):

                data = getValveSetting(VaemIndex.ResponseTime, valve_id, **{"ResponseTime" : openning_time})
                frame = constructFrame(data)
                self.transfer(frame)
                print('configured')
                data = getValveSetting(VaemIndex.SelectValve, vaemValveIndex[valve_id], **{})
                frame = constructFrame(data)
                self.transfer(frame)
                print('end')
            else:
                self._log.error(f'openning time must be in range 0-2000 and valve_id -> 0-8')
                raise ValueError
        except Exception as e:
            self._log.error(f"Wrong values provided {e}")
            raise ValueError

    async def openValve(self):
        """
        Start all valves that are selected
        """
        data = {}
        #save settings
        data['access'] = VaemAccess.Write.value
        data['dataType'] = VaemDataType.UINT16.value
        data['paramIndex'] = VaemIndex.ControlWord.value
        data['paramSubIndex'] = 0
        data['errorRet'] = 0
        data['transferValue'] = VaemControlWords.StartValves.value
        frame = constructFrame(data)        
        self.transfer(frame)

        #reset the control word
        data['access'] = VaemAccess.Write.value
        data['dataType'] = VaemDataType.UINT16.value
        data['paramIndex'] = VaemIndex.ControlWord.value
        data['paramSubIndex'] = 0
        data['errorRet'] = 0
        data['transferValue'] = 0
        frame = constructFrame(data)        
        self.transfer(frame)



    def closeValve(self):
        data = {}
        #save settings
        data['access'] = VaemAccess.Write.value
        data['dataType'] = VaemDataType.UINT16.value
        data['paramIndex'] = VaemIndex.ControlWord.value
        data['paramSubIndex'] = 0
        data['errorRet'] = 0
        data['transferValue'] = VaemControlWords.StopValves.value

        frame = constructFrame(data)
        self.transfer(frame)

    def readStatus(self):
        """
        Read the status of the VAEM
        The status is return as a dictionary with the following keys:
        -> status: 1 if more than 1 valve is active
        -> error: 1 if error in valves is present
        """
        data = {}
        #save settings
        data['access'] = VaemAccess.Read.value
        data['dataType'] = VaemDataType.UINT16.value
        data['paramIndex'] = VaemIndex.StatusWord.value
        data['paramSubIndex'] = 0
        data['errorRet'] = 0
        data['transferValue'] = 0

        frame = constructFrame(data)
        resp = self.transfer(frame)
        tmp = deconstructFrame(resp)
        self._log.info(getStatus(tmp['transferValue']))

        return getStatus(tmp['transferValue'])

    async def clearError(self):
        """
        If any error occurs in valve opening, must be cleared with this opperation.
        """
        data  = {}
        data['access'] = VaemAccess.Write.value
        data['dataType'] = VaemDataType.UINT16.value
        data['paramIndex'] = VaemIndex.ControlWord.value
        data['paramSubIndex'] = 0
        data['errorRet'] = 0
        data['transferValue'] = VaemControlWords.ResetErrors.value
        frame = constructFrame(data)
        self.transfer(frame)