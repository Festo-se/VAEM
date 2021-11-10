using driver;
using System;

class Example {
    static void Main(string[] args)
    {
        {
            VaemDriver driver = new VaemDriver("192.168.178.1", 502);
            driver.ConfigureVaem();
            driver.ConfigureValves(new int[] {500,0,0,0,0,0,0,0});
            
            for (int i = 0; i < 5; i++)
            {
                Thread.Sleep(1000);
                driver.ReadStatus();
                driver.ClearError();
                driver.ReadStatus();
                driver.ConfigureValves(new int[] {500,0,0,0,0,0,0,0});
                Thread.Sleep(1000);
                driver.OpenValve();
            }
        }
    }
}
