# 🐍 Python Driver
<img src="https://www.python.org/static/community_logos/python-logo-master-v3-TM-flattened.png" alt="alt text" width="600" height="250">

![GitHub last commit](https://img.shields.io/github/last-commit/jhynes94/vaem)

## 💬 Language
* Python 3.7

## 📚 Required Libraries
* <img src="http://domoticx.com/wp-content/uploads/2017/09/modbus-logo-300x96.png" alt="alt text" width="60" height="30">[ PyModbus v2.5.2](http://riptideio.github.io/pymodbus/)
* <img src="https://pythonhosted.org/pyserial/_static/pyserial.png" alt="alt text" width="60" height="30">[ PySerial v3.5](https://pythonhosted.org/pyserial/)

## 📜 PGVA Arguments
* ```string ip``` - host IP for tcp/ip (ex. 192.168.0.XXX)
* ```int port``` - TCP port number for tcp/ip (ex. 502)
* ```int slave_id``` - unit or slave Modbus identification number for the device (ex. 0)

## Example Code
### 🚀 Start
* Creates a new ```VAEM``` driver object (```ip```, ```port```, ```slave_id```, ```logger```) and attempts to connect
* Initializes the device. selects valve 1, and sets the opening time to 500 ms 

 ![image](https://user-images.githubusercontent.com/71296226/144479345-8e52da72-0d90-4ca2-b377-d864d849079f.png)

### ♾️ Loop
* While loop that repeatedly opens and closes valve 1
* Reads the status of the ```VAEM``` after opening the valve
* Waits one second between opening and closing, vice versa
* Checks if there is an error and clears it if true

![image](https://user-images.githubusercontent.com/71296226/144479368-e41411fd-e076-4b01-ad46-8c29443fbbc8.png)

### 🚧 Constructor
* Sets the ```TcpClient``` with the given host ip and port from ```config```
* Attempts three times to connect to the client
* Throws an error if the code was not able to connect to the device

![image](https://user-images.githubusercontent.com/71296226/135303620-42ddb615-ba3f-4cf3-ac42-1c1cdb01bf47.png)

### ✔️ Initialization
* Sets the operating mode to ```OpMode1``` using a write operation
* Clears any errors on the device using a write operation

(```constructFrame``` builds the message to be sent to the device and ```transfer``` sends it)

![image](https://user-images.githubusercontent.com/71296226/135303699-c066e66c-01a1-43dc-a231-89893b727951.png)

## 🧑‍💻Interface
- [x] selectValve(int valve_id)
- [x] deselectValve(int valve_id)
- [x] setOpeningTime(int valve_id, int opening_time)
- [X] openValve()
- [x] closeValve(self)
- [x] readStatus()
- [x] clearError()
- [x] saveSettings()

## Author
|Name          | Email                     | GitHub         |
| ------------ | ------------------------- | -------------- |
| Milen Kolev  | milen.kolev@festo.com     | @MKollev       |
