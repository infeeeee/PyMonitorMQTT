from Commands.Command import Command
import Logger

supports_win = True
try:
    import win10toast
except:
    supports_win = False


supports_unix = True
try:
    import wmi  # Only to get windows temperature
except:
    supports_unix = False


TOPIC = 'notify'

# If I haven't value for the notification I use these
DEFAULT_MESSAGE = 'Notification'
DEFAULT_TITLE = 'PyMonitorMQTT'
DEFAULT_DURATION = 10  # Seconds


class NotifyCommand(Command):
    def Initialize(self):
        self.SubscribeToTopic(self.GetTopic(TOPIC))

    # I need it here cause I have to check the right import for my OS (and I may not know the OS in Init function)
    def PostInitialize(self):
        self.os = self.GetOS()
        if self.os == 'Windows':
            if not supports_win:
                raise Exception(
                    'Notify not available, have you installed \'win10toast\' on pip ?')
        else:
            if not supports_unix:
                raise Exception(
                    'Notify not available, have you installed \'notify2\' on pip ?')

    def Callback(self, message):
        # TO DO
        # Convert the payload in a dict
        messageDict = ''
        try:
            messageDict = eval(message.payload.decode('utf-8'))
        except:
            pass  # No message or title in the payload

        # Priority for configuration content and title. If not set there, will try to find them in the payload

        # Look for notification content
        if 'message' in self.options:
            content = self.options['message']
        elif 'message' in messageDict:
            content = messageDict['message']
        else:
            content = DEFAULT_MESSAGE
            self.Log(Logger.LOG_WARNING,
                     'No message for the notification set in configuration or in the received payload')

        # Look for notification title
        if 'title' in self.options:
            title = self.options['title']
        elif 'title' in messageDict:
            title = messageDict['title']
        else:
            title = DEFAULT_TITLE

        # Look for notification duration
        if 'duration' in self.options:
            duration = self.options['duration']
        elif 'duration' in messageDict:
            duration = messageDict['duration']
        else:
            duration = DEFAULT_DURATION

        # Check only the os (if it's that os, it's supported because if it wasn't supported,
        # an execption would be thrown in post-inits)

        if self.os == 'Windows':
            toaster = win10toast.ToastNotifier()
            toaster.show_toast(
                title, content, duration=duration, threaded=False)

    def GetOS(self):
        # Get OS from OsSensor and get temperature based on the os
        os = self.FindSensor('Os')
        if os:
            os.Update()
            return os.GetTopicValue()
