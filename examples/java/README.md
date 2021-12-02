# ☕ Java Driver
<img src="https://user-images.githubusercontent.com/71296226/134033531-ce6c1238-aa46-43da-8d6a-9cd36d30a62b.png" alt="alt text" width="500" height="300">

![GitHub last commit](https://img.shields.io/github/last-commit/jhynes94/vaem)

## 💬 Language
* Java 11.0.10

## 📚 Required Libraries
* <img src="https://a.fsdn.com/allura/p/easymodbustcp/icon?1609423069?&w=90" alt="alt text" width="30" height="30">[ EasyModbusTCP v2.8](https://sourceforge.net/projects/easymodbustcp-udp-java/#focus)

## 📜 VaemDriver Arguments
* ```String host``` - host IP for tcp/ip (ex. 192.168.0.XXX)
* ```int port``` - TCP port number for tcp/ip (ex. 502)

## Example Code
### 🚀 Start
* Creates a new ```Vaem``` driver object (```host IP```, ```tcp/ip port```)
* Initializes and connects to the ```VAEM```
* Selects valve 1 and sets the opening time to 500 ms

![image](https://user-images.githubusercontent.com/71296226/144478597-3c35978b-2b56-4604-b7a2-b24c9d6df31f.png)

### ♾️ Loop
* While loop that repeatedly opens and closes valve 1
* Reads the status of the ```VAEM``` before and after opening the valve
* Waits one second between opening and closing, vice versa

![image](https://user-images.githubusercontent.com/71296226/144478658-ee81f0c7-8856-492a-997d-73b3eee712b3.png)

### 🚧 Constructor
* Creates a new ```Modbus Client``` with the given ```host IP address``` and ```port number```
* Sets the clients ```slave ID``` to "0"
* Attempts to connect to the client

![image](https://user-images.githubusercontent.com/71296226/135158001-1dc6e290-e8ea-4abb-b021-644398d4ff40.png)

### ✔️ Initialization
* Sets the operating mode of the device to 1 using a write operation
* Reads back the current operating mode using a read operation
* ```VAEM``` is fully initialized and connected

![image](https://user-images.githubusercontent.com/71296226/135158394-871868cf-e385-42ed-a0b2-8dfa10b7670a.png)

## 🧑‍💻Interface
- [x] selectValve(int valve_id);
- [x] deselectValve(int valve_id);
- [x] setOpeningTime(int valve_id, int opening_time);
- [X] openValve();
- [x] closeValve();
- [x] readStatus();
- [x] clearError();
- [x] saveSettings();

## Author
|Name          | Email                      | GitHub         |
| ------------ | -------------------------  | -------------- |
| Jared Raines | raines.j@northeastern.edu  | @rainesjared   |
