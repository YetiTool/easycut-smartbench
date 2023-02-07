from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from asmcnc.apps.upgrade_app.upgrade_complete import UpgradeComplete

Builder.load_string("""
<UpgradeAppHome>:
    error_label:error_label
    context_label_1:context_label_1
    context_label_2:context_label_2
    qr_code_img:qr_code_img
    unlock_code_input:unlock_code_input
    serial_hint_label:serial_hint_label

    BoxLayout:
        orientation: 'vertical'
        
        BoxLayout:
            orientation: 'horizontal'
            size_hint: None, None
            width: dp(800)
            height: dp(50)
            
            canvas:
                Color:
                    rgba: hex('#1976d2')
                Rectangle:
                    size: self.size
                    pos: self.pos
            
            BoxLayout:
                size_hint: None, None
                width: dp(50)
                height: dp(50)
            
            Label:
                text: 'Upgrading to PrecisionPro +'
                halign: 'center'
                valign: 'middle'
                font_size: dp(28)
                text_size: self.size
                width: dp(200)
                height: dp(50)
                
            ClickableImage:
                source: 'asmcnc/apps/shapeCutter_app/img/exit_icon.png'
                halign: 'right'
                size_hint: None, None
                width: dp(50)
                height: dp(50)
                on_press: root.exit_app()
                
        BoxLayout:
            orientation: 'vertical'
            padding: [0, dp(30), 0, 0]
            
            canvas: 
                Color:
                    rgba: hex('f9f9f9ff')
                Rectangle:
                    size: self.size
                    pos: self.pos
                    
            BoxLayout:
                orientation: 'vertical'
                
                Label:
                    text: '1. Plug in your SC2 Spindle motor (both power and data cable)'
                    color: 0, 0, 0, 1
                    font_size: dp(16)
                    
                Label:
                    text: '2. Type in your upgrade code below'
                    color: 0, 0, 0, 1
                    font_size: dp(16)
                    
                Label:
                    text: '3. Press the "Enter" key on the keyboard'
                    color: 0, 0, 0, 1
                    font_size: dp(16)
            
            Label:
                id: serial_hint_label
                text: 'Your spindle serial number is: '
                color: 0, 0, 0, 1
            
            BoxLayout:
                padding: [dp(200), 0, 0, 0]
                
                TextInput:
                    id: unlock_code_input
                    multiline: False
                    valign: 'middle'
                    halign: 'center'
                    size_hint: None, None
                    font_size: dp(30)
                    height: dp(50)
                    width: dp(400)
                    on_text_validate: root.on_input_enter()
            
            Label:
                id: error_label
                text: 'Upgrade code incorrect, please check and try again.'
                color: 1, 0, 0, 1
                font_size: dp(18)
                halign: 'center'
                opacity: 0
                
            Label:
                id: context_label_1
                text: 'This app allows you to upgrade your SmartBench v1.3 PrecisionPro to a PrecisionPro +.'
                color: 0, 0, 0, 1
                halign: 'center'
                font_size: dp(16)
                
            Label:
                id: context_label_2
                text: 'For more information on upgrades, please contact your place or purchase or visit www.yetitool.com'
                color: 0, 0, 0, 1
                halign: 'center'
                font_size: dp(16)
            
            BoxLayout:
                padding: [dp(360), dp(25), 0, 0]
                size_hint_y: None
                height: dp(90)
                Image:
                    id: qr_code_img
                    source: 'asmcnc/apps/upgrade_app/img/qr_code.png'
                    size_hint: None, None
                    width: dp(80)
                    height: dp(80)
                    
            Label:
                text: ''
                size_hint: None, None
                height: dp(10)
""")

from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.image import Image


class ClickableImage(ButtonBehavior, Image):
    def on_press(self):
        pass


def get_correct_unlock_code(serial):
    try:
        return str(hex((serial + 42) * 10000))[2:]
    except TypeError:
        return 1


class UpgradeAppHome(Screen):
    activated = False

    def __init__(self, **kwargs):
        super(UpgradeAppHome, self).__init__(**kwargs)

        self.sm = kwargs['screen_manager']
        self.m = kwargs['machine']
        self.l = kwargs['localization']

        self.poll_for_spindle = Clock.schedule_interval(self.poll_for_spindle, 10)

    def exit_app(self):
        self.sm.remove_widget(self)
        self.sm.current = 'lobby'

    def poll_for_spindle(self, dt):
        if self.m.s.spindle_serial_number is not None and self.m.s.spindle_serial_number != -999:
            self.poll_for_spindle.cancel()
            self.get_spindle_serial()

    def on_enter(self):
        self.m.send_any_gcode_command('$51=1')
        self.get_spindle_serial()

    def on_leave(self):
        if not self.activated:
            self.m.send_any_gcode_command('$51=0')

    def show_verifying(self):
        self.error_label.opacity = 0
        self.context_label_1.text = 'Verifying...'
        self.context_label_1.font_size = '30dp'
        self.context_label_2.opacity = 0
        self.qr_code_img.opacity = 0

    def check_unlock_code(self):
        serial = self.m.s.spindle_serial_number

        if serial is None or serial is -999:
            self.show_failed_to_get_spindle()
            return

        correct_unlock_code = get_correct_unlock_code(serial)
        entered_unlock_code = self.unlock_code_input.text.lower().replace('o', '0')

        if correct_unlock_code is None:
            self.show_failed_to_get_spindle()
            return

        if correct_unlock_code == entered_unlock_code:
            self.activate_pro_plus()
        else:
            self.show_wrong_code_input()

    def show_wrong_code_input(self):
        self.error_label.text = 'Upgrade code incorrect, please check and try again.'
        self.error_label.opacity = 1
        self.context_label_2.opacity = 0
        self.qr_code_img.opacity = 1
        self.unlock_code_input.color = [1, 0, 0, 1]
        self.context_label_1.font_size = '16dp'
        self.context_label_1.text = "If the problem persists, please submit a support ticket: www.yetitool.com/submit-a-ticket\nSC2 detected. Quote spindle serial number: '%s'" % str(self.m.s.spindle_serial_number)

    def show_failed_to_get_spindle(self):
        self.error_label.text = 'No SC2 detected. Check your spindle and your connections.'
        self.error_label.opacity = 1
        self.context_label_2.opacity = 0
        self.qr_code_img.opacity = 1
        self.unlock_code_input.color = [1, 0, 0, 1]
        self.context_label_1.font_size = '16dp'
        self.context_label_1.text = "If the problem persists, please submit a support ticket: www.yetitool.com/submit-a-ticket\nSC2 detected. Quote error 'No SC2 detected'."

    def create_pro_plus_file(self):
        with open('../../proplus.txt', 'w+'):
            pass

    def add_upgrade_complete_screen(self):
        if not self.sm.has_screen('upgrade_complete'):
            upgrade_complete = UpgradeComplete(name='upgrade_complete', screen_manager=self.sm, machine=self.m,
                                               localization=self.l)
            self.sm.add_widget(upgrade_complete)

    def activate_pro_plus(self):
        self.add_upgrade_complete_screen()
        self.sm.current = 'upgrade_complete'
        self.create_pro_plus_file()

    def get_spindle_serial(self):
        self.m.s.write_command('M3 S0')
        Clock.schedule_once(
            lambda dt: self.m.s.write_protocol(self.m.p.GetDigitalSpindleInfo(), "GET DIGITAL SPINDLE INFO"), 0.2)
        Clock.schedule_once(lambda dt: self.m.s.write_command('M5'), 0.25)
        self.serial_hint_label.text = 'Your spindle serial number is: ' + str(self.m.s.spindle_serial_number or 'N/A')

    def on_input_enter(self):
        self.show_verifying()
        self.get_spindle_serial()
        Clock.schedule_once(lambda dt: self.check_unlock_code(), 0.5)
