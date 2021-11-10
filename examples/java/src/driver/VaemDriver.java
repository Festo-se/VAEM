/* Author:     Raines, Jared
 * Copyright:  Copyright 2021, Festo Life Tech
 * Version:    0.0.1
 * Maintainer: Raines, Jared
 * Email:      raines.j@northeastern.edu
 * Status:     Development
 */

package driver;
import de.re.easymodbus.modbusclient.*;
import java.util.Arrays;


public class VaemDriver implements IVaemDriver {

    private final ModbusClient modbusClient;

    public VaemDriver(String host, int port) {
        this.modbusClient = new ModbusClient(host, port);
        //this.modbusClient.setConnectionTimeout(5000);
        this.modbusClient.setUnitIdentifier((byte)0);

        //for (int i = 0; i < 3; i++) {
        try {
          this.modbusClient.Connect();
              //System.out.println("Attempt: " + (i + 1));
        } catch (Exception e) {
          System.out.println("Could not connect to VAEM: " + e);
        }
        //}
    }

    public void init() {
        // set to operating mode 1
        transfer(VaemAccess.Write.val,
                VaemDataType.UINT8.val, VaemIndex.OperatingMode.val, 0, VaemOperatingModes.OpMode1.val);
        // read the current operating mode
        System.out.println(Arrays.toString(transfer(VaemAccess.Read.val,
                VaemDataType.UINT8.val, VaemIndex.OperatingMode.val, 0, 0)));
        // select valve 1
        //System.out.println(Arrays.toString(transfer(VaemAccess.Write.val,
        //        VaemDataType.UINT8.val, VaemIndex.SelectValve.val, 0, VaemValveIndex.Valve1.val)));

        System.out.println("VAEM Initialized");
    }

    public void configureVaem() {
        int[] paramIndex = {0x04, 0x05, 0x06, 0x07, 0x08, 0x16, 0x2e};
        int[] settingsDataType = {2, 3, 3, 2, 2, 3, 3};
        int[] settingsValue = {24000, 500, 0, 125, 300, 100, 100};
        int i = 0;
        try {
            for (VaemValveIndex valve : VaemValveIndex.values()) {
                for (int pIndex : paramIndex) {
                    transfer(VaemAccess.Write.val,
                            settingsDataType[i], pIndex, valve.val, settingsValue[i]);
                    i++;
                }
            }
        }
        catch (Exception e)
        {
            System.out.println("Error configuring VAEM");
        }
    }

    public int[] transfer(int access, int dataType, int index, int subIndex, int transferVal) {
        int[] ret = new int[7], writeData = new int[7];
        writeData[0] = (access << 8) + dataType;
        writeData[1] = index;
        writeData[2] = subIndex << 8;
        writeData[3] = 0;
        writeData[4] = 0;
        writeData[5] = 0;
        writeData[6] = transferVal;

        try {
            ret = modbusClient.ReadWriteMultipleRegisters(
                    0, 0x07, 0, writeData);
        } catch(Exception e) {
            System.out.println("Something went wrong with read/write operation");
        }

        return ret;
    }

    public int[] deconstructFrame(int[] frame) {
        int[] data = new int[6];
        if (frame != null) {
            data[0] = (frame[0] & 0xff00) >> 8;
            data[1] = frame[0] & 0x00ff;
            data[2] = frame[1];
            data[3] = (frame[2] & 0xff00) >> 8;
            data[4] = frame[2] & 0x00ff;
            data[5] = 0;
            for (int i = 0; i < 4; i++) {
                data[5] += (frame[frame.length-1-i] << (i*16));
            }
        }
        else {
            System.out.println("cannot read frame");
        }
        return data;
    }

    public int[] getStatus(int statusWord) {
        int status = new int[12];
        status[0] = statusWord & 0x01;
        status[1] = (statusWord & 0x08) >> 3;
        status[2] = (statusWord & 0x10) >> 4;
        status[3] = (statusWord & 0xC0) >> 6;

        System.out.println("Status: " + (statusWord & 0x01));
        System.out.println("Error: " + ((statusWord & 0x08) >> 3));
        System.out.println("Readiness: " + ((statusWord & 0x10) >> 4));
        System.out.println("Operating Mode: " + ((statusWord & 0xC0) >> 6));

        status[4] = (statusWord & 0x100) >> 8;
        status[5] = (statusWord & 0x200) >> 9;
        status[6] = (statusWord & 0x400) >> 10;
        status[7] = (statusWord & 0x800) >> 11;
        status[8] = (statusWord & 0x1000) >> 12;
        status[9] = (statusWord & 0x2000) >> 13;
        status[10] = (statusWord & 0x4000) >> 14;
        status[11] = (statusWord & 0x8000) >> 15;

        System.out.println("Valve 1: " + ((statusWord & 0x100) >> 8));
        System.out.println("Valve 2: " + ((statusWord & 0x200) >> 9));
        System.out.println("Valve 3: " + ((statusWord & 0x400) >> 10));
        System.out.println("Valve 4: " + ((statusWord & 0x800) >> 11));
        System.out.println("Valve 5: " + ((statusWord & 0x1000) >> 12));
        System.out.println("Valve 6: " + ((statusWord & 0x2000) >> 13));
        System.out.println("Valve 7: " + ((statusWord & 0x4000) >> 14));
        System.out.println("Valve 8: " + ((statusWord & 0x8000) >> 15));
        if (((statusWord & 0x08) >> 3) == 1) {
            clearError();
        }

        return status;
    }

    public void openValve() {
        transfer(VaemAccess.Write.val,
                VaemDataType.UINT16.val, VaemIndex.ControlWord.val, 0, VaemControlWords.StartValves.val);
        /*
        System.out.println(Arrays.toString(transfer(VaemAccess.Write.val,
                VaemDataType.UINT16.val, VaemIndex.ControlWord.val, 0, VaemControlWords.StartValves.val)));

         */
    }

    public void closeValve() {
        transfer(VaemAccess.Write.val,
                VaemDataType.UINT16.val, VaemIndex.ControlWord.val, 0, VaemControlWords.StopValves.val);
        /*
        System.out.println(Arrays.toString(transfer(VaemAccess.Write.val,
                VaemDataType.UINT16.val, VaemIndex.ControlWord.val, 0, VaemControlWords.StopValves.val)));

        */
    }

    public void configureValves(int[] openingTimes) {
       VaemValveIndex[] valves = VaemValveIndex.values();
       int selValves = 0;
       if (openingTimes.length > 8) {
           throw new ArgumentException("Must configure 1-8 valves");
       }
       for(int t : openingTimes) {
           if (t < 0 || t > 2000) {
               thrown new ArgumentException("Opening times must be between 0-2000");
           }
       }
       try {
           for (int i = 0; i < openingTimes.length; i++) {
               if (openingTimes[i] != 0) {
                   selValves = selValves | valves[i].val;
               }
               transfer(VaemAccess.Write.val,
                       VaemDataType.UINT32.val, VaemIndex.ResponseTime.val, valves[i].val, openingTimes[i]);
           }
           transfer(VaemAccess.Write.val,
                   VaemDataType.UINT8.val, VaemIndex.SelectValve.val, 0, selValves);
       } catch (Exception e) {
            System.out.println("Error setting up valves");
       }
    }

    public void readStatus() {
        int[] status = getStatus(deconstructFrame(transfer(VaemAccess.Read.val,
                VaemDataType.UINT16.val, VaemIndex.StatusWord.val, 0, 0))[5]);
        
        return Arrays.copyOfRange(status, 5, status.length);
    }

    public void clearError() {
        transfer(VaemAccess.Write.val,
                VaemDataType.UINT16.val, VaemIndex.ControlWord.val, 0, VaemControlWords.ResetErrors.val);
    }

    public void saveSettings() {
        transfer(VaemAccess.Write.val, VaemDataType.UINT32.val, VaemIndex.SaveParameters.val, 0, 99999);
    }
}
