from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from asmcnc.apps.upgrade_app.popups.help_popup import HelpPopup
from asmcnc.apps.upgrade_app.upgrade_complete import UpgradeComplete

Builder.load_string("""
<UpgradeAppHome>:
    unlock_code:unlock_code
    error_label:error_label
    help_button:help_button
    exit_button:exit_button

    BoxLayout:
        orientation: 'vertical'
        spacing: 5

        canvas:
            Color:
                rgba: hex('##e5e5e5')
            Rectangle:
                size: self.size
                pos: self.pos
                
        BoxLayout:
            orientation: 'horizontal'
            size_hint: None, None
            width: dp(800)
            height: dp(50)
            
            ClickableImage:
                id: exit_button
                source: "asmcnc/apps/shapeCutter_app/img/exit_cross.png"
                size_hint: None, None
                width: dp(50)
                height: dp(50)
                on_press: root.exit_app()
            
            AnchorLayout:
                anchor_x: 'right'
                ClickableImage:
                    id: help_button
                    source: "./asmcnc/skavaUI/img/help_btn_orange_round.png"
                    size_hint: None, None
                    width: dp(50)
                    height: dp(50)
                    on_press: root.open_help()
        
        BoxLayout:
            orientation: 'vertical'
            padding: [0,0,0,dp(200)]
            
            Label:
                text: "This app allows you to upgrade your SmartBench v1.3 [b]PrecisionPro[/b] to a [b]PrecisionPro +[/b].\\nYou will have needed to purchase an upgrade package. For more information on the upgrade,\\n please visit www.yetitool.com/PRODUCTS/upgrades"
                halign: "center"
                markup: True
                color: 0,0,0,1
                size_hint_y: None
                font_size: dp(16)
        
            Label:
                text: "Enter your unlock code:"
                halign: "center"
                markup: True
                color: 0,0,0,1
                size_hint_y: None
                id: error_label
                font_size: dp(16)
            
            BoxLayout:
                padding: [dp(200), 0, 0, 0]
                TextInput:
                    id: unlock_code
                    multiline: False
                    font_size: dp(30)
                    color: 0,0,0,1  
                    size_hint: None, None
                    height: dp(50)
                    width: dp(400)
                    on_text_validate: root.check_unlock_code()
""")

from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.image import Image


class ClickableImage(ButtonBehavior, Image):
    def on_press(self):
        pass


class UpgradeAppHome(Screen):
    serial = None
    valid_unlock_code = None

    def __init__(self, **kwargs):
        super(UpgradeAppHome, self).__init__(**kwargs)

        self.sm = kwargs['screen_manager']
        self.m = kwargs['machine']
        self.l = kwargs['localization']
        self.localize()

    def localize(self):
        pass

    def open_help(self):
        HelpPopup()

    def exit_app(self):
        self.sm.current = 'lobby'

    def on_enter(self):
        self.m.s.write_command('M3 S0')
        Clock.schedule_once(lambda dt: self.get_serial_and_calculate_unlock_code(), 1)
        Clock.schedule_once(lambda dt: self.m.s.write_command('M5'))

    def get_serial_and_calculate_unlock_code(self):
        self.serial = self.m.s.spindle_serial_number or 1

        self.valid_unlock_code = str(hex((self.serial + 42) * 10000))[2:]

    def create_pro_plus_file(self):
        with open('../../proplus.txt', 'w+'):
            pass

    def go_to_complete_screen(self):
        if self.sm.has_screen('upgrade_complete'):
            self.sm.current = 'upgrade_complete'
            return

        complete_screen = UpgradeComplete(name='upgrade_complete', screen_manager=self.sm,
                                          machine=self.m, localization=self.l)
        self.sm.add_widget(complete_screen)
        self.sm.current = 'upgrade_complete'

    def activate_pro_plus(self):
        self.m.send_any_gcode_command('$51=1')
        self.create_pro_plus_file()
        self.go_to_complete_screen()

    def check_unlock_code(self):
        if self.unlock_code.text.lower() == str(self.valid_unlock_code):
            self.activate_pro_plus()
            return

        self.error_label.text = "[color=FF0000]Unlock code incorrect, please check and try again.[/color]\n If the " \
                                "problem persists, please submit a support ticket: www.yetitool.com/submit-a-ticket " \
                                "\nquoting spindle serial number: " + str(self.serial)
