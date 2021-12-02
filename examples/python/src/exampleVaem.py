from time import sleep
from driver.VaemDriver import vaemDriver
import logging


if __name__ == "__main__":
    ip = '192.168.0.220'
    port = 502
    slave_id = 0

    try:
        vaem = vaemDriver(ip, port, slave_id, logging)
    except Exception as e:
        print(e)

    vaem.init()
    vaem.selectValve(1)
    vaem.setOpeningTime(1, 500)
    while 1:
        vaem.openValve()
        sleep(0.2)
        status = vaem.readStatus()
        if status["error"] == 1:
            vaem.clearError()
        status = vaem.readStatus()
        print(status)
        vaem.closeValve()
        sleep(1)
