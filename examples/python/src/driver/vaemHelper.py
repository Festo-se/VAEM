from enum import IntEnum


valveSettings = {
    'NominalVoltage' : 24000,
    'ResponseTime' : 500,
    'TimeDelay' : 0,
    'PickUpTime' : 125,
    'InrushCurrent' : 300,
    'HitNHold' : 100,
    'HoldingCurrent' : 100
}

vaemValveIndex = {
    1: 0x01,
    2: 0x02,
    3: 0x04,
    4: 0x08,
    5: 0x10,
    6: 0x20,
    7: 0x40,
    8: 0x80,
    "AllValves" : 255
}

class VaemAccess(IntEnum):
    Read = 0
    Write = 1

class VaemDataType(IntEnum):
    UINT8 = 1
    UINT16 = 2
    UINT32 = 3
    UINT64 = 4

class VaemIndex(IntEnum):
    ControlWord = 0x01
    StatusWord = 0x02
    NominalVoltage = 0x04
    InrushCurrent = 0x05
    HoldingCurrent = 0x06
    ResponseTime = 0x07
    PickUpTime = 0x08
    OperatingMode = 0x09
    SaveParameters = 0x11
    SelectValve = 0x13
    TimeDelay = 0x16
    HitNHold = 0x2E

"""
class VaemValveIndex(IntEnum):
    Valve1 = 0x01
    Valve2 = 0x02
    Valve3 = 0x04
    Valve4 = 0x08
    Valve5 = 0x10
    Valve6 = 0x20
    Valve7 = 0x40
    Valve8 = 0x80
    AllValves = 255
"""

class VaemControlWords(IntEnum):
    StartValves = 0x01
    StopValves = 0x04
    ResetErrors = 0x08

class VaemOperatingMode(IntEnum):
    OpMode1 = 0x00
    OpMode2 = 0x01
    OpMode3 = 0x02

def get_status(statusWord):
    status = {}
    status['Status'] = statusWord & 0x01
    status['Error'] = (statusWord & 0x08) >> 3
    status['Readiness'] = (statusWord & 0x10) >> 4
    status['OperatingMode'] = (statusWord & 0xC0) >> 6
    status['Valve1'] = (statusWord & 0x100) >> 8
    status['Valve2'] = (statusWord & 0x200) >> 9
    status['Valve3'] = (statusWord & 0x400) >> 10
    status['Valve4'] = (statusWord & 0x800) >> 11
    status['Valve5'] = (statusWord & 0x1000) >> 12
    status['Valve6'] = (statusWord & 0x2000) >> 13
    status['Valve7'] = (statusWord & 0x4000) >> 14
    status['Valve8'] = (statusWord & 0x8000) >> 15
    return status

def get_transfer_value(param, valve, opperation, **settings):
    out = {}
    if param == VaemIndex.NominalVoltage:
        out['access'] = opperation
        out['dataType'] = VaemDataType.UINT16.value
        out['paramIndex'] = VaemIndex.NominalVoltage.value
        out['paramSubIndex'] = valve
        out['errorRet'] = 0
        out['transferValue'] = settings['NominalVoltage']
    elif param == VaemIndex.ResponseTime:
        out['access'] = opperation
        out['dataType'] = VaemDataType.UINT32.value
        out['paramIndex'] = VaemIndex.ResponseTime.value
        out['paramSubIndex'] = valve
        out['errorRet'] = 0
        out['transferValue'] = settings['ResponseTime']        
    elif param == VaemIndex.InrushCurrent:
        out['access'] = opperation
        out['dataType'] = VaemDataType.UINT32.value
        out['paramIndex'] = VaemIndex.InrushCurrent.value
        out['paramSubIndex'] = valve
        out['errorRet'] = 0
        out['transferValue'] = settings['InrushCurrent'] 
    elif param == VaemIndex.HoldingCurrent:
        out['access'] = opperation
        out['dataType'] = VaemDataType.UINT16.value
        out['paramIndex'] = VaemIndex.HoldingCurrent.value
        out['paramSubIndex'] = valve
        out['errorRet'] = 0
        out['transferValue'] = settings['HoldingCurrent']         
    elif param == VaemIndex.PickUpTime:
        out['access'] = opperation
        out['dataType'] = VaemDataType.UINT16.value
        out['paramIndex'] = VaemIndex.PickUpTime.value
        out['paramSubIndex'] = valve
        out['errorRet'] = 0
        out['transferValue'] = settings['PickUpTime']  
    elif param == VaemIndex.TimeDelay:
        out['access'] = opperation
        out['dataType'] = VaemDataType.UINT32.value
        out['paramIndex'] = VaemIndex.TimeDelay.value
        out['paramSubIndex'] = valve
        out['errorRet'] = 0
        out['transferValue'] = settings['TimeDelay']          
    elif param == VaemIndex.HitNHold:
        out['access'] = opperation
        out['dataType'] = VaemDataType.UINT32.value
        out['paramIndex'] = VaemIndex.HitNHold.value
        out['paramSubIndex'] = valve
        out['errorRet'] = 0
        out['transferValue'] = settings['HitNHold']  
    elif param == VaemIndex.SelectValve:
        out['access'] = opperation
        out['dataType'] = VaemDataType.UINT8.value
        out['paramIndex'] = VaemIndex.SelectValve.value
        out['paramSubIndex'] = 0
        out['errorRet'] = 0
        out['transferValue'] = valve
    else:
        print('Invalid input param')
    return out
