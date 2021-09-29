from time import sleep
from driver.VaemDriver import vaemDriver


defValveData1 = {x: {"opening_time": 0} for x in range(1, 9)}
defValveData2 = {1: {"opening_time": 500}}

if __name__ == "__main__":
    vaemConfig = {
        'ip': '192.168.0.214',
        'port': 502,
        'slave_id': 0
    }

    try:
        vaem = vaemDriver(**vaemConfig)
    except Exception as e:
        print(e)

    vaem.init()
    vaem.configureValves(defValveData2)
    while 1:
        vaem.openValve()
        sleep(1)
        status = vaem.readStatus()
        if status["error"] == 1:
            vaem.clearError()
        sleep(1)
        vaem.closeValve()
