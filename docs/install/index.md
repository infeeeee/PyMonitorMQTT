# Install

Currently you need Python 3.7 to run PyMonitorMQTT; standalone executable files will be available soon (you won't need to install manually Python and all the requirements).


You can install Python 3.7 [here](https://www.python.org/downloads/).

### Install PIP

To install required packages you need [pip](https://www.makeuseof.com/tag/install-pip-for-python/)

### Python dependencies

To install dependencies all together, you only have to type in your terminal
```
python3 -m pip install -r requirements.txt
```

### Windows dependencies

In addition, to get CPU temperature from Windows you need:
* wmi (module from pip): `python3 -m pip install wmi`
* Open Hardware Monitor (external software). [Download it](https://openhardwaremonitor.org/downloads/)

### Linux dependencies

Install all dependencies on debian based linux with this command:

```shell
sudo apt install wireless-tools brightnessctl
```

#### iwconfig

`iwconfig` is sometimes installed to `/sbin` so you need to be root to run it. You can circumwent this limitation by linking it to your user bin directory:

```shell
sudo ln -s `sudo which iwconfig` /usr/local/bin/iwconfig
```

Restart PyMonitorMQTT, and it will report netwoek speeds.