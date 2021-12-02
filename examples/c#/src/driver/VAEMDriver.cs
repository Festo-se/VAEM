using System;
using EasyModbus;

namespace VaemCSharpDriver.driver
{
    // VAEM (8-valve controller) class
    public class VaemDriver
    {
        bool DEBUG_ENABLED = true;

        private ModbusClient client;
        private int[] VaemValveIndex= {0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 255};

        public enum VaemSettings : int
        {
            NOMINAL_VOLTAGE = 24000,
            RESPONSE_TIME = 500,
            TIME_DELAY = 0,
            PICKUP_TIME = 125,
            INRUSH_CURRENT = 500,
            HIT_N_HOLD = 100,
            HOLDING_CURRENT = 100
        }

        // VAEM constructor
        public VaemDriver(string ip, int port)
        {
            this.client = new ModbusClient();

            this.client.IPAddress = ip;
            this.client.Port = port;
            this.client.UnitIdentifier = 0;
            this.client.ConnectionTimeout = 1000;

            for (int i = 0; i < 3; i++)
            {
                if (client.Connected)
                    break;
                try
                {
                    this.client.Connect();
                }
                catch (EasyModbus.Exceptions.ConnectionException e)
                {
                    Console.WriteLine("Could not connect to VAEM: " + e + ", attempt {" + (i + 1) + "}");
                }
            }

            if (!client.Connected)
            {
                throw new Exception("Couldn't create a modbus connection");
            }

            Init();
        }

        // Deconstructor
        ~VaemDriver()
        {
            client.Disconnect();
        }

        // Initialize the VAEM
        private void Init()
        {
            // set operating mode
            ReadWrite((int) VAEMConstants.VaemAccess.WRITE,
                (int) VAEMConstants.VaemDataType.UINT8,
                (int) VAEMConstants.VaemIndex.OPERATING_MODE,
                0,
                (int) VAEMConstants.VaemOperatingMode.MODE1);

            ClearError();
        }
        
        // Disconnect from the VAEM
        public void Disconnect()
        {
            this.client.Disconnect();
        }

        // Construct a modbus frame and send it to the device
        private int[] ReadWrite(int access, int dataType, int index, int subindex, int transferVal)
        {
            int[] writeData = new int[7];
            writeData[0] = (access << 8) + dataType;
            writeData[1] = index;
            writeData[2] = subindex;
            writeData[3] = 0;
            writeData[4] = 0;
            writeData[5] = (transferVal >> 16) & 0xFFFF;
            writeData[6] = transferVal & 0xFFFF;
            return this.client.ReadWriteMultipleRegisters(0, 0x07, 0, writeData);
        }

        // Save the current device settings to memory
        public void SaveSettings()
        {
            string s = string.Join(", ", ReadWrite(
                (int) VAEMConstants.VaemAccess.WRITE,
                (int) VAEMConstants.VaemDataType.UINT32,
                (int) VAEMConstants.VaemIndex.SAVE_PARAMETERS,
                0,
                99999));

            if (DEBUG_ENABLED)
                Console.WriteLine("SaveSettings(): " + s);
        }

        // Select the given valve
        public void SelectValve(int valveId)
        {
            if (valveId < 1 || valveId > 8) {
                throw new ArgumentException("Valve ID must be in range 1-8");
            }
            int selValves = ReadValves();
            selValves = selValves | VaemValveIndex[valveId-1];
            ReadWrite((int) VAEMConstants.VaemAccess.WRITE, 
                (int) VAEMConstants.VaemDataType.UINT8, 
                (int) VAEMConstants.VaemIndex.SELECT_VALVE, 
                0, 
                selValves);
        }

        // Deselect the given valve
        public void DeselectValve(int valveId)
        {
            if (valveId < 1 || valveId > 8) {
                throw new ArgumentException("Valve ID must be in range 1-8");
            }
            int selValves = ReadValves();
            if ((selValves & VaemValveIndex[valveId-1]) > 0) {
                selValves = selValves - VaemValveIndex[valveId-1];
                ReadWrite((int) VAEMConstants.VaemAccess.WRITE,
                    (int) VAEMConstants.VaemDataType.UINT8, 
                    (int) VAEMConstants.VaemIndex.SELECT_VALVE, 
                    0, 
                    selValves);
            }
        }

        // Set the opening time of the given valve
        public void SetOpeningTime(int valveId, int openingTime)
        {
            if (valveId < 1 || valveId > 8) {
                throw new ArgumentException("Valve ID must be in range 1-8");
            }
            if (openingTime < 1 || openingTime > 2000) {
                throw new ArgumentException("Opening time must be in range 1-2000");
            }
            if ((ReadValves() & VaemValveIndex[valveId-1]) == 0) {
                throw new ArgumentException("Valve " + valveId + " is not selected");
            }
            ReadWrite((int) VAEMConstants.VaemAccess.WRITE,
                (int) VAEMConstants.VaemDataType.UINT32, 
                (int) VAEMConstants.VaemIndex.RESPONSE_TIME, 
                valveId-1, 
                openingTime);
        }

        // Open all selected valves
        public void OpenValve()
        {
            string s = string.Join(", ", ReadWrite(
                (int) VAEMConstants.VaemAccess.WRITE,
                (int) VAEMConstants.VaemDataType.UINT16,
                (int) VAEMConstants.VaemIndex.CONTROL_WORD,
                0,
                (int) VAEMConstants.VaemControlWord.START_VALVES));

            string t = string.Join(", ", ReadWrite(
                (int) VAEMConstants.VaemAccess.WRITE,
                (int) VAEMConstants.VaemDataType.UINT16,
                (int) VAEMConstants.VaemIndex.CONTROL_WORD,
                0, 0));

            if (DEBUG_ENABLED)
            {
                Console.WriteLine("OpenValve(): " + s);
                Console.WriteLine("OpenValve(): " + t);
            }
        }

        // Close all selected valves
        public void CloseValve()
        {
            string s = string.Join(", ", ReadWrite(
                (int) VAEMConstants.VaemAccess.WRITE,
                (int) VAEMConstants.VaemDataType.UINT16,
                (int) VAEMConstants.VaemIndex.CONTROL_WORD,
                0,
                (int) VAEMConstants.VaemControlWord.STOP_VALVES));

            if (DEBUG_ENABLED)
                Console.WriteLine("CloseValve(): " + s);
        }

        // Read the status of the VAEM
        public int[] ReadStatus()
        {
            int[] ret = ReadWrite(
                (int) VAEMConstants.VaemAccess.READ,
                (int) VAEMConstants.VaemDataType.UINT16,
                (int) VAEMConstants.VaemIndex.STATUS_WORD,
                0,
                0);

            string s = string.Join(", ", ret);

            Console.WriteLine("ReadStatus(): " + s);

            return ret;
        }

        // Clear the error bit
        public void ClearError()
        {
            string s = string.Join(", ", ReadWrite(
                (int) VAEMConstants.VaemAccess.WRITE,
                (int) VAEMConstants.VaemDataType.UINT16,
                (int) VAEMConstants.VaemIndex.CONTROL_WORD,
                0,
                (int) VAEMConstants.VaemControlWord.RESET_ERRORS));

            if (DEBUG_ENABLED)
                Console.WriteLine("ClearError(): " + s);
        }

        // Read which valves are currently selected
        public int ReadValves()
        {
            return ReadWrite(
                (int) VAEMConstants.VaemAccess.READ,
                (int) VAEMConstants.VaemDataType.UINT8,
                (int) VAEMConstants.VaemIndex.SELECT_VALVE,
                0,
                0)[6];
        }

        // Read the opening time of a valve by ID
        public int ReadOpeningTime(int valveId)
        {
            return ReadWrite(
                (int) VAEMConstants.VaemAccess.READ,
                (int) VAEMConstants.VaemDataType.UINT32,
                (int) VAEMConstants.VaemIndex.RESPONSE_TIME,
                valveId - 1,
                0)[6];
        }

        // Return the formatted status word
        public int[] GetStatus(int statusWord)
        {
            int[] status = new int[12];
            status[0] = statusWord & 0x01;
            status[1] = (statusWord & 0x08) >> 3;
            status[2] = (statusWord & 0x10) >> 4;
            status[3] = (statusWord & 0xC0) >> 6;

            Console.WriteLine("Status: " + (statusWord & 0x01));
            Console.WriteLine("Error: " + ((statusWord & 0x08) >> 3));
            Console.WriteLine("Readiness: " + ((statusWord & 0x10) >> 4));
            Console.WriteLine("Operating Mode: " + ((statusWord & 0xC0) >> 6));

            status[4] = (statusWord & 0x100) >> 8;
            status[5] = (statusWord & 0x200) >> 9;
            status[6] = (statusWord & 0x400) >> 10;
            status[7] = (statusWord & 0x800) >> 11;
            status[8] = (statusWord & 0x1000) >> 12;
            status[9] = (statusWord & 0x2000) >> 13;
            status[10] = (statusWord & 0x4000) >> 14;
            status[11] = (statusWord & 0x8000) >> 15;

            Console.WriteLine("Valve 1: " + ((statusWord & 0x100) >> 8));
            Console.WriteLine("Valve 2: " + ((statusWord & 0x200) >> 9));
            Console.WriteLine("Valve 3: " + ((statusWord & 0x400) >> 10));
            Console.WriteLine("Valve 4: " + ((statusWord & 0x800) >> 11));
            Console.WriteLine("Valve 5: " + ((statusWord & 0x1000) >> 12));
            Console.WriteLine("Valve 6: " + ((statusWord & 0x2000) >> 13));
            Console.WriteLine("Valve 7: " + ((statusWord & 0x4000) >> 14));
            Console.WriteLine("Valve 8: " + ((statusWord & 0x8000) >> 15));

            return status;
        }
    }
}