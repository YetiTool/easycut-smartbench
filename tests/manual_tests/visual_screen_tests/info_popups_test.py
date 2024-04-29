"""
From the easycut folder: python -m tests.manual_tests.visual_screen_tests.info_popups_test
"""
import sys, os, textwrap

from asmcnc.comms.logging_system.logging_system import Logger

path_to_EC = os.getcwd()
sys.path.append('./src')
#os.chdir('./src')

from kivy.app import App

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from asmcnc.skavaUI import popup_info
from asmcnc.comms import localization

from kivy.config import Config

Config.set('kivy', 'keyboard_mode', 'systemanddock')

if sys.platform.startswith("linux"):
    # get screen resolution as "1280x800" or "800x480"
    resolution = os.popen(""" fbset | grep -oP 'mode "\K[^"]+' """).read().strip()
    width, height = resolution.split("x")
    Config.set('graphics', 'width', width)
    Config.set('graphics', 'height', height)
else:
    Config.set('graphics', 'width', '800')
    Config.set('graphics', 'height', '480')

Config.set('graphics', 'maxfps', '60')
Config.set('kivy', 'KIVY_CLOCK', 'interrupt')

# path_to_EC = os.getcwd()
# sys.path.append('./src')
# os.chdir('./src')

Builder.load_string("""
<MenuScreen>:
    BoxLayout:
        Button:
            text: 'Popup'
            on_press: root.test()
""")


# Declare both screens
class MenuScreen(Screen):
    test_no = 0
    popup_no = 0

    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)

        self.sm = kwargs['sm']
        self.l = kwargs['l']

        self.info_popups = None
        self.popup_9_text = 'None'
        self.popup_8_text = 'None'
        self.popup_7_text = 'None'
        self.popup_6_text = 'None'
        self.popup_5_text = 'None'
        self.popup_4_text = 'None'
        self.popup_3_text = 'None'
        self.popup_2_text = 'None'
        self.popup_1_text = 'None'
        self.popup_0_text = 'None'

        self.info_popups = [
            (self.sm, self.l, 500, self.popup_0_text),
            (self.sm, self.l, 780, self.popup_1_text),
            (self.sm, self.l, 750, self.popup_2_text),
            (self.sm, self.l, 700, self.popup_3_text),
            (self.sm, self.l, 500, self.popup_4_text),
            (self.sm, self.l, 500, self.popup_5_text),
            (self.sm, self.l, 760, self.popup_6_text),
            (self.sm, self.l, 450, self.popup_7_text),
            (self.sm, self.l, 760, self.popup_8_text),
            (self.sm, self.l, 450, self.popup_9_text)]

    def test(self):
        for j in range(0, len(self.l.approved_languages)):
            self.next_lang()
            self.update_strings()
            args = self.info_popups[self.popup_no]
            popup_info.PopupInfo(args[0], args[1], args[2], args[3])
        self.popup_no += 1
        if self.popup_no > len(self.info_popups):
            self.popup_no = 0

    def format_command(self, cmd):
        wrapped_cmd = textwrap.fill(cmd, width=50, break_long_words=False)
        return wrapped_cmd

    def next_lang(self):
        # LOCALIZATION TESTING -----------------------------------------------------------
        if self.test_no < len(self.l.approved_languages):
            lang = self.l.approved_languages[self.test_no]
            self.l.load_in_new_language(lang)
            Logger.info("New lang: " + str(lang))
            self.test_no = self.test_no + 1
        else:
            self.test_no = 0

    def update_strings(self):
        self.popup_0_text = self.l.get_str("File names must be between 1 and 40 characters long.")
        self.popup_1_text = (
                self.l.get_str(
                    "When using a 110V spindle as part of your SmartBench, please be aware of the following:") + \
                "\n\n" + \
                self.l.get_str("110V spindles have a minimum speed of ~10,000 RPM.") + \
                "\n\n" + \
                self.l.get_str(
                    "SmartBench electronics are set up to work with a 230V spindle, so our software does a smart conversion to make sure the machine code we send is adjusted to control a 110V spindle.") + \
                "\n\n" + \
                self.l.get_str(
                    "The 5% spindle speed adjustments in the Job Screen cannot be converted for a 110V spindle, so they will not be able to adjust the speed by exactly 5%.") + \
                " " + \
                self.l.get_str(
                    "You will still be able to use the real time spindle speed feedback feature to assist your adjustment.")
        )
        self.popup_2_text = (

                self.l.get_bold("Touchplate offset") + \
                "\n" + \
                self.l.get_str("Update the offset to make setting the Z datum even more precise.") + \
                "\n" + \
                self.l.get_str("Make sure you press the save button to save your settings.") + \
                "\n\n" + \
                self.l.get_bold("Time since lead screw lubricated") + \
                "\n" + \
                self.l.get_str(
                    "If you have just lubricated the Z head lead screw, reset the hours since it was last lubricated.") + \
                "\n" + \
                self.l.get_str("This will reset the time until SmartBench gives you the next reminder.") + \
                "\n" + \
                self.l.get_str("Make sure you press the save button to save your settings.")
        )
        self.popup_3_text = (
                self.l.get_bold("To set, if laser hardware is fitted:") + "\n\n" + self.l.get_str(
            "1. Enable laser crosshair (switch to on).").replace(self.l.get_str("on"),
                                                                 self.l.get_bold("on")) + "\n" + self.l.get_str(
            "2. On a test piece, cut a mark using manual moves.") + "\n" + self.l.get_str(
            "3. Lift Z Head and press the reset button in the bottom left.").replace(
            self.l.get_str("reset"), self.l.get_bold("reset")) + "\n" + self.l.get_str(
            "4. Move the Z Head so that the cross hair lines up with the mark centre.") + "\n" + self.l.get_str(
            "5. Press save.").replace(self.l.get_str("save"), self.l.get_bold("save"))
        )
        self.popup_4_text = (
            "This serial number is already in the database! You cannot overwrite."
        )
        self.popup_5_text = self.l.get_str('Calibration complete!')
        self.popup_6_text = (
                self.l.get_bold(
                    "Automatic lifting during a pause (recommended for most tools)"
                )
                + ":"
                + "\n"
                + self.l.get_str(
            "When paused, SmartBench can automatically lift the Z axis and move the tool away from the job."
        )
                + "\n\n"
                + " - "
                + self.l.get_str("This can be used to inspect the work or clear blockages.")
                + "\n"
                + " - "
                + self.l.get_str(
            "It allows the spindle to decelerate away from the job, avoiding burn marks."
        )
                + "\n\n"
                + self.l.get_str(
            "SmartBench automatically returns the tool to the correct position before resuming."
        )
                + "\n\n"
                + self.l.get_bold(
            "Do not allow this feature if the tool has any inverted horizontal features which would rip through the job if the tool were to be lifted (e.g. a biscuit cutter tool profile)."
        )
        )
        self.popup_7_text = (
                self.l.get_str('New software update available for download!') + '\n\n' +
                self.l.get_str(
                    'Please use the Update app to get the latest version.'
                ).replace(self.l.get_str('Update'), self.l.get_bold('Update'))
        )
        self.popup_8_text = (
                self.l.get_bold("Manual squaring")
                + "\n"
                + self.l.get_str(
            "Before power up, the user manually pushes the X beam up against the bench legs at the home end."
        )
                + " "
                + self.l.get_str("The power is then switched on.")
                + " "
                + self.l.get_str(
            "The motor coils lock the lower beam into position with a high degree of reliability."
        )
                + " "
                + self.l.get_str(
            "Thus, mechanical adjustments to square the beam can be repeated."
        )
                + "\n\n"
                + self.l.get_bold("Auto squaring")
                + "\n"
                + self.l.get_str("No special preparation from the user is needed.")
                + " "
                + self.l.get_str(
            "When homing, the lower beam automatically drives into the legs to square the X beam against the bench legs."
        )
                + " "
                + self.l.get_str("The stalling procedure can offer a general squareness.")
                + " "
                + self.l.get_str(
            "But at the end of the movement, the motor coils can bounce into a different step position."
        )
                + " "
                + self.l.get_str(
            "Thus, mechanical adjustments to square the beam can be repeated less reliably than manual squaring."
        )
        )
        self.popup_9_text = (
                self.format_command(self.l.get_str('Before running, a file needs to be loaded.')) + '\n\n' + \
                self.format_command(self.l.get_str('Tap the file chooser in the first tab (top left) to load a file.'))
        )
        self.info_popups = [
            (self.sm, self.l, 500, self.popup_0_text),
            (self.sm, self.l, 780, self.popup_1_text),
            (self.sm, self.l, 750, self.popup_2_text),
            (self.sm, self.l, 700, self.popup_3_text),
            (self.sm, self.l, 500, self.popup_4_text),
            (self.sm, self.l, 500, self.popup_5_text),
            (self.sm, self.l, 760, self.popup_6_text),
            (self.sm, self.l, 450, self.popup_7_text),
            (self.sm, self.l, 760, self.popup_8_text),
            (self.sm, self.l, 450, self.popup_9_text)]

class TestApp(App):

    def build(self):
        l = localization.Localization()

        # Create the screen manager
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu', sm=sm, l=l))

        return sm


if __name__ == '__main__':
    TestApp().run()
