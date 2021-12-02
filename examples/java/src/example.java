import driver.VaemDriver;
import static java.lang.Thread.sleep;

public class example {
    public static void main(String[] args) throws InterruptedException {
        VaemDriver vm = new VaemDriver("192.168.0.220", 502);
        vm.init();
        vm.selectValve(1);
        vm.setOpeningTime(1, 500);

        while (true) {
            sleep(1000);
            vm.readStatus();
            vm.openValve();
            sleep(1000);
            vm.readStatus();
            vm.closeValve();
        }



    }

}
