import time
import logging
from unittest import TestCase
from driver.VaemDriver import vaemDriver


# Unit Testing
class TestVaemDriver(TestCase):

    # initialize VAEM and values
    def init(self):
        vaemConfig = {
            'ip': '192.168.0.220',
            'port': 502,
            'modbusSlave': 0,
            'logger': logging
        }
        try:
            self.vm = vaemDriver(**vaemConfig)
        except Exception as e:
            print(e)
        self.vm.init()
        for i in range(1, 9):
            self.vm.deselectValve(i)
        self.vm.selectValve(1)
        self.vm.setOpeningTime(1, 500)
        self.vm.closeValve()
        print(self.vm.readStatus())

    # Tests for selectValve(int valve_id)
    def test_select_valve(self):
        self.init()
        # valve 1 selected
        self.assertEqual(1, self.vm.readValves())
        self.vm.selectValve(1)
        self.assertEqual(1, self.vm.readValves())
        # valve 2 selected
        self.vm.selectValve(2)
        self.assertEqual(3, self.vm.readValves())
        # valve 3 selected
        self.vm.selectValve(3)
        self.assertEqual(7, self.vm.readValves())
        # valve 4 selected
        self.vm.selectValve(4)
        self.assertEqual(15, self.vm.readValves())
        # valve 5 selected
        self.vm.selectValve(5)
        self.assertEqual(31, self.vm.readValves())
        # valve 6 selected
        self.vm.selectValve(6)
        self.assertEqual(63, self.vm.readValves())
        # valve 7 selected
        self.vm.selectValve(7)
        self.assertEqual(127, self.vm.readValves())
        # valve 8 selected
        self.vm.selectValve(8)
        self.assertEqual(255, self.vm.readValves())
        self.vm.disconnect()

    # Tests for selectValve(int valve_id) with the wrong ID
    def test_select_valve_wrong_id(self):
        self.init()
        # Negative ID
        self.assertRaisesRegex(ValueError, "Valve ID must be in range 1-8",
                               self.vm.selectValve, -1)
        # Zero ID
        self.assertRaisesRegex(ValueError, "Valve ID must be in range 1-8",
                               self.vm.selectValve, 0)
        # ID > 8
        self.assertRaisesRegex(ValueError, "Valve ID must be in range 1-8",
                               self.vm.selectValve, 9)
        self.vm.disconnect()

    # Tests for deselectValve(int valve_id)
    def test_deselect_valve(self):
        self.init()
        # Select all valves
        for i in range(1, 9):
            self.vm.selectValve(i)

        # All valves selected
        self.assertEqual(255, self.vm.readValves())
        # Deselect valve 8
        self.vm.deselectValve(8)
        self.assertEqual(127, self.vm.readValves())
        # Deselect valve 7
        self.vm.deselectValve(7)
        self.assertEqual(63, self.vm.readValves())
        # Deselect valve 6
        self.vm.deselectValve(6)
        self.assertEqual(31, self.vm.readValves())
        # Deselect valve 5
        self.vm.deselectValve(5)
        self.assertEqual(15, self.vm.readValves())
        # Deselect valve 4
        self.vm.deselectValve(4)
        self.assertEqual(7, self.vm.readValves())
        # Deselect valve 3
        self.vm.deselectValve(3)
        self.assertEqual(3, self.vm.readValves())
        # Deselect valve 2
        self.vm.deselectValve(2)
        self.assertEqual(1, self.vm.readValves())
        # Deselect valve 1
        self.vm.deselectValve(1)
        self.assertEqual(0, self.vm.readValves())
        self.vm.disconnect()

    # Tests for deselectValve(int valve_id) with wrong ID
    def test_deselect_valve_wrong_id(self):
        self.init()
        # Negative ID
        self.assertRaisesRegex(ValueError, "Valve ID must be in range 1-8",
                               self.vm.deselectValve, -1)
        # Zero ID
        self.assertRaisesRegex(ValueError, "Valve ID must be in range 1-8",
                               self.vm.deselectValve, 0)
        # ID > 8
        self.assertRaisesRegex(ValueError, "Valve ID must be in range 1-8",
                               self.vm.deselectValve, 9)
        self.vm.disconnect()

    # Tests for setOpeningTime(int valve_id, int opening_time)
    def test_set_opening_time(self):
        self.init()
        # valve 1 initially has an opening time of 500 ms
        self.assertEqual(500, self.vm.readOpeningTime(1))
        # valve 1 opening time 500 ms
        self.vm.setOpeningTime(1, 500)
        self.assertEqual(500, self.vm.readOpeningTime(1))
        # valve 1 opening time 1 ms
        self.vm.setOpeningTime(1, 1)
        self.assertEqual(1, self.vm.readOpeningTime(1))
        # valve 1 opening time 2000 ms
        self.vm.setOpeningTime(1, 2000)
        self.assertEqual(2000, self.vm.readOpeningTime(1))
        # valve 8 selected
        self.vm.selectValve(8)
        print(self.vm.readValves())
        # valve 8 opening time 500 ms
        self.vm.setOpeningTime(8, 500)
        self.assertEqual(500, self.vm.readOpeningTime(8))

        self.vm.disconnect()

    # Tests for setOpeningTime(int valve_id, int opening_time) with wrong ID
    def test_set_opening_time_wrong_id(self):
        self.init()
        # Negative ID
        self.assertRaisesRegex(ValueError, "Valve ID must be in range 1-8",
                               self.vm.setOpeningTime, -1, 500)
        # Zero ID
        self.assertRaisesRegex(ValueError, "Valve ID must be in range 1-8",
                               self.vm.setOpeningTime, 0, 500)
        # ID > 8
        self.assertRaisesRegex(ValueError, "Valve ID must be in range 1-8",
                               self.vm.setOpeningTime, 9, 500)
        # ID > 8 amd time > 2000
        self.assertRaisesRegex(ValueError, "Valve ID must be in range 1-8",
                               self.vm.setOpeningTime, 9, 5000)
        self.vm.disconnect()

    # Tests for setOpeningTime(int valve_id, int opening_time) with wrong time
    def test_set_opening_time_wrong_time(self):
        self.init()
        # Negative time
        self.assertRaisesRegex(ValueError, "Opening time must be in range 1-2000",
                               self.vm.setOpeningTime, 1, -1)
        # Zero time
        self.assertRaisesRegex(ValueError, "Opening time must be in range 1-2000",
                               self.vm.setOpeningTime, 1, 0)
        # time > 2000 ms
        self.assertRaisesRegex(ValueError, "Opening time must be in range 1-2000",
                               self.vm.setOpeningTime, 1, 2001)
        self.vm.disconnect()

    # Tests for setOpeningTime(int valve_id, int opening_time) with a non-selected valve
    def test_set_opening_time_wrong_valve(self):
        self.init()
        # Valve 7 not selected
        self.assertRaisesRegex(ValueError, "Valve 7 is not selected",
                               self.vm.setOpeningTime, 7, 300)
        self.vm.disconnect()

    # Tests for openValve()
    def test_open_valve(self):
        self.init()
        # Valves not ready
        self.assertEqual(0, self.vm.readStatus()['Readiness'])
        # Open valves
        self.vm.openValve()
        time.sleep(0.2)
        # Valves ready
        self.assertEqual(1, self.vm.readStatus()['Readiness'])
        self.vm.disconnect()

    # Tests for closeValve()
    def test_close_valve(self):
        self.init()
        # Open valves
        self.vm.openValve()
        time.sleep(0.2)
        # Valves ready
        self.assertEqual(1, self.vm.readStatus()['Readiness'])
        # Close valves
        self.vm.closeValve()
        time.sleep(0.2)
        # valves not ready
        self.assertEqual(0, self.vm.readStatus()['Readiness'])
        self.vm.disconnect()

    # Tests for readStatus()
    def test_read_status(self):
        self.init()

        # Open valve 1
        self.vm.openValve()
        time.sleep(0.2)
        testData = self.vm.readStatus()

        # status
        self.assertEqual(0, testData['status'])
        # error
        self.assertEqual(0, testData['error'])
        # readiness
        self.assertEqual(1, testData['Readiness'])
        # operating mode
        self.assertEqual(0, testData['OperatingMode'])
        # valves 1-8 status (1 = open)
        self.assertEqual(1, testData['Valve1'])
        self.assertEqual(0, testData['Valve2'])
        self.assertEqual(0, testData['Valve3'])
        self.assertEqual(0, testData['Valve4'])
        self.assertEqual(0, testData['Valve5'])
        self.assertEqual(0, testData['Valve6'])
        self.assertEqual(0, testData['Valve7'])
        self.assertEqual(0, testData['Valve8'])
        self.vm.disconnect()
