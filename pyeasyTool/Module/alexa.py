import base
import threading
from time import sleep
import os

class Alexa:
    def run(self):
        threading.Thread(target=base.monitor).start()
        sleep(1)
        os.system('''adb shell "adk-message-send 'voiceui_start_onboarding{client:\\"AVS\\"}'"''')
