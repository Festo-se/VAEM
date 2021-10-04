using System;
using EasyModbus;

namespace driver
{
    class VaemDriver
    {
        private ModbusClient client;
        
        public enum VaemSettings : int
        {
            NOMINAL_VOLTAGE = 24000,
            INRUSH_CURRENT = 500,
            HOLDING_CURRENT = 0,
            RESPONSE_TIME = 125,
            PICKUP_TIME = 300,
            TIME_DELAY = 100,
            HIT_N_HOLD = 100
        }
        
        public VaemDriver(string ip, int port)
        {

            this.client = new ModbusClient(ip, port);

            for (int i = 0; i < 3; i++) {
                try
                {
                    while (client.Available(1000))
                    {
                        this.client.Connect();
                    }
                } catch (EasyModbus.Exceptions.ConnectionException e) {
                    Console.WriteLine("Could not connect to VAEM: " + e + ", attempt {" + (i+1) + "}");
                }
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
            
            // select valve
            ReadWrite((int) VAEMConstants.VaemAccess.WRITE,
                (int) VAEMConstants.VaemDataType.UINT8,
                (int) VAEMConstants.VaemIndex.SELECT_VALVE,
                0,
                (int) VAEMConstants.VaemValveIndex.VALVE1);
        }

        private int[] ReadWrite(int access, int dataType, int index, int subindex, int transferVal)
        {
            int[] writeData = new int[7];
            writeData[0] = (access << 8) + dataType;
            writeData[1] = index;
            writeData[2] = subindex;
            writeData[3] = 0;
            writeData[4] = 0;
            writeData[5] = 0;
            writeData[6] = transferVal;
            return this.client.ReadWriteMultipleRegisters(0, 0x07, 0, writeData);
        }

        public void ConfigureVaem()
        {
            int[] valveIndex =
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

            foreach (int valve in valveIndex)
            {
                ReadWrite(
                    (int) VAEMConstants.VaemAccess.WRITE,
                    (int) VAEMConstants.VaemDataType.UINT16,
                    (int) VAEMConstants.VaemIndex.NOMINAL_VOLTAGE,
                    valve,
                    (int) VaemSettings.NOMINAL_VOLTAGE);

                ReadWrite(
                    (int) VAEMConstants.VaemAccess.WRITE,
                    (int) VAEMConstants.VaemDataType.UINT32,
                    (int) VAEMConstants.VaemIndex.INRUSH_CURRENT,
                    valve,
                    (int) VaemSettings.INRUSH_CURRENT);

                ReadWrite(
                    (int) VAEMConstants.VaemAccess.WRITE,
                    (int) VAEMConstants.VaemDataType.UINT16,
                    (int) VAEMConstants.VaemIndex.HOLDING_CURRENT,
                    valve,
                    (int) VaemSettings.HOLDING_CURRENT);

                ReadWrite(
                    (int) VAEMConstants.VaemAccess.WRITE,
                    (int) VAEMConstants.VaemDataType.UINT32,
                    (int) VAEMConstants.VaemIndex.RESPONSE_TIME,
                    valve,
                    (int) VaemSettings.RESPONSE_TIME);

                ReadWrite(
                    (int) VAEMConstants.VaemAccess.WRITE,
                    (int) VAEMConstants.VaemDataType.UINT16,
                    (int) VAEMConstants.VaemIndex.PICKUP_TIME,
                    valve,
                    (int) VaemSettings.PICKUP_TIME);

                ReadWrite(
                    (int) VAEMConstants.VaemAccess.WRITE,
                    (int) VAEMConstants.VaemDataType.UINT32,
                    (int) VAEMConstants.VaemIndex.TIME_DELAY,
                    valve,
                    (int) VaemSettings.TIME_DELAY);

                ReadWrite(
                    (int) VAEMConstants.VaemAccess.WRITE,
                    (int) VAEMConstants.VaemDataType.UINT32,
                    (int) VAEMConstants.VaemIndex.HIT_N_HOLD,
                    valve,
                    (int) VaemSettings.HIT_N_HOLD);
            }
        }
        
        public void SaveSettings()
        {
            Console.WriteLine(string.Join(", ", ReadWrite(
                (int) VAEMConstants.VaemAccess.WRITE,
                (int) VAEMConstants.VaemDataType.UINT32, 
                (int) VAEMConstants.VaemIndex.SAVE_PARAMETERS, 
                0,
                99999)));
        }
        
        public void OpenValve() {
            Console.WriteLine(string.Join(", ", ReadWrite(
                (int) VAEMConstants.VaemAccess.WRITE,
                (int) VAEMConstants.VaemDataType.UINT16, 
                (int) VAEMConstants.VaemIndex.CONTROL_WORD, 
                0,
                (int) VAEMConstants.VaemControlWord.START_VALVES)));
        }

        public void CloseValve() {
            Console.WriteLine(string.Join(", ", ReadWrite(
                (int) VAEMConstants.VaemAccess.WRITE,
                (int) VAEMConstants.VaemDataType.UINT16, 
                (int) VAEMConstants.VaemIndex.CONTROL_WORD, 
                0,
                (int) VAEMConstants.VaemControlWord.STOP_VALVES)));
        }

        public void ReadStatus() {
            Console.WriteLine(string.Join(", ", ReadWrite(
                (int) VAEMConstants.VaemAccess.READ,
                (int) VAEMConstants.VaemDataType.UINT16, 
                (int) VAEMConstants.VaemIndex.STATUS_WORD, 
                0,
                0)));
        }
    }
}