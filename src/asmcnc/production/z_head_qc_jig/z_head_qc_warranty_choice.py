from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.clock import Clock
import traceback


Builder.load_string("""
<ZHeadWarrantyChoice>:

    fw_version_label : fw_version_label

    BoxLayout:
        orientation: 'vertical'

        GridLayout:
            size: self.parent.size
            pos: self.parent.pos
            cols: 1
            rows: 3

            GridLayout: 
                rows: 2

                Label: 
                    text: 'How old is this Z Head?'
                    color: 1,1,1,1
                    text_size: self.size
                    markup: 'True'
                    halign: 'center'
                    valign: 'bottom'
                    font_size: dp(30)

                Label: 
                    id: fw_version_label
                    text: 'Detecting FW version...'
                    color: 1,1,1,1
                    text_size: self.size
                    markup: 'True'
                    halign: 'center'
                    valign: 'middle'
                    font_size: dp(24)

            GridLayout: 
                cols: 2

                Button:
                    text: root.after_label
                    font_size: dp(20)
                    color: 1,1,1,1
                    text_size: self.size
                    markup: 'True'
                    halign: 'center'
                    valign: 'middle'
                    on_press: root.after_apr21()

                Button:
                    text: root.before_label
                    font_size: dp(20)
                    color: 1,1,1,1
                    text_size: self.size
                    markup: 'True'
                    halign: 'center'
                    valign: 'middle'
                    on_press: root.before_apr21()

            Button: 
                text: '<<< Back'
                font_size: dp(20)
                on_press: root.back_to_home()

""")


class ZHeadWarrantyChoice(Screen):

    after_label = "Made AFTER April 2021\n\nFW version v1.3.6 or above"
    before_label = "Made BEFORE April 2021\n\nFW version v1.1.2 or below"

    poll_for_fw = None


    def __init__(self, **kwargs):
        super(ZHeadWarrantyChoice, self).__init__(**kwargs)

        self.sm = kwargs['sm']
        self.m = kwargs['m']

    def on_enter(self):
        self.poll_for_fw = Clock.schedule_once(self.scrape_fw_version, 1)

    def scrape_fw_version(self, dt):
        try:
            self.fw_version_label.text = "Detected FW version: " + str((str(self.m.s.fw_version)).split('; HW')[0])
            if self.poll_for_fw != None: Clock.unschedule(self.poll_for_fw)
        
        except:
            print("could not detect fw/update label")
            print(traceback.format_ex())

    def after_apr21(self):
        self.sm.current = 'qcW136'

    def before_apr21(self):
        self.sm.current = 'qcW112'

    def back_to_home(self):
        self.sm.current = 'qchome'