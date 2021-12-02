namespace VaemCSharpDriver.driver
{
    public class VAEMConstants
    {
        public enum VaemAccess : int
        {
            READ = 0,
            WRITE = 1
        }

        public enum VaemDataType : int
        {
            UINT8 = 1,
            UINT16 = 2,
            UINT32 = 3,
            UINT64 = 4
        }

        public enum VaemIndex : int
        {
            CONTROL_WORD = 0x01,
            STATUS_WORD = 0x02,
            NOMINAL_VOLTAGE = 0x04,
            INRUSH_CURRENT = 0x05,
            HOLDING_CURRENT = 0x06,
            RESPONSE_TIME = 0x07,
            PICKUP_TIME = 0x08,
            OPERATING_MODE = 0x09,
            SAVE_PARAMETERS = 0x0B,
            SELECT_VALVE = 0x13,
            TIME_DELAY = 0x16,
            HIT_N_HOLD = 0x2E
        }

        public enum VaemValveIndex : int
        {
            VALVE1 = 0x01,
            VALVE2 = 0x02,
            VALVE3 = 0x04,
            VALVE4 = 0x08,
            VALVE5 = 0x10,
            VALVE6 = 0x20,
            VALVE7 = 0x40,
            VALVE8 = 0x80,
            ALL_VALVES = 0xFF
        }

        public enum VaemControlWord : int
        {
            START_VALVES = 0x01,
            STOP_VALVES = 0x04,
            RESET_ERRORS = 0x08
        }

        public enum VaemOperatingMode : int
        {
            MODE1 = 0x00,
            MODE2 = 0x01,
            MODE3 = 0x02
        }
    }
}