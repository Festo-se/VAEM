from time import sleep
import logging
import asyncio

from driver.VaemDriver import vaemDriver
from driver.dataTypes import VaemConfig


if __name__ == "__main__":
    vaemConfig = VaemConfig('192.168.8.118', 502, 0)

    try:
        vaem = vaemDriver(vaemConfig, logger=logging)
    except Exception as e:
        print(e)
    async def func():
        vaem.init()
        print(vaem.read_status())
        await vaem.select_valve(3)
        print(vaem.read_status())
        await vaem.deselect_valve(3)
        print(vaem.read_status())
        await vaem.select_valve(7)
        print(vaem.read_status())
        await vaem.deselect_valve(7)
        print(vaem.read_status())

    loop = asyncio.get_event_loop()
    loop.run_until_complete(func())
