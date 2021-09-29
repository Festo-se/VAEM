package driver;

/* Author:     Raines, Jared
 * Copyright:  Copyright 2021, Festo Life Tech
 * Version:    0.0.1
 * Maintainer: Raines, Jared
 * Email:      raines.j@northeastern.edu
 * Status:     Development
 */
public interface IVaemDriver {
    void openValve();
    void closeValve();
    void configureValves(int[] openingTimes);
    void readStatus();
    void clearError();


    enum VaemAccess {
        Read(0),
        Write(1);

        public final int val;

        private VaemAccess(int val) {
            this.val = val;
        }
    }

    enum VaemDataType {
        UINT8(1),
        UINT16(2),
        UINT32(3),
        UINT64(4);

        public final int val;

        private VaemDataType(int val) {
            this.val = val;
        }
    }

    enum VaemIndex {
        ControlWord(0x01),
        StatusWord(0x02),
        NominalVoltage(0x04),
        InrushCurrent(0x05),
        HoldingCurrent(0x06),
        ResponseTime(0x07),
        PickUpTime(0x08),
        OperatingMode(0x09),
        SaveParameters(0x11),
        SelectValve(0x13),
        TimeDelay(0x16),
        HitNHold(0x2E);

        public final int val;

        private VaemIndex(int val) {
            this.val = val;
        }
    }

    enum VaemValveIndex {
        Valve1(0x01),
        Valve2(0x02),
        Valve3(0x04),
        Valve4(0x08),
        Valve5(0x10),
        Valve6(0x20),
        Valve7(0x40),
        Valve8(0x80),
        AllValves(255);

        public final int val;

        private VaemValveIndex(int val) {
            this.val = val;
        }
    }

    enum VaemControlWords {
        StartValves(0x01),
        StopValves(0x04),
        ResetErrors(0x08);

        public final int val;

        private VaemControlWords(int val) {
            this.val = val;
        }
    }

    enum VaemOperatingModes {
        OpMode1(0x00),
        OpMode2(0x01),
        OpMode3(0x02);

        public final int val;

        private VaemOperatingModes(int val) {
            this.val = val;
        }
    }

}
