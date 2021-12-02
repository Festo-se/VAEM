using System.Threading;
using VaemCSharpDriver.driver;

namespace VaemCSharpDriver
{
    class Example
    {
        static void Main(string[] args)
        {
            {
                VaemDriver driver = new VaemDriver("192.168.0.220", 502);
                driver.SelectValve(1);
                driver.SetOpeningTime(1, 500);

                for (int i = 0; i < 5; i++)
                {
                    driver.CloseValve();
                    Thread.Sleep(1000);
                    driver.ReadStatus();
                    driver.ClearError();
                    driver.ReadStatus();
                    driver.OpenValve();
                    Thread.Sleep(1000);
                }
            }
        }
    }
}
