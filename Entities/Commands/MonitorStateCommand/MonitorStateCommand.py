import subprocess
import ctypes
import os as sys_os
from Entities.Entity import Entity
from ctypes import *
import re

TOPIC = 'monitor_state'


class MonitorStateCommand(Entity):
    def Initialize(self):
        self.SubscribeToTopic(TOPIC)
        self.stopCommand = False
        self.stopSensor = False
        self.stateOff = False

    def PostInitialize(self):
        os = self.GetOS()

        # Sensor function settings
        if(os == self.consts.FIXED_VALUE_OS_WINDOWS):
            self.GetMonitorState_OS = self.GetMonitorState_Win
        elif(os == self.consts.FIXED_VALUE_OS_MACOS):
            self.GetMonitorState_OS = self.GetMonitorState_macOS
        elif(os == self.consts.FIXED_VALUE_OS_LINUX):
            self.GetMonitorState_OS = self.GetMonitorState_Linux
        else:
            self.Log(self.Logger.LOG_WARNING,
                     'Monitor state is not available for this operating system')
            self.stopSensor = True

        # Command function settings
        if(os == self.consts.FIXED_VALUE_OS_WINDOWS):
            self.SetMonitorState_OS = self.SetMonitorState_Win
        elif(os == self.consts.FIXED_VALUE_OS_MACOS):
            self.SetMonitorState_OS = self.SetMonitorState_macOS
        elif(os == self.consts.FIXED_VALUE_OS_LINUX):
            self.SetMonitorState_OS = self.SetMonitorState_Linux
        else:
            self.Log(self.Logger.LOG_WARNING,
                     'No monitor state command available for this operating system')
            self.stopCommand = True

    def Callback(self, message):
        state = message.payload.decode("utf-8")
        if not self.stopCommand:
            try:
                self.SetMonitorState_OS(state)
            except ValueError:  # Not int -> not a message for that function
                return
            except Exception as e:
                raise Exception("Error during monitorstate set: " + str(e))

            # Finally, tell the sensor to update and to send
            self.CallUpdate()
            self.lastSendingTime = None  # Force sensor to send immediately

    def Update(self):
        if not self.stopSensor:
            self.SetTopicValue(TOPIC, self.GetMonitorState_OS(),
                               self.ValueFormatter.TYPE_NONE)

    def SetMonitorState_Linux(self, value):
        if sys_os.environ.get('DISPLAY'):
            command = f'xset dpms force {value.lower()}'
            subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        else:
            raise Exception(
                'The Turn ON Monitors command is not available for this Linux Window System')

    def GetMonitorState_Linux(self):
        command = 'xset q '
        p = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        out = p.stdout.read().decode()
        p.communicate()
        st = re.findall('Monitor is (.{2,3})', out)[0].upper()
        return

    def GetOS(self):
        # Get OS from OsSensor and get temperature based on the os
        os = self.FindEntity('Os')
        if os:
            if not os.postinitializeState:  # I run this function in post initialize so the os sensor might not be ready
                os.CallPostInitialize()
            os.CallUpdate()
            return os.GetTopicValue()

    def ManageDiscoveryData(self, discovery_data):
        for data in discovery_data:
            data['expire_after'] = ""

        discovery_data[0]['payload']['state_topic'] = self.SelectTopic(
            TOPIC)
        discovery_data[0]['payload']['payload_on'] = self.consts.ON_STATE
        discovery_data[0]['payload']['payload_off'] = self.consts.OFF_STATE

        return discovery_data
