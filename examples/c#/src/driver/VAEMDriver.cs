using System;
using EasyModbus;

namespace driver
{
    class VaemDriver
    {
        bool DEBUG_ENABLED = true;
        
        private ModbusClient client;
        
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
        
        public VaemDriver(string ip, int port)
        {

            this.client = new ModbusClient();

            this.client.IPAddress = ip;
            this.client.Port = port;
            this.client.UnitIdentifier = 0;
            this.client.ConnectionTimeout = 1000;
            
            for (int i = 0; i < 3; i++) {
                if (client.Connected)
                    break;
                try
                {
                    this.client.Connect();
                } catch (EasyModbus.Exceptions.ConnectionException e) {
                    Console.WriteLine("Could not connect to VAEM: " + e + ", attempt {" + (i+1) + "}");
                }
            }

            if (!client.Connected)
            {
                throw new Exception("Couldn't create a modbus connection");
            }
            
            Init();
        }
        
        ~VaemDriver()
        {
            client.Disconnect();
        }

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

        private int[] ReadWrite(int access, int dataType, int index, int subindex, int transferVal)
        {
            int[] writeData = new int[7];
            writeData[0] = (access << 8) + dataType;
            writeData[1] = index;
            writeData[2] = subindex << 8;
            writeData[3] = 0;
            writeData[4] = 0;
            writeData[5] = (transferVal >> 16) & 0xFFFF;
            writeData[6] = transferVal & 0xFFFF;
            return this.client.ReadWriteMultipleRegisters(0, 0x07, 0, writeData);
        }

        public void ConfigureVaem()
        {
            string s;
            
            s = string.Join(", ", ReadWrite(
                (int) VAEMConstants.VaemAccess.WRITE,
                (int) VAEMConstants.VaemDataType.UINT8,
                (int) VAEMConstants.VaemIndex.SELECT_VALVE,
                0, 
                (int) VAEMConstants.VaemValveIndex.ALL_VALVES));
            
            if (DEBUG_ENABLED)
                Console.WriteLine("ConfigureVaem(): " + s);
            
            for (int valve = 0; valve < 8; valve++)
            {
                s = string.Join(", ", ReadWrite(
                    (int) VAEMConstants.VaemAccess.WRITE,
                    (int) VAEMConstants.VaemDataType.UINT16,
                    (int) VAEMConstants.VaemIndex.NOMINAL_VOLTAGE,
                    valve,
                    (int) VaemSettings.NOMINAL_VOLTAGE));
                
                if (DEBUG_ENABLED)
                    Console.WriteLine("ConfigureVaem(): " + s);
                
                s = string.Join(", ", ReadWrite(
                    (int) VAEMConstants.VaemAccess.WRITE,
                    (int) VAEMConstants.VaemDataType.UINT16,
                    (int) VAEMConstants.VaemIndex.INRUSH_CURRENT,
                    valve,
                    (int) VaemSettings.INRUSH_CURRENT));

                if (DEBUG_ENABLED)
                    Console.WriteLine("ConfigureVaem(): " + s);
                
                s = string.Join(", ", ReadWrite(
                    (int) VAEMConstants.VaemAccess.WRITE,
                    (int) VAEMConstants.VaemDataType.UINT16,
                    (int) VAEMConstants.VaemIndex.HOLDING_CURRENT,
                    valve,
                    (int) VaemSettings.HOLDING_CURRENT));

                if (DEBUG_ENABLED)
                    Console.WriteLine("ConfigureVaem(): " + s);
                
                s = string.Join(", ", ReadWrite(
                    (int) VAEMConstants.VaemAccess.WRITE,
                    (int) VAEMConstants.VaemDataType.UINT32,
                    (int) VAEMConstants.VaemIndex.RESPONSE_TIME,
                    valve,
                    (int) VaemSettings.RESPONSE_TIME));

                if (DEBUG_ENABLED)
                    Console.WriteLine("ConfigureVaem(): " + s);
                
                s = string.Join(", ", ReadWrite(
                    (int) VAEMConstants.VaemAccess.WRITE,
                    (int) VAEMConstants.VaemDataType.UINT32,
                    (int) VAEMConstants.VaemIndex.PICKUP_TIME,
                    valve,
                    (int) VaemSettings.PICKUP_TIME));

                if (DEBUG_ENABLED)
                    Console.WriteLine("ConfigureVaem(): " + s);
                
                s = string.Join(", ", ReadWrite(
                    (int) VAEMConstants.VaemAccess.WRITE,
                    (int) VAEMConstants.VaemDataType.UINT32,
                    (int) VAEMConstants.VaemIndex.TIME_DELAY,
                    valve,
                    (int) VaemSettings.TIME_DELAY));

                if (DEBUG_ENABLED)
                    Console.WriteLine("ConfigureVaem(): " + s);
                
                s = string.Join(", ", ReadWrite(
                    (int) VAEMConstants.VaemAccess.WRITE,
                    (int) VAEMConstants.VaemDataType.UINT32,
                    (int) VAEMConstants.VaemIndex.HIT_N_HOLD,
                    valve,
                    (int) VaemSettings.HIT_N_HOLD));
                
                if (DEBUG_ENABLED)
                    Console.WriteLine("ConfigureVaem(): " + s);
            }
            SaveSettings();
        }

        public void ConfigureValves(int[] openingTimes)
        {
            if (openingTimes.Length != 8)
            {
                throw new Exception("ConfigureValves(): openingTimes must be of length 8.");
            }
            
            int[] valves =
            {
                (int) VAEMConstants.VaemValveIndex.VALVE1,
                (int) VAEMConstants.VaemValveIndex.VALVE2,
                (int) VAEMConstants.VaemValveIndex.VALVE3,
                (int) VAEMConstants.VaemValveIndex.VALVE4,
                (int) VAEMConstants.VaemValveIndex.VALVE5,
                (int) VAEMConstants.VaemValveIndex.VALVE6,
                (int) VAEMConstants.VaemValveIndex.VALVE7,
                (int) VAEMConstants.VaemValveIndex.VALVE8
            };
            
            int selValves = 0;
            try {
                for (int i = 0; i < openingTimes.Length; i++) {
                    if (openingTimes[i] != 0) {
                        selValves = selValves | valves[i];
                    }
                    ReadWrite(
                        (int) VAEMConstants.VaemAccess.WRITE,
                        (int) VAEMConstants.VaemDataType.UINT32, 
                        (int) VAEMConstants.VaemIndex.RESPONSE_TIME, 
                        i, 
                        openingTimes[i]);
                }
                
                ReadWrite(
                    (int) VAEMConstants.VaemAccess.WRITE,
                    (int) VAEMConstants.VaemDataType.UINT8,
                    (int) VAEMConstants.VaemIndex.SELECT_VALVE,
                    0,
                    selValves);
            } catch (Exception e) {
                Console.WriteLine("ConfigureValves(): Error setting up valves");
            }
        }
        
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
        
        public void OpenValve() {
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

        public void CloseValve() {
            string s = string.Join(", ", ReadWrite(
                (int) VAEMConstants.VaemAccess.WRITE,
                (int) VAEMConstants.VaemDataType.UINT16, 
                (int) VAEMConstants.VaemIndex.CONTROL_WORD, 
                0,
                (int) VAEMConstants.VaemControlWord.STOP_VALVES));
            
            if (DEBUG_ENABLED)
                Console.WriteLine("CloseValve(): " + s);
        }

        public int[] ReadStatus() {
            int[] ret =  ReadWrite(
                (int) VAEMConstants.VaemAccess.READ,
                (int) VAEMConstants.VaemDataType.UINT16, 
                (int) VAEMConstants.VaemIndex.STATUS_WORD, 
                0,
                0);

            string s = string.Join(", ", ret);

            Console.WriteLine("ReadStatus(): " + s);

            return ret;
        }
        
        public void ClearError() {
            string s = string.Join(", ", ReadWrite(
                (int) VAEMConstants.VaemAccess.WRITE,
                (int) VAEMConstants.VaemDataType.UINT16, 
                (int) VAEMConstants.VaemIndex.CONTROL_WORD, 
                0,
                (int) VAEMConstants.VaemControlWord.RESET_ERRORS));
            
            if (DEBUG_ENABLED)
                Console.WriteLine("ClearError(): " + s);
        }
    }
}
