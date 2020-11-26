'''
Log dam

BECAUSE IT'S A STACK OF LOGS C:

@author Letty
'''

from datetime import datetime
import os
from kivy.clock import Clock

dam_path = "/home/pi/smartbench_dam.txt"

class Beaver(object):

    dam = []

    def __init__(self):
        self.make_log("Start beaver...")
        Clock.schedule_interval(self.sustain_dam_list, 10)
        # Clock.schedule_interval(self.sustain_dam_file, 300)

    def make_log(self, message):
        timestamp = datetime.now()
        log = (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + str(message))
        self.add_to_dam(log)

    def add_to_dam(self, log):
        self.dam.append(log)
        print log
        os.system("sed -i \'1s/^/" + log + "\\n/ \' " + dam_path)

    def sustain_dam_list(self, dt):
        if len(self.dam) > 60:
            self.dam = self.dam[-60:]

# add sed truncating function
    def sustain_dam_file(self, dt):
       os.system(" sed -i \'20000001,$ d\' " + dam_path)