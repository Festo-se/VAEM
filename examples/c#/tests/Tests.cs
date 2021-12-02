using System;
using System.Threading;
using NUnit.Framework;
using VaemCSharpDriver.driver;

namespace Tests
{
    [TestFixture]
    public class Tests
    {
        private VaemDriver vm;
        
        private void Init() 
        {
            vm = new VaemDriver("192.168.0.220", 502);
            for (int i = 1; i < 9; i++)
            {
                vm.DeselectValve(i);
            }
            vm.SelectValve(1);
            vm.SetOpeningTime(1, 500);
            vm.CloseValve();
        }
        
        // Tests for SelectValve
        [Test]
        public void TestSelectValve() {
            Init();
            // valve 1 Selected
            Assert.AreEqual(1, vm.ReadValves());
            vm.SelectValve(1);
            Assert.AreEqual(1, vm.ReadValves());
            // valve 2 Selected
            vm.SelectValve(2);
            Assert.AreEqual(3, vm.ReadValves());
            // valve 3 Selected
            vm.SelectValve(3);
            Assert.AreEqual(7, vm.ReadValves());
            // valve 4 Selected
            vm.SelectValve(4);
            Assert.AreEqual(15, vm.ReadValves());
            // valve 5 Selected
            vm.SelectValve(5);
            Assert.AreEqual(31, vm.ReadValves());
            // valve 6 Selected
            vm.SelectValve(6);
            Assert.AreEqual(63, vm.ReadValves());
            // valve 7 Selected
            vm.SelectValve(7);
            Assert.AreEqual(127, vm.ReadValves());
            // valve 8 Selected
            vm.SelectValve(8);
            Assert.AreEqual(255, vm.ReadValves());
            vm.Disconnect();
        }

        // Tests for SelectValve(int valve_id) with the wrong ID
        [Test]
        public void TestSelectValveWrongId() {
            Init();
            var except = Assert.Throws<ArgumentException>(() => vm.SelectValve(-1));
            Assert.AreEqual("Valve ID must be in range 1-8", except.Message);
            
            except = Assert.Throws<ArgumentException>(() => vm.SelectValve(0));
            Assert.AreEqual("Valve ID must be in range 1-8", except.Message);
            
            except = Assert.Throws<ArgumentException>(() => vm.SelectValve(9));
            Assert.AreEqual("Valve ID must be in range 1-8", except.Message);
            vm.Disconnect();
        }

        // Tests for DeselectValve(int valve_id)
        [Test]
        public void TestDeselectValve() {
            Init();
            for (int i = 1; i < 9; i++) {
                vm.SelectValve(i);
            }
            //All valves selected
            Assert.AreEqual(255, vm.ReadValves());
            //Deselect valve 8
            vm.DeselectValve(8);
            Assert.AreEqual(127, vm.ReadValves());
            //Deselect valve 7
            vm.DeselectValve(7);
            Assert.AreEqual(63, vm.ReadValves());
            //Deselect valve 6
            vm.DeselectValve(6);
            Assert.AreEqual(31, vm.ReadValves());
            //Deselect valve 5
            vm.DeselectValve(5);
            Assert.AreEqual(15, vm.ReadValves());
            //Deselect valve 4
            vm.DeselectValve(4);
            Assert.AreEqual(7, vm.ReadValves());
            //Deselect valve 3
            vm.DeselectValve(3);
            Assert.AreEqual(3, vm.ReadValves());
            //Deselect valve 2
            vm.DeselectValve(2);
            Assert.AreEqual(1, vm.ReadValves());
            //Deselect valve 1
            vm.DeselectValve(1);
            Assert.AreEqual(0, vm.ReadValves());
            vm.Disconnect();
        }

        // Tests for DeselectValve(int valve_id) with the wrong ID
        [Test]
        public void TestDeselectValveWrongId() {
            Init();
            var except = Assert.Throws<ArgumentException>(() => vm.DeselectValve(-1));
            Assert.AreEqual("Valve ID must be in range 1-8", except.Message);
            
            except = Assert.Throws<ArgumentException>(() => vm.DeselectValve(0));
            Assert.AreEqual("Valve ID must be in range 1-8", except.Message);
            
            except = Assert.Throws<ArgumentException>(() => vm.DeselectValve(9));
            Assert.AreEqual("Valve ID must be in range 1-8", except.Message);
            vm.Disconnect();
        }
        
        // Tests for SetOpeningTime(int valve_id, int opening_time)
        [Test]
        public void TestSetOpeningTime() {
            Init();
            //valve 1 Initially has an opening time of 500 ms
            Assert.AreEqual(500, vm.ReadOpeningTime(1));
            //valve 1 opening time 500 ms
            vm.SetOpeningTime(1, 500);
            Assert.AreEqual(500, vm.ReadOpeningTime(1));
            //valve 1 opening time 1 ms
            vm.SetOpeningTime(1, 1);
            Assert.AreEqual(1, vm.ReadOpeningTime(1));
            //valve 1 opening time 2000 ms
            vm.SetOpeningTime(1, 2000);
            Assert.AreEqual(2000, vm.ReadOpeningTime(1));
            //valve 8 selected
            vm.SelectValve(8);
            Console.WriteLine(vm.ReadValves());
            //valve 8 opening time 500 ms
            vm.SetOpeningTime(8, 500);
            Assert.AreEqual(500, vm.ReadOpeningTime(8));
            vm.Disconnect();
        }

        // Tests for SetOpeningTime(int valve_id, int opening_time) with the wrong ID
        [Test]
        public void TestSetOpeningTimeWrongId() {
            Init();
            var except = Assert.Throws<ArgumentException>(() => vm.SetOpeningTime(-1, 500));
            Assert.AreEqual("Valve ID must be in range 1-8", except.Message);
            
            except = Assert.Throws<ArgumentException>(() => vm.SetOpeningTime(0, 500));
            Assert.AreEqual("Valve ID must be in range 1-8", except.Message);
            
            except = Assert.Throws<ArgumentException>(() => vm.SetOpeningTime(9, 500));
            Assert.AreEqual("Valve ID must be in range 1-8", except.Message);
            
            except = Assert.Throws<ArgumentException>(() => vm.SetOpeningTime(9, 5000));
            Assert.AreEqual("Valve ID must be in range 1-8", except.Message);
            vm.Disconnect();
        }
        
        // Tests for SetOpeningTime(int valve_id, int opening_time) with wrong time
        [Test]
        public void TestSetOpeningTimeWrongTime() {
            Init();
            var except = Assert.Throws<ArgumentException>(() => vm.SetOpeningTime(1, -1));
            Assert.AreEqual("Opening time must be in range 1-2000", except.Message);
            
            except = Assert.Throws<ArgumentException>(() => vm.SetOpeningTime(1, 0));
            Assert.AreEqual("Opening time must be in range 1-2000", except.Message);
            
            except = Assert.Throws<ArgumentException>(() => vm.SetOpeningTime(1, 2001));
            Assert.AreEqual("Opening time must be in range 1-2000", except.Message);
            vm.Disconnect();
        }

        // Tests for SetOpeningTime(int valve_id, int opening_time) with a non-selected valve
        [Test]
        public void TestSetOpeningTimeWrongValve()  {
            Init();
            var except = Assert.Throws<ArgumentException>(() => vm.SetOpeningTime(7, 500));
            Assert.AreEqual("Valve 7 is not selected", except.Message);
            vm.Disconnect();
        }
        
        // Tests for OpenValve()
        [Test]
        public void TestOpenValve()
        {
            Init();
            vm.OpenValve();
            Thread.Sleep(200);
            Assert.AreEqual(1, (vm.ReadStatus()[6] & 0x10) >> 4);
            vm.CloseValve();
            Assert.AreEqual(0, (vm.ReadStatus()[6] & 0x10) >> 4);
            vm.Disconnect();
        }

        // Tests CloseValve()
        [Test]
        public void TestCloseValve()
        {
            Init();
            vm.OpenValve();
            Thread.Sleep(200);
            Console.WriteLine(vm.ReadStatus());
            Assert.AreEqual(1, (vm.ReadStatus()[6] & 0x10) >> 4);
            vm.CloseValve();
            Console.WriteLine(vm.ReadStatus());
            Assert.AreEqual(0, (vm.ReadStatus()[6] & 0x10) >> 4);
            vm.Disconnect();
        }

        // Tests for ReadStatus()
        [Test]
        public void TestReadStatus() {
            Init();
            int[] valveData = {500, 0, 500, 0, 500, 0, 500, 0};
            vm.OpenValve();
            Thread.Sleep(200);
            int[] testData = vm.GetStatus(vm.ReadStatus()[6]);

            // status
            Assert.AreEqual(0, testData[0]);
            // error
            Assert.AreEqual(0, testData[1]);
            //Readiness
            Assert.AreEqual(1, testData[2]);
            // operating mode
            Assert.AreEqual(0, testData[3]);
            //valves 1-8 status (1 = open)
            Assert.AreEqual(1, testData[4]);
            Assert.AreEqual(0, testData[5]);
            Assert.AreEqual(0, testData[6]);
            Assert.AreEqual(0, testData[7]);
            Assert.AreEqual(0, testData[8]);
            Assert.AreEqual(0, testData[9]);
            Assert.AreEqual(0, testData[10]);
            Assert.AreEqual(0, testData[11]);

            vm.Disconnect();
        }
    }
}