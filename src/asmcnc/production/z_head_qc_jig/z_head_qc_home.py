from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.clock import Clock

from asmcnc.production.z_head_qc_jig import popup_z_head_qc

try: 
    import pigpio

except:
    pass

Builder.load_string("""
<ZHeadQCHome>:
    
    test_fw_update_button : test_fw_update_button

    BoxLayout:
        orientation: 'vertical'

        GridLayout:
            size: self.parent.size
            pos: self.parent.pos
            cols: 1
            rows: 3

            Label: 
                text: 'Have you just updated the FW on this Z Head?'
                color: 1,1,1,1
                text_size: self.size
                markup: 'True'
                halign: 'center'
                valign: 'middle'
                font_size: dp(30)

            GridLayout: 
                cols: 2

                Button:
                    id: test_fw_update_button 
                    text: 'NO - Update FW now!'
                    font_size: dp(20)
                    on_press: root.test_fw_update()

                Button:
                    text: 'YES - Take me to QC!'
                    font_size: dp(20)
                    on_press: root.enter_qc()

            Button: 
                text: 'Secret option C - take me to WARRANTY QC!'
                font_size: dp(20)
                on_press: root.secret_option_c()
""")


class ZHeadQCHome(Screen):
    def __init__(self, **kwargs):
        super(ZHeadQCHome, self).__init__(**kwargs)

        self.sm = kwargs['sm']
        self.m = kwargs['m']

        self.start_calibration_timer(0.5)

    def start_calibration_timer(self, minutes):
        self.sm.get_screen('qc3').update_time(minutes*30)

    def enter_qc(self):
        self.sm.current = 'qc1'

    def test_fw_update(self):

        self.test_fw_update_button.text = "  Updating..."

        def nested_do_fw_update(dt):
            pi = pigpio.pi()
            pi.set_mode(17, pigpio.ALT3)
            print(pi.get_mode(17))
            pi.stop()
            self.m.s.s.close()

            cmd = "grbl_file=/media/usb/GRBL*.hex && avrdude -patmega2560 -cwiring -P/dev/ttyAMA0 -b115200 -D -Uflash:w:$(echo $grbl_file):i"
            proc = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = True)
            stdout, stderr = proc.communicate()
            exit_code = int(proc.returncode)

            if exit_code == 0: 
                did_fw_update_succeed = "Success! Disconnect or reboot to reconnect to Z head."

            else: 
                did_fw_update_succeed = "Update failed. Reboot to reconnect to Z head."

            popup_z_head_qc.PopupFWUpdateDiagnosticsInfo(self.sm, did_fw_update_succeed, str(stdout))

        Clock.schedule_once(nested_do_fw_update, 1)


    def secret_option_c(self):
        self.sm.current = 'qcWC'


