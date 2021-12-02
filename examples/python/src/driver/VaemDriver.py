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
from driver.pvInterface import pvControl
from driver.vaemHelper import *

readParam = {
    'address': 0,
    'length': 0x07,
}

writeParam = {
    'address': 0,
    'length': 0x07,
}


# Construct the frame (message) to be sent to the VAEM
def constructFrame(data):
    frame = []
    tmp = struct.pack('>BBHBBQ', data['access'], data['dataType'], data['paramIndex'], data['paramSubIndex'],
                      data['errorRet'], data['transferValue'])
    for i in range(0, len(tmp) - 1, 2):
        frame.append((tmp[i] << 8) + tmp[i + 1])
    return frame


# Deconstruct the frame (message) received from the VAEM into info
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
            data['transferValue'] += (frame[len(frame) - 1 - i] << (i * 16))

    return data


# VAEM (8-valve controller) class
class vaemDriver(pvControl):
    def __init__(self, ip: str, port: int, modbusSlave: int, logger: logging):
        self.ip = ip
        self.port = port
        self.slave_id = modbusSlave
        self._log = logger

        # initialize client
        self.client = TcpClient(host=self.ip, port=self.port)

        # attempt to connect five times
        for _ in range(5):
            if self.client.connect():
                # connected
                break
            else:
                # attempt to connect again
                self._log.warning(f'Failed to connect VAEM. Reconnecting attempt: {_}')
            if _ == 4:
                # failed to connect
                self._log.error(f'Could not connect to VAEM: {self.ip}')
                raise ConnectionError(f'Could not connect to VAEM: {self.ip}')

        self._log.info(f'Connected to VAEM : {self.ip}')

    # initialize the VAEM
    def init(self):
        data = {}
        frame = []
        # set operating mode
        data['access'] = VaemAccess.Write.value
        data['dataType'] = VaemDataType.UINT8.value
        data['paramIndex'] = VaemIndex.OperatingMode.value
        data['paramSubIndex'] = 0
        data['errorRet'] = 0
        data['transferValue'] = VaemOperatingMode.OpMode1.value
        frame = constructFrame(data)
        self.transfer(frame)

        # clear errors
        data['access'] = VaemAccess.Write.value
        data['dataType'] = VaemDataType.UINT16.value
        data['paramIndex'] = VaemIndex.ControlWord.value
        data['transferValue'] = VaemControlWords.ResetErrors.value
        frame = constructFrame(data)
        self.transfer(frame)

    # disconnect from the VAEM
    def disconnect(self):
        # close connection
        self.client.close()

    # save the VAEM's current settings to memory
    def saveSettings(self):
        data = {}
        frame = []
        # save settings
        data['access'] = VaemAccess.Write.value
        data['dataType'] = VaemDataType.UINT32.value
        data['paramIndex'] = VaemIndex.SaveParameters.value
        data['paramSubIndex'] = 0
        data['errorRet'] = 0
        data['transferValue'] = 99999
        frame = constructFrame(data)
        self.transfer(frame)

    # read write operation is constant and custom modbus is implemented on top
    def transfer(self, writeData):
        data = 0
        try:
            data = self.client.readwrite_registers(read_address=readParam['address'], read_count=readParam['length'],
                                                   write_address=writeParam['address'], write_registers=writeData,
                                                   unit=self.slave_id)
            return data.registers
        except Exception as e:
            self._log.error(f'Something went wrong with read operation VAEM : {e}')

    # select valves by ID
    def selectValve(self, valve_id: int):
        if valve_id not in range(1, 9):
            raise ValueError(f"Valve ID must be in range 1-8")
        selValves = self.readValves()

        selValves = selValves | vaemValveIndex[valve_id]
        data = getValveSetting(VaemIndex.SelectValve, selValves, 0)
        frame = constructFrame(data)
        self.transfer(frame)

    # deselect valves by ID
    def deselectValve(self, valve_id: int):
        if valve_id not in range(1, 9):
            raise ValueError(f"Valve ID must be in range 1-8")
        selValves = self.readValves()

        # check if the valve is currently selected
        if selValves & vaemValveIndex[valve_id] > 0:
            selValves = selValves - vaemValveIndex[valve_id]
            data = getValveSetting(VaemIndex.SelectValve, selValves, 0)
            frame = constructFrame(data)
            self.transfer(frame)

    # set the opening (actuation) time of the valve by ID
    def setOpeningTime(self, valve_id: int, opening_time: int):
        if valve_id not in range(1, 9):
            raise ValueError(f"Valve ID must be in range 1-8")
        if opening_time not in range(1, 2001):
            raise ValueError(f"Opening time must be in range 1-2000")
        if self.readValves() & vaemValveIndex[valve_id] == 0:
            raise ValueError(f"Valve " + str(valve_id) + " is not selected")

        data = getValveSetting(VaemIndex.ResponseTime, valve_id-1, opening_time)
        frame = constructFrame(data)
        self.transfer(frame)

    # open all selected valves
    def openValve(self):
        """
        Start all valves that are selected
        """
        data = {}
        # save settings
        data['access'] = VaemAccess.Write.value
        data['dataType'] = VaemDataType.UINT16.value
        data['paramIndex'] = VaemIndex.ControlWord.value
        data['paramSubIndex'] = 0
        data['errorRet'] = 0
        data['transferValue'] = VaemControlWords.StartValves.value
        frame = constructFrame(data)
        self.transfer(frame)

        # reset the control word
        data['access'] = VaemAccess.Write.value
        data['dataType'] = VaemDataType.UINT16.value
        data['paramIndex'] = VaemIndex.ControlWord.value
        data['paramSubIndex'] = 0
        data['errorRet'] = 0
        data['transferValue'] = 0
        frame = constructFrame(data)
        self.transfer(frame)

    # close all selected valves
    def closeValve(self):
        data = {}
        # save settings
        data['access'] = VaemAccess.Write.value
        data['dataType'] = VaemDataType.UINT16.value
        data['paramIndex'] = VaemIndex.ControlWord.value
        data['paramSubIndex'] = 0
        data['errorRet'] = 0
        data['transferValue'] = VaemControlWords.StopValves.value

        frame = constructFrame(data)
        self.transfer(frame)

    # read the current status word
    def readStatus(self):
        """
        Read the status of the VAEM
        The status is return as a dictionary with the following keys:
        -> status: 1 if more than 1 valve is active
        -> error: 1 if error in valves is present
        """
        data = {}
        # save settings
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

    # read which valves are currently selected
    def readValves(self):
        out = {}
        out['access'] = VaemAccess.Read.value
        out['dataType'] = VaemDataType.UINT8.value
        out['paramIndex'] = VaemIndex.SelectValve.value
        out['paramSubIndex'] = 0
        out['errorRet'] = 0
        out['transferValue'] = 0
        frame = constructFrame(out)
        return self.transfer(frame)[6]

    # read the opening time of a valve by ID
    def readOpeningTime(self, valve_id: int):
        out = {}
        out['access'] = VaemAccess.Read.value
        out['dataType'] = VaemDataType.UINT32.value
        out['paramIndex'] = VaemIndex.ResponseTime.value
        out['paramSubIndex'] = valve_id - 1
        out['errorRet'] = 0
        out['transferValue'] = 0
        frame = constructFrame(out)
        data = self.transfer(frame)
        print(data)
        return data[6]

    # clear the error bit in the VAEM
    def clearError(self):
        """
        If any error occurs in valve opening, must be cleared with this operation.
        """
        data = {}
        data['access'] = VaemAccess.Write.value
        data['dataType'] = VaemDataType.UINT16.value
        data['paramIndex'] = VaemIndex.ControlWord.value
        data['paramSubIndex'] = 0
        data['errorRet'] = 0
        data['transferValue'] = VaemControlWords.ResetErrors.value
        frame = constructFrame(data)
        self.transfer(frame)
