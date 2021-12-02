/* Author:     Raines, Jared
 * Copyright:  Copyright 2021, Festo Life Tech
 * Version:    0.0.1
 * Maintainer: Raines, Jared
 * Email:      raines.j@northeastern.edu
 * Status:     Development
 */

package driver;
import de.re.easymodbus.modbusclient.*;
import java.io.IOException;


// VAEM (8-valve controller) class
public class VaemDriver implements IVaemDriver {

    private final ModbusClient modbusClient;
    private final int[] VaemValveIndex = {0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 255};

    // VAEM constructor
    public VaemDriver(String host, int port) {
        this.modbusClient = new ModbusClient(host, port);
        this.modbusClient.setUnitIdentifier((byte)0);

        try {
            this.modbusClient.Connect();
        } catch (Exception e) {
            System.out.println("Could not connect to VAEM: " + e);
        }
    }

    // initialize the VAEM
    public void init() {
        // set to operating mode 1
        transfer(VaemAccess.Write.val,
                VaemDataType.UINT8.val, VaemIndex.OperatingMode.val, 0, VaemOperatingModes.OpMode1.val);
        // clear errors
        transfer(VaemAccess.Write.val,
                VaemDataType.UINT16.val, VaemIndex.ControlWord.val, 0, VaemControlWords.ResetErrors.val);
    }

    // disconnect from the VAEM
    public void disconnect() throws IOException {
        this.modbusClient.Disconnect();
    }

    // construct a modbus frame and send it to the device
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

    // save the current device settings to memory
    public void saveSettings() {
        transfer(VaemAccess.Write.val,
                VaemDataType.UINT32.val, VaemIndex.SaveParameters.val, 0, 99999);
    }

    // select the given valve
    public void selectValve(int valve_id) {
        if (valve_id < 1 || valve_id > 8) {
            throw new IllegalArgumentException("Valve ID must in range 1-8");
        }
        int selValves = readValves();
        selValves = selValves | VaemValveIndex[valve_id-1];
        transfer(VaemAccess.Write.val,
                VaemDataType.UINT8.val, VaemIndex.SelectValve.val, 0, selValves);
    }

    // deselect the given valve
    public void deselectValve(int valve_id) {
        if (valve_id < 1 || valve_id > 8) {
            throw new IllegalArgumentException("Valve ID must be in range 1-8");
        }
        int selValves = readValves();
        if ((selValves & VaemValveIndex[valve_id-1]) > 0) {
            selValves = selValves - VaemValveIndex[valve_id-1];
            transfer(VaemAccess.Write.val,
                    VaemDataType.UINT8.val, VaemIndex.SelectValve.val, 0, selValves);
        }
    }

    // set the opening time of the given valve
    public void setOpeningTime(int valve_id, int opening_time) {
        if (valve_id < 1 || valve_id > 8) {
            throw new IllegalArgumentException("Valve ID must be in range 1-8");
        }
        if (opening_time < 1 || opening_time > 2000) {
            throw new IllegalArgumentException("Opening time must be in range 1-2000");
        }
        if ((readValves() & VaemValveIndex[valve_id-1]) == 0) {
            throw new IllegalArgumentException("Valve " + valve_id + " is not selected");
        }
        transfer(VaemAccess.Write.val,
                VaemDataType.UINT32.val, VaemIndex.ResponseTime.val, valve_id-1, opening_time);
    }

    // open all selected valves
    public void openValve() {
        transfer(VaemAccess.Write.val,
                VaemDataType.UINT16.val, VaemIndex.ControlWord.val, 0, VaemControlWords.StartValves.val);
    }

    // close all selected valves
    public void closeValve() {
        transfer(VaemAccess.Write.val,
                VaemDataType.UINT16.val, VaemIndex.ControlWord.val, 0, VaemControlWords.StopValves.val);
    }

    // read the status of the VAEM
    public int[] readStatus() {
        return getStatus(deconstructFrame(transfer(VaemAccess.Read.val,
                VaemDataType.UINT16.val, VaemIndex.StatusWord.val, 0, 0))[5]);
    }

    // clear the error bit
    public void clearError() {
        transfer(VaemAccess.Write.val,
                VaemDataType.UINT16.val, VaemIndex.ControlWord.val, 0, VaemControlWords.ResetErrors.val);
    }

    // read which valves are currently selected
    public int readValves() {
        return (transfer(VaemAccess.Read.val,
                VaemDataType.UINT8.val, VaemIndex.SelectValve.val, 0, 0))[6];
    }

    // read the opening time of a valve by ID
    public int readOpeningTime(int valve_id) {
        return (transfer(VaemAccess.Read.val,
                VaemDataType.UINT32.val, VaemIndex.ResponseTime.val, valve_id - 1, 0))[6];
    }

    // deconstruct a Modbus frame
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

    // return the formatted status word
    public int[] getStatus(int statusWord) {
        int[] status = new int[12];
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

        return status;
    }

}


    /*
    public void configureVaem() {
        byte[] paramIndex = {0x04, 0x05, 0x06, 0x07, 0x08, 0x16, 0x2e};

        try {
            for (VaemIndex i : VaemIndex.values()) {
                if (Arrays.asList(paramIndex).contains(i.val)){
                    for (VaemValveIndex v : VaemValveIndex.values()) {
                        // data = getValveSetting(i, v);
                        // frame = constructFrame(data);
                        // transfer(frame);
                    }
                }
            }
        }
        catch (Exception e) {
            System.out.println("Unable to configure: " + e);
        }

        saveSettings();
    }
    */



/*
class VaemSerialPort implements SerialPortWrapper {

    @Override
    public void close() throws Exception {

    }

    @Override
    public void open() throws Exception {

    }

    @Override
    public InputStream getInputStream() {
        return null;
    }

    @Override
    public OutputStream getOutputStream() {
        return null;
    }

    @Override
    public int getBaudRate() {
        return 0;
    }

    @Override
    public int getDataBits() {
        return 0;
    }

    @Override
    public int getStopBits() {
        return 0;
    }

    @Override
    public int getParity() {
        return 0;
    }
}
*/