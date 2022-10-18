from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.clock import Clock
from asmcnc.comms.yeti_grbl_protocol.c_defines import *
from datetime import datetime

from asmcnc.skavaUI import widget_status_bar

Builder.load_string("""
<ZHeadPCBSetUpOutcome>:

    status_container : status_container

    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            orientation: 'vertical'
            size_hint_y: 0.92

            BoxLayout:
                orientation: 'horizontal'
                size_hint_y: 0.2

                Button:
                    text: '<<< Back'
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
                    padding: [dp(10),0]
                    on_press: root.go_back_to_pcb_setup()


                BoxLayout: 
                    orientation: 'horizontal'

            BoxLayout: 
                orientation: 'horizontal'
                size_hint_y: 0.6


            Button:
                on_press: 
                text: 'OK'
                font_size: dp(30)
                size_hint_y: 0.2
                on_press: root.go_to_qc_home()

        BoxLayout:
            size_hint_y: 0.08
            id: status_container 
            pos: self.pos
""")

def log(message):
    timestamp = datetime.now()
    print ('Z Head Connecting Screen: ' + timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + str(message))

class ZHeadPCBSetUpOutcome(Screen):

    def __init__(self, **kwargs):

        super(ZHeadPCBSetUpOutcome, self).__init__(**kwargs)

        self.sm = kwargs['sm']
        self.m = kwargs['m']

        # Green status bar
        self.status_bar_widget = widget_status_bar.StatusBar(machine=self.m, screen_manager=self.sm)
        self.status_container.add_widget(self.status_bar_widget)

    def go_to_qc_home(self):
        self.sm.current = "qchome"

    def go_back_to_pcb_setup(self):
        self.sm.current = "qcpcbsetup"        
