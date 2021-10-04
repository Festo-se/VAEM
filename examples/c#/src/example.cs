using driver;

class Example {
    static void Main(string[] args)
    {
                VaemDriver driver = new VaemDriver("192.168.0.207", 502);
                driver.ConfigureVaem();
                driver.SaveSettings();
                while(1) {
                    sleep(1000);
                    driver.OpenValve();
                    sleep(1000);
                    driver.ReadStatus();
                    driver.CloseValve();
                }
    }
}