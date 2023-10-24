from datetime import datetime

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from asmcnc.skavaUI import popup_info
from asmcnc.apps.drywall_cutter_app import widget_xy_move_drywall

Builder.load_string("""
<DrywallCutterScreen>:

    xy_move_container:xy_move_container

    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            orientation: 'horizontal'
            padding: dp(5)
            spacing: dp(10)

            Button:
                size_hint_x: 7
                text: 'Home'
                on_press: root.home()

            Button:
                size_hint_x: 7
                text: 'File'

            Spinner:
                size_hint_x: 7
                text: 'Tool'
                values: root.tool_options

            Spinner:
                size_hint_x: 7
                text: 'Shape'
                values: root.shape_options
                on_text: root.select_shape()

            Button:
                size_hint_x: 7
                text: 'Rotate'
                on_press: root.rotate_shape()

            Spinner:
                size_hint_x: 7
                text: 'Cut on line'
                text_size: self.size
                halign: 'center'
                valign: 'middle'
                values: root.line_cut_options

            Button:
                size_hint_x: 7
                text: 'Material setup'
                text_size: self.size
                halign: 'center'
                valign: 'middle'
                on_press: root.material_setup()

            Button:
                size_hint_x: 15
                text: 'STOP'
                on_press: root.stop()

            Button:
                size_hint_x: 7
                on_press: root.quit_to_lobby()
                text: 'Quit'

        BoxLayout:
            size_hint_y: 5
            orientation: 'horizontal'
            padding: dp(5)
            spacing: dp(10)

            BoxLayout:
                size_hint_x: 55

                canvas.before:
                    Color:
                        rgba: hex('#E5E5E5FF')
                    Rectangle:
                        size: self.size
                        pos: self.pos

            BoxLayout:
                size_hint_x: 23
                orientation: 'vertical'
                spacing: dp(10)

                BoxLayout:
                    id: xy_move_container
                    size_hint_y: 31
                    padding: [dp(0), dp(30)]

                    canvas.before:
                        Color:
                            rgba: hex('#E5E5E5FF')
                        Rectangle:
                            size: self.size
                            pos: self.pos

                BoxLayout:
                    size_hint_y: 7
                    orientation: 'horizontal'
                    spacing: dp(10)

                    Button:
                        text: 'Simulate'
                        on_press: root.simulate()

                    Button:
                        text: 'Save'
                        on_press: root.save()

                    Button:
                        text: 'Run'
                        on_press: root.run()

""")

def log(message):
    timestamp = datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + message)

class DrywallCutterScreen(Screen):

    tool_options = ['6mm', '8mm', 'V groove']
    shape_options = ['Circle', 'Square', 'Line', 'Geberit']
    line_cut_options = ['Cut on line', 'Cut inside line', 'Cut outside line']

    def __init__(self, **kwargs):
        super(DrywallCutterScreen, self).__init__(**kwargs)

        self.sm = kwargs['screen_manager']
        self.m = kwargs['machine']
        self.l = kwargs['localization']
        self.gtg = kwargs['geometry_to_gcode']

        # XY move widget
        self.xy_move_widget = widget_xy_move_drywall.XYMoveDrywall(machine=self.m, screen_manager=self.sm)
        self.xy_move_container.add_widget(self.xy_move_widget)

    def home(self):
        self.m.request_homing_procedure('drywall_cutter','drywall_cutter')

    def select_shape(self):
        pass

    def rotate_shape(self):
        pass

    def material_setup(self):
        pass

    def stop(self):
        popup_info.PopupStop(self.m, self.sm, self.l)

    def quit_to_lobby(self):
        self.sm.current = 'lobby'

    def simulate(self):
        pass

    def save(self):
        pass

    def run(self):
        pass
