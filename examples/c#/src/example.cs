using driver;

class Example {
    static void Main(string[] args)
    {
                VaemDriver driver = new VaemDriver("192.168.0.207", 502);
                driver.ConfigureVaem();
                driver.SaveSettings();
                driver.OpenValve();
                driver.CloseValve();
                driver.ReadStatus();
    }
}