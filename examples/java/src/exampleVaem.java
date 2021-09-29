import driver.VaemDriver;

import static java.lang.Thread.sleep;

public class exampleVaem {
    public static void main(String[] args) throws InterruptedException {
        int[] valveData = {500, 0, 0, 0, 0, 0, 0, 0};
        VaemDriver vm = new VaemDriver("192.168.0.214", 502);
        vm.init();
        vm.configureValves(valveData);

        while (true) {
            sleep(1000);
            vm.openValve();
            sleep(1000);
            vm.readStatus();
            vm.closeValve();
        }



    }

}
