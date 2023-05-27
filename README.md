# Singapore Bus Stop Arrival Timing (Telegram Bot)

The code in this repository makes use of Land Transport Authority's (LTA) DataMall Dynamic API to call the bus arrival times for a specified bus stop.

To make calls with the DataMall API, you will need to sign up to use the service.

For this version of the code, it is intended to be used on devices such as:

* Raspberry Pi (the Pico version does not apply here)
* Devices that can run Python (Mainly computers)

For the MicroPython version, please view [here](https://github.com/TwelfthDoctor1/BusSvcDisplay-micropython).

Note: Changes displayed here will take longer to show up on the Micropython version, in terms of suitability, time, etc.

## Usage

Before running the code, the following modules are required:
* python-dotenv
* *pyTelegramBotAPI

You also need to setup a `RefKey.env` file with the following values:

```dotenv
API_KEY_LTA=XXX
BOT_KEY=XXX
```

**Remember to replace `XXX` with the actual API Key.**

To run the Python version of the project, run main.py.

## Running the Code

You can choose to run either the UI or Console Version. Both versions will request on a Bus Stop Code and an Explicit Services (optional).

### Bus Stop Code

The Bus Stop Code is a unique 5-digit code where it refers to a bus stop in a certain location. You can find at the Bus Stop, Google Maps, etc.

#### Terminology

The first 2 digits typically refers to a group of locations ranging from 0 to 9, where it will specify a town. e.g. 77 -> Pasir Ris, 84 -> Bedok

The next 2 digits are not inherently clear on its formation but the very last digit can end in 1, 2, 3, 7, 8 or 9.

**Bus Interchanges/Terminals typically have this code: XX009**

You can read up on these 2 articles on Bus Stop Code information:
* https://landtransportguru.net/bus-stops/
* https://web.archive.org/web/20181107233311/http://www.sbstransit.com.sg/iris3/busstopno.aspx (Original site no longer available, but archive remains)

### Explicit Services

Explicit Services mean the Bus Services that you specifically want to see from a list of services offered in a bus stop.

e.g. You want Services 12 and 107 from Bus Stop 01319 (Lavender Stn A/ICA Building) which has 2, 12, 33, 1107, 107M and 133

This feature will allow you to filter out only those services that you want.

**Note: Should you not require this function, you will need to leave the option blank when requested, otherwise services will not show up. (empty test check)**

#### Minor Explanation

In the Bus Timings API, it is possible to request timing of one service in a bus stop, however due to that limitation and instead of using multiple requests, filtering is used instead.

#### Output

Both versions will output a similar structure after input and processing:
* Arrival Times (XX min @ XX:XX:XX)
* Seating/Load
* Bus Type
* Visit Number (only useful or certain buses)
* Estimated Duration (dependent of up to 3 buses)

Note: Should buses have no arrival timing, they will not be displayed at the time of request due to the API. They may reappear at a later time.

The Visit Number is useful on for buses where they pass by a bus stop twice. An example will be feeder buses if they have 2 loops such as 291 & 293 on Tampines and 358 and 359 in Pasir Ris.

As for the Estimated Duration, it is based on the following:
* Should all 3 buses are on 1st Visit or less thereof with Not in Service then estimation is acquired based on mean (for 1 Timing and 2 Not in Service, duration = first bus timing)
* Should there be Visits 1 and 2, buses are split based on visits and above rule is applied for both durations
