import driver.VaemDriver;
import static java.lang.Thread.sleep;
import static org.junit.Assert.*;
import static org.junit.jupiter.api.Assertions.assertThrows;
import java.io.IOException;
import java.util.Arrays;

class Tests {
    VaemDriver vm;

    public void init() {
        this.vm = new VaemDriver("192.168.0.220", 502);
        this.vm.init();
        for (int i = 1; i < 9; i++) {
            vm.deselectValve(i);
        }
        vm.selectValve(1);
        vm.setOpeningTime(1, 500);
        vm.closeValve();
    }

    // test for selectValve(int valve_id)
    @org.junit.jupiter.api.Test
    public void testSelectValve() throws InterruptedException, IOException {
        init();
        // valve 1 selected
        assertEquals(1, vm.readValves());
        vm.selectValve(1);
        assertEquals(1, vm.readValves());
        // valve 2 selected
        vm.selectValve(2);
        assertEquals(3, vm.readValves());
        // valve 3 selected
        vm.selectValve(3);
        assertEquals(7, vm.readValves());
        // valve 4 selected
        vm.selectValve(4);
        assertEquals(15, vm.readValves());
        // valve 5 selected
        vm.selectValve(5);
        assertEquals(31, vm.readValves());
        // valve 6 selected
        vm.selectValve(6);
        assertEquals(63, vm.readValves());
        // valve 7 selected
        vm.selectValve(7);
        assertEquals(127, vm.readValves());
        // valve 8 selected
        vm.selectValve(8);
        assertEquals(255, vm.readValves());
        vm.disconnect();
    }

    // tests for selectValve(int valve_id) with the wrong ID
    @org.junit.jupiter.api.Test
    public void testSelectValveWrongId() throws IOException {
        init();
        Exception exception = assertThrows(IllegalArgumentException.class, () -> {
            vm.selectValve(-1);
        });
        String expectedMessage = "Valve ID must in range 1-8";
        String actualMessage = exception.getMessage();
        assertTrue(actualMessage.contains(expectedMessage));

        exception = assertThrows(IllegalArgumentException.class, () -> {
            vm.selectValve(0);
        });
        expectedMessage = "Valve ID must in range 1-8";
        actualMessage = exception.getMessage();
        assertTrue(actualMessage.contains(expectedMessage));

        exception = assertThrows(IllegalArgumentException.class, () -> {
            vm.selectValve(9);
        });
        expectedMessage = "Valve ID must in range 1-8";
        actualMessage = exception.getMessage();
        assertTrue(actualMessage.contains(expectedMessage));

        vm.disconnect();
    }

    // tests for deselectValve(int valve_id)
    @org.junit.jupiter.api.Test
    public void testDeselectValve() throws IOException {
        init();
        for (int i = 1; i < 9; i++) {
            vm.selectValve(i);
        }
        //All valves selected
        assertEquals(255, vm.readValves());
        //Deselect valve 8
        vm.deselectValve(8);
        assertEquals(127, vm.readValves());
        //Deselect valve 7
        vm.deselectValve(7);
        assertEquals(63, vm.readValves());
        //Deselect valve 6
        vm.deselectValve(6);
        assertEquals(31, vm.readValves());
        //Deselect valve 5
        vm.deselectValve(5);
        assertEquals(15, vm.readValves());
        //Deselect valve 4
        vm.deselectValve(4);
        assertEquals(7, vm.readValves());
        //Deselect valve 3
        vm.deselectValve(3);
        assertEquals(3, vm.readValves());
        //Deselect valve 2
        vm.deselectValve(2);
        assertEquals(1, vm.readValves());
        //Deselect valve 1
        vm.deselectValve(1);
        assertEquals(0, vm.readValves());
        vm.disconnect();
    }

    // tests for deselectValve(int valve_id) with the wrong ID
    @org.junit.jupiter.api.Test
    public void testDeselectValveWrongId() throws IOException {
        init();
        Exception exception = assertThrows(IllegalArgumentException.class, () -> {
            vm.deselectValve(-1);
        });
        String expectedMessage = "Valve ID must be in range 1-8";
        String actualMessage = exception.getMessage();
        assertTrue(actualMessage.contains(expectedMessage));

        exception = assertThrows(IllegalArgumentException.class, () -> {
            vm.deselectValve(0);
        });
        expectedMessage = "Valve ID must be in range 1-8";
        actualMessage = exception.getMessage();
        assertTrue(actualMessage.contains(expectedMessage));

        exception = assertThrows(IllegalArgumentException.class, () -> {
            vm.deselectValve(9);
        });
        expectedMessage = "Valve ID must be in range 1-8";
        actualMessage = exception.getMessage();
        assertTrue(actualMessage.contains(expectedMessage));

        vm.disconnect();
    }
    
    // tests for setOpeningTime(int valve_id, int opening_time)
    @org.junit.jupiter.api.Test
    public void testSetOpeningTime() throws IOException {
        init();
        //valve 1 initially has an opening time of 500 ms
        assertEquals(500, vm.readOpeningTime(1));
        //valve 1 opening time 500 ms
        vm.setOpeningTime(1, 500);
        assertEquals(500, vm.readOpeningTime(1));
        //valve 1 opening time 1 ms
        vm.setOpeningTime(1, 1);
        assertEquals(1, vm.readOpeningTime(1));
        //valve 1 opening time 2000 ms
        vm.setOpeningTime(1, 2000);
        assertEquals(2000, vm.readOpeningTime(1));
        //valve 8 selected
        vm.selectValve(8);
        System.out.println(vm.readValves());
        //valve 8 opening time 500 ms
        vm.setOpeningTime(8, 500);
        assertEquals(500, vm.readOpeningTime(8));
        vm.disconnect();
    }

    // tests for setOpeningTime(int valve_id, int opening_time) with the wrong ID
    @org.junit.jupiter.api.Test
    public void testSetOpeningTimeWrongId() throws IOException {
        init();
        Exception exception = assertThrows(IllegalArgumentException.class, () -> {
            vm.setOpeningTime(-1, 500);
        });
        String expectedMessage = "Valve ID must be in range 1-8";
        String actualMessage = exception.getMessage();
        assertTrue(actualMessage.contains(expectedMessage));

        exception = assertThrows(IllegalArgumentException.class, () -> {
            vm.setOpeningTime(0, 500);
        });
        expectedMessage = "Valve ID must be in range 1-8";
        actualMessage = exception.getMessage();
        assertTrue(actualMessage.contains(expectedMessage));

        exception = assertThrows(IllegalArgumentException.class, () -> {
            vm.setOpeningTime(9, 500);
        });
        expectedMessage = "Valve ID must be in range 1-8";
        actualMessage = exception.getMessage();
        assertTrue(actualMessage.contains(expectedMessage));

        exception = assertThrows(IllegalArgumentException.class, () -> {
            vm.setOpeningTime(9, 5000);
        });
        expectedMessage = "Valve ID must be in range 1-8";
        actualMessage = exception.getMessage();
        assertTrue(actualMessage.contains(expectedMessage));

        vm.disconnect();
    }
    
    // tests for setOpeningTime(int valve_id, int opening_time) with wrong time
    @org.junit.jupiter.api.Test
    public void testSetOpeningTimeWrongTime() throws IOException {
        init();
        // negative time
        Exception exception = assertThrows(IllegalArgumentException.class, () -> {
            vm.setOpeningTime(1, -1);
        });
        String expectedMessage = "Opening time must be in range 1-2000";
        String actualMessage = exception.getMessage();
        assertTrue(actualMessage.contains(expectedMessage));

        // zero time
        exception = assertThrows(IllegalArgumentException.class, () -> {
            vm.setOpeningTime(1, 0);
        });
        expectedMessage = "Opening time must be in range 1-2000";
        actualMessage = exception.getMessage();
        assertTrue(actualMessage.contains(expectedMessage));

        // time > 2000 ms
        exception = assertThrows(IllegalArgumentException.class, () -> {
            vm.setOpeningTime(1, 2001);
        });
        expectedMessage = "Opening time must be in range 1-2000";
        actualMessage = exception.getMessage();
        assertTrue(actualMessage.contains(expectedMessage));

        vm.disconnect();
    }

    // tests for setOpeningTime(int valve_id, int opening_time) with a non-selected valve
    @org.junit.jupiter.api.Test
    public void testSetOpeningTimeWrongValve() throws IOException {
        init();

        // valve 7 not selected
        Exception exception = assertThrows(IllegalArgumentException.class, () -> {
            vm.setOpeningTime(7, 500);
        });
        String expectedMessage = "Valve 7 is not selected";
        String actualMessage = exception.getMessage();
        assertTrue(actualMessage.contains(expectedMessage));

        vm.disconnect();
    }

    // tests for openValve()
    @org.junit.jupiter.api.Test
    public void testOpenValve() throws InterruptedException, IOException {
        init();
        assertEquals(0, vm.readStatus()[2]);
        vm.openValve();
        sleep(200);
        assertEquals(1, vm.readStatus()[2]);
        vm.disconnect();
    }

    // tests for closeValve()
    @org.junit.jupiter.api.Test
    void testCloseValve() throws InterruptedException, IOException {
        init();
        vm.openValve();
        sleep(200);
        assertEquals(1, vm.readStatus()[2]);
        vm.closeValve();
        assertEquals(0, vm.readStatus()[2]);
        vm.disconnect();
    }

    // tests for int[] readStatus
    @org.junit.jupiter.api.Test
    void testReadStatus() throws IOException, InterruptedException {
        init();
        vm.openValve();
        sleep(200);
        int[] testData = vm.readStatus();

        // status
        assertEquals(0, testData[0]);
        // error
        assertEquals(0, testData[1]);
        //readiness
        assertEquals(1, testData[2]);
        // operating mode
        assertEquals(0, testData[3]);
        //valves 1-8 status (1 = open)
        assertEquals(1, testData[4]);
        assertEquals(0, testData[5]);
        assertEquals(0, testData[6]);
        assertEquals(0, testData[7]);
        assertEquals(0, testData[8]);
        assertEquals(0, testData[9]);
        assertEquals(0, testData[10]);
        assertEquals(0, testData[11]);

        vm.disconnect();
    }
}