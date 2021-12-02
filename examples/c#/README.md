# 🪓 C#/.NET Driver
<img src="https://miro.medium.com/max/2000/1*MfOHvI5b1XZKYTXIAKY7PQ.png" alt="alt text" width="800" height="300">

![GitHub last commit](https://img.shields.io/github/last-commit/jhynes94/vaem)

## 💬 Language and Framework
* C# 7.3
* .NETFramework v4.7.2

## 📚 Required Libraries
* <img src="https://a.fsdn.com/allura/p/easymodbustcp/icon?1609423069?&w=90" alt="alt text" width="30" height="30">[ EasyModbusTCP v5.6.0](https://sourceforge.net/projects/easymodbustcp/#focus)

## 📜 VaemDriver Arguments
* ```String ip``` - host IP for tcp/ip (ex. 192.168.0.XXX)
* ```int port``` - TCP port number for tcp/ip (ex. 502)

## Example Code
### 🚀 Start
* Creates a new ```Vaem``` driver object (```host IP```, ```tcp/ip port```)
* Initializes and connects to the ```VAEM```
* Selects valve 1
* Configures valve 1 with an opening time of 500 ms

![image](https://user-images.githubusercontent.com/71296226/144477466-56f7817d-a109-435c-91ac-a1c43c692656.png)

### ♾️ Loop
* While loop that repeatedly opens and closes all valves five times
* Closes all selected valves and waits for 1 second
* Reads the status of the VAEM before and after clearing all errors
* Open all selected valves and waits for 1 second

![image](https://user-images.githubusercontent.com/71296226/144477319-a804d5d1-721c-432b-9eeb-e12e0ea1b7b7.png)

### 🚧 Constructor
* Creates a new ```Modbus Client``` with the given ```host IP address``` and ```port number```
* Attempts to connect to the client three times if needed
* If connected, initialize the ```VAEM```

![image](https://user-images.githubusercontent.com/71296226/135522768-0ec3d901-47f7-43ed-84c1-5a7cabdc2bca.png)

### ✔️ Initialization
* Sets the operating mode of the device to 1 using a write operation
* Selects the valve connected to channel one with a write operation
* ```VAEM``` is fully initialized and connected

![image](https://user-images.githubusercontent.com/71296226/135523020-d68f2e8e-f1f4-42ff-bbb1-81ee7aca2fdc.png)

## 🧑‍💻Interface
- [ ] configureValves(int[] openingTimes);
- (configureVaem() selects all valves instead)
- [X] openValve();
- [x] closeValve();
- [x] readStatus();
- [ ] clearError();
- [x] saveSettings();


## Author
|Name          | Email                      | GitHub         |
| ------------ | -------------------------  | -------------- |
| John Alessio | alessio.j@northeastern.edu | @jalesssio     |
