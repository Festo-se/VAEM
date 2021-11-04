
<p align="right">
  <img src="https://user-images.githubusercontent.com/71296226/132049416-fc92dde2-d4fc-4d59-89e9-3aef004c9ee8.png" alt="alt text" width="200" height="30">
</p>

# **VAEM** 8️⃣ 🎮
## **8-Channel Valve Controller**

<p align="center">
  <img src="https://user-images.githubusercontent.com/71296226/135117973-92878832-2fb8-44da-8a9a-5b8161466005.png" alt="alt text" width="400" height="300">
</p>

![GitHub](https://img.shields.io/badge/Festo-Automation-0091dc/?style=for-the-badge&color=0091dc)
![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/jhynes94/VAEM?include_prereleases)
![GitHub language count](https://img.shields.io/github/languages/count/jhynes94/VAEM)
![GitHub](https://img.shields.io/github/license/jhynes94/VAEM)

* The [Festo](https://www.festo.com/us/en/?fwacid=9c792b0a20f1ab8d&gclid=Cj0KCQjwm9yJBhDTARIsABKIcGb7XGaLbJ-ljqb2bccWRPNZg1aE6mirUx0hWMCG82ycezodZ9I4ZTgaAqOYEALw_wcB) designed valve control module ```VAEM``` makes precise switching of solenoid valves easier than ever in any ```Festo``` systems or dispense applications.
* Up to 8 channels can be parameterised individually.
* A time resolution of only 0.2 ms and the control of the valves via current – not voltage – enable extremely high precision.
* The holding current reduction saves energy and minimizes heat input.
* Communication Protocol: [Modbus TCP/IP](https://en.wikipedia.org/wiki/Modbus#Modbus_TCP_frame_format_(primarily_used_on_Ethernet_networks)).

## Table of Contents

- [About](#about)
- [Links](#links)
- [GUI](#gui)
- [Driver Languages](#driver-languages)
- [Methods](#methods)
- [Diagram](#diagram)
- [Contributors](#contributors)
- [Capabilities](#current-version-capabilities)

## About
* This is an ```open software project``` which provides ```VAEM``` customers and users with a wide array of driver templates in different coding languages to allow for quick and easy adaptability of the ```Festo``` valve control module to any system, project, or environment. Listed below are the current languages provided along with the methods that each driver provides to the user.

## Links
### [:shopping_cart:: Product Page](https://www.festo.com/us/en/a/8088772/?q=VAEM~:festoSortOrderScored)
### [:receipt:: Operating Instructions](https://www.festo.com/net/SupportPortal/Files/716358/VAEM-V-S8EPRS2_operating-instr_2021-10a_8144872g1.pdf)
### [:old_key:: Support Portal](https://www.festo.com/net/en-in_in/SupportPortal/default.aspx?tab=0&q=8088772)
### [:desktop_computer:: GUI](https://www.festo.com/net/en-in_in/SupportPortal/default.aspx?q=8088772&tab=4&s=t#result)

## GUI
<p align="center">
  <img src="https://user-images.githubusercontent.com/71296226/136092356-8481541c-4a9f-4f75-a6a9-5d0b88f3e922.PNG" alt="alt text" width="800" height="700">
</p>

* 🔌 **CONNECT** the VAEM to your PC using an Ethernet cable and click the scan button.
(If the VAEM is found, press the connect button, else your gateway may have to be changed)
* 🕹️ **CONTROL** the eight channels of the VAEM.
* 🔬 **ANALYZE** data including the nominal current versus time.
* ❕ ❕ **STATUSWORD** displays the individual statusword bits and allows for basic read/write operations.
* ℹ️ **SYSTEMINFO** provides firmware and product number information.
* 📶 **ETHERNET** allows the user to change the host IP, port, and timeout.

## Driver Languages
* <img src="https://icons.iconarchive.com/icons/papirus-team/papirus-apps/256/python-icon.png" alt="alt text" width="40" height="40">[  Python](/examples/python)
* <img src="https://images.vexels.com/media/users/3/166401/isolated/lists/b82aa7ac3f736dd78570dd3fa3fa9e24-java-programming-language-icon.png" alt="alt text" width="40" height="40">  [  Java](/examples/java)
* <img src="https://camo.githubusercontent.com/8d56e87edf99e89bfc457cd62462e0b7aae19e6b197b1df5c542d474d8d76f81/68747470733a2f2f646576656c6f7065722e6665646f726170726f6a6563742e6f72672f7374617469632f6c6f676f2f6373686172702e706e67" alt="alt text" width="30" height="30">[  .NET/C#](/examples/c%23)

## Methods
* **:toolbox: configureValves** -
  * ```Purpose:```      Configures the valve opening times of all eight channels, with 0 turning the channel off
  * ```Value Ranges:``` openingTimes >= 0
  * ```Arguments:```    int[8] openingTimes (ms)
  * ```Returns:```      void

* **💧: openValve** -
  * ```Purpose:```      Opens the valves connected to the initialized channels
  * ```Value Ranges:``` NONE
  * ```Arguments:```    void
  * ```Returns:```      void
* **🚪: closeValve** -
  * ```Purpose:```      Closes the valves connected to the initialized channels
  * ```Value Ranges:``` NONE
  * ```Arguments:```    void
  * ```Returns:```      void
  
* **:books: readStatus** -
  * ```Purpose:```      Read the VAEM status, error code, readiness, operating mode, and eight valve status bits (in order)
  * ```Value Ranges:``` NONE
  * ```Arguments:```    void
  * ```Returns:```      void

* **:soap: clearError** -
  * ```Purpose:```      Clears (resets) the error bit on the VAEM
  * ```Value Ranges:``` NONE
  * ```Arguments:```    void
  * ```Returns:```      void

* **:floppy_disk: saveSettings** -
  * ```Purpose:```      Save the current valve configuration upon restart
  * ```Value Ranges:``` NONE
  * ```Arguments:```    void
  * ```Returns:```      void

## Diagram
![festo_vaem_pic](https://user-images.githubusercontent.com/71296226/135151696-b2e39274-deb0-4d43-8371-ba793b44f638.PNG)

## Current Version Capabilities
- [x] Modbus TCP/IP over Ethernet
- [ ] Serial Ascii over RS232
- [x] Open all 8 valve channels
- [x] Close all 8 valve channels
- [x] Read the current device status
- [x] Configure the valves/channels

## Contributors
|Name                 | Email                         | GitHub         |
| ------------        | -------------------------     | -------------- |
| John Alessio        | alessio.j@northeastern.edu    | @jalesssio     |
| Justin Hynes-Bruell | justin.hynes-bruell@festo.com | @jhynes94      |
| Milen Kolev         | milen.kolev@festo.com         | @MKollev       |
| Jared Raines        | raines.j@northeastern.edu     | @rainesjared   |
