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

Restart PyMonitorMQTT, and it will report network speeds.

## Use venv

You can install PyMonitorMQTT to a [python venv](https://docs.python.org/3/library/venv.html) (virtual environment). This way the packages required by this program can't mess up your other python based tools, and if you want to reinstall, by deleting the folder you will also remove all dependencies. Nowadays this is the recommended way to install python apps with a lot of dependencies.

Python venv is available to Linux, Windows and Mac.

### Full install and configuration commands on Linux

Example commands on a fresh debian installation:

```shell
sudo apt install git wireless-tools brightnessctl python3-venv python3-dev
git clone https://github.com/riccardo-briccola/PyMonitorMQTT
cd PyMonitorMQTT
python3 -m venv .
source ./bin/activate
python3 -m pip install -r requirements-linux.txt
```

Configuration: ([Documentation](https://riccardo-briccola.github.io/PyMonitorMQTT/configuration/))

```shell
cp configuration.yaml.example configuration.yaml
nano configuration.yaml
```

Test run:

```shell
# Activate the venv:
source ./bin/activate
./main.py
# To deactivate the venv:
deactivate
```

Create systemd service:

*TODO*

