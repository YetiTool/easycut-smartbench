from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

from asmcnc.skavaUI import popup_info

from asmcnc.apps.systemTools_app.screens.xy_jig import screen_xy_jig
from asmcnc.apps.systemTools_app.screens.xy_jig import screen_xy_jig_monitor
from asmcnc.apps.systemTools_app.screens.xy_jig import screen_xy_jig_manual_move

from asmcnc.comms.yeti_grbl_protocol.c_defines import *

Builder.load_string("""
<XYJigDecision>:

    BoxLayout:
        padding: [dp(20), dp(150)]
        spacing: dp(20)

        Button:
            text: 'X Single Stack'
            font_size: dp(50)
            bold: True
            text_size: self.size
            halign: 'center'
            valign: 'middle'
            background_color: [1,0,0,1]
            background_normal: ''
            on_press: root.enter_xy_jig('X_single')

        Button:
            text: 'X Double Stack'
            font_size: dp(50)
            bold: True
            text_size: self.size
            halign: 'center'
            valign: 'middle'
            background_color: [1,0,0,1]
            background_normal: ''
            on_press: root.enter_xy_jig('X_double')

        Button:
            text: 'Y'
            font_size: dp(50)
            bold: True
            text_size: self.size
            halign: 'center'
            valign: 'middle'
            background_color: hex('#00C300FF')
            background_normal: ''
            on_press: root.enter_xy_jig('Y')

""")


class XYJigDecision(Screen):

    def __init__(self, **kwargs):
        super(XYJigDecision, self).__init__(**kwargs)

        self.systemtools_sm = kwargs['systemtools']
        self.m = kwargs['m']
        self.l = kwargs['l']

    def enter_xy_jig(self, axis):

        if not self.systemtools_sm.sm.has_screen('xy_jig_monitor'):
            xy_jig_decision_screen = screen_xy_jig_monitor.XYJigMonitor(name='xy_jig_monitor', systemtools=self.systemtools_sm, m=self.m, l=self.l)
            self.systemtools_sm.sm.add_widget(xy_jig_decision_screen)

        # Always destroy screens on entry, so that they can be set up correctly based on axis
        self.systemtools_sm.destroy_screen('xy_jig')
        xy_jig_screen = screen_xy_jig.XYJig(name='xy_jig', systemtools=self.systemtools_sm, m=self.m, l=self.l, axis=axis)
        self.systemtools_sm.sm.add_widget(xy_jig_screen)

        self.systemtools_sm.destroy_screen('xy_jig_manual_move')
        xy_jig_screen = screen_xy_jig_manual_move.XYJigManualMove(name='xy_jig_manual_move', systemtools=self.systemtools_sm, m=self.m, axis=axis)
        self.systemtools_sm.sm.add_widget(xy_jig_screen)

        try:
            if axis == 'Y':
                self.systemtools_sm.sm.get_screen('xy_jig').max_travel = -self.m.s.setting_131
                self.systemtools_sm.sm.get_screen('xy_jig').max_speed = self.m.s.setting_111
                self.systemtools_sm.sm.get_screen('xy_jig').max_x_speed = self.m.s.setting_110
                self.m.disable_y_motors()
            else:
                self.systemtools_sm.sm.get_screen('xy_jig').max_travel = -self.m.s.setting_130
                self.systemtools_sm.sm.get_screen('xy_jig').max_speed = self.m.s.setting_110
                self.m.disable_x_motors()

            self.systemtools_sm.sm.current = 'xy_jig'
        except:
            self.systemtools_sm.open_factory_settings_screen()
            popup_info.PopupWarning(self.systemtools_sm.sm, self.l, "Unable to read GRBL settings")
