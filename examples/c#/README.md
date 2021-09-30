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
* Configures the 8 valve channels using the opening time values in ```valveData```

![image](https://user-images.githubusercontent.com/71296226/135155686-feca88c9-1b54-4b6f-9cfd-cfbdbf575b6c.png)

### ♾️ Loop
* While loop that repeatedly opens and closes valve 1
* Reads the status of the ```VAEM``` after opening the valve
* Waits one second between opening and closing, vice versa

![image](https://user-images.githubusercontent.com/71296226/135160108-3d8ed286-8047-4b7d-ae73-f30f310ecce7.png)

### 🚧 Constructor
* Creates a new ```Modbus Client``` with the given ```host IP address``` and ```port number```
* Sets the clients ```slave ID``` to "0"
* Attempts to connect to the client

![image](https://user-images.githubusercontent.com/71296226/135158001-1dc6e290-e8ea-4abb-b021-644398d4ff40.png)

### ✔️ Initialization
* Sets the operating mode of the device to 1 using a basic write operation
* Reads back the current operating mode using a basic read operation
* ```VAEM``` is fully initialized and connected

![image](https://user-images.githubusercontent.com/71296226/135158394-871868cf-e385-42ed-a0b2-8dfa10b7670a.png)

## Author
|Name          | Email                      | GitHub         |
| ------------ | -------------------------  | -------------- |
| John Alessio | alessio.j@northeastern.edu | @jalesssio     |
