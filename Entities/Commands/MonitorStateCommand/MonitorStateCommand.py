import subprocess
import ctypes
import os as sys_os
from Entities.Entity import Entity
from ctypes import *
import re

IN_TOPIC = 'monitor_state/set'


class MonitorStateCommand(Entity):
    def Initialize(self):
        self.SubscribeToTopic(IN_TOPIC)
        self.stopCommand = False
        self.stopSensor = False
        self.stateOff = False

    def PostInitialize(self):
        os = self.GetOS()

        # Sensor function settings
        if(os == self.consts.FIXED_VALUE_OS_LINUX):
            self.GetMonitorState_OS = self.GetMonitorState_Linux
        # elif(os == self.consts.FIXED_VALUE_OS_WINDOWS):
        #     self.GetMonitorState_OS = self.GetMonitorState_Win
        # elif(os == self.consts.FIXED_VALUE_OS_MACOS):
        #     self.GetMonitorState_OS = self.GetMonitorState_macOS
        else:
            self.Log(self.Logger.LOG_WARNING,
                     'Monitor state is not available for this operating system')
            self.stopSensor = True

        # Command function settings
        if(os == self.consts.FIXED_VALUE_OS_LINUX):
            self.SetMonitorState_OS = self.SetMonitorState_Linux
        # elif(os == self.consts.FIXED_VALUE_OS_WINDOWS):
        #     self.SetMonitorState_OS = self.SetMonitorState_Win
        # elif(os == self.consts.FIXED_VALUE_OS_MACOS):
        #     self.SetMonitorState_OS = self.SetMonitorState_macOS
        else:
            self.Log(self.Logger.LOG_WARNING,
                     'No monitor state command available for this operating system')
            self.stopCommand = True

    def Callback(self, message):
        state = message.payload.decode("utf-8").lower()
        if not self.stopCommand:
            try:
                self.SetMonitorState_OS(state)
            except Exception as e:
                raise Exception("Error during monitorstate set: " + str(e))

            # Need some timeout on linux before getting the state,
            # so send state back manually:
            if state == 'on':
                send_state = self.consts.ON_STATE
            else:
                send_state = self.consts.OFF_STATE

            self.mqtt_client.SendTopicData(
                self.SelectTopic(self.STATE_TOPIC), send_state)

            self.lastSendingTime = None  # Force sensor to send immediately

    def Update(self):
        if not self.stopSensor:
            self.SendOnlineState()

    def SetMonitorState_Linux(self, value):
        if sys_os.environ.get('DISPLAY'):
            command = f'xset dpms force {value}'
            subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        else:
            raise Exception(
                'The Turn ON Monitors command is not available for this Linux Window System')

    def GetMonitorState_Linux(self):
        command = 'xset q'
        p = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        out = p.stdout.read().decode()
        p.communicate()
        st = re.findall('Monitor is (.{2,3})', out)[0].lower()
        return st

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

        self.SendOnlineState()

        discovery_data[0]['payload']['state_topic'] = self.SelectTopic(
            self.STATE_TOPIC)
        discovery_data[0]['payload']['command_topic'] = self.SelectTopic(
            IN_TOPIC)
        discovery_data[0]['payload']['payload_on'] = self.consts.ON_STATE
        discovery_data[0]['payload']['payload_off'] = self.consts.OFF_STATE

        return discovery_data

    STATE_TOPIC = 'monitor_state/state'

    def SendOnlineState(self, state=None):
        if self.GetMonitorState_OS() == 'on':
            self.mqtt_client.SendTopicData(
                self.SelectTopic(self.STATE_TOPIC), self.consts.ON_STATE)
        else:
            self.mqtt_client.SendTopicData(
                self.SelectTopic(self.STATE_TOPIC), self.consts.OFF_STATE)
