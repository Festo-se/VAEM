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


def constructFrame(data):
    frame = []
    tmp = struct.pack('>BBHBBQ', data['access'], data['dataType'], data['paramIndex'], data['paramSubIndex'],
                      data['errorRet'], data['transferValue'])
    for i in range(0, len(tmp) - 1, 2):
        frame.append((tmp[i] << 8) + tmp[i + 1])
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
            data['transferValue'] += (frame[len(frame) - 1 - i] << (i * 16))

    return data


class vaemDriver(pvControl):
    def __init__(self, **config):
        self.config = config

        for attempt in range(3):
            try:
                self.client = TcpClient(host=self.config['ip'], port=self.config['port'])
                self.client.connect()
                break
            except Exception as e:
                print(f'Could not connect to VAEM: {e}, attempt {attempt}')

    def init(self):
        data = {}
        frame = []
        resp = []
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
                                                   unit=self.config['slave_id'])
            # this is uncertain
            print(data.registers)
            return data.registers
        except Exception as e:
            print(f'Something went wrong with read operation VAEM : {e}')

    def configureValves(self, valveOpeningTimes: dict):
        data = {}
        selValves = 0
        try:
            for k, v in valveOpeningTimes.items():
                if v["opening_time"] != 0:
                    selValves = selValves | vaemValveIndex[k]
                data = getValveSetting(VaemIndex.ResponseTime, vaemValveIndex[k],
                                       **{"ResponseTime": v["opening_time"]})
                frame = constructFrame(data)
                self.transfer(frame)

            data = getValveSetting(VaemIndex.SelectValve, selValves)
            frame = constructFrame(data)
            self.transfer(frame)
        except Exception as e:
            raise ValueError(f"Wrong values provided: {e}")

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
        print(getStatus(tmp['transferValue']))

        return getStatus(tmp['transferValue'])

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
