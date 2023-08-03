import os, sys, subprocess
from datetime import datetime

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.scatter import Scatter
from kivy.clock import Clock

from asmcnc.skavaUI import popup_info

import svgwrite
from svgpathtools import svg2paths, parse_path

Builder.load_string("""
<GeberitCutterScreen>:

    editor_container:editor_container

    BoxLayout:
        orientation: 'horizontal'

        canvas.before:
            Color:
                rgba: hex('#E2E2E2FF')
            Rectangle:
                size: self.size
                pos: self.pos

        BoxLayout:
            size_hint_x: 0.3
            orientation: 'vertical'
            padding: dp(10)
                    
            Label:
                size_hint_y: 0.3
                text: 'Geberit cutter'
                color: 0,0,0,1
                font_size: dp(28)

            BoxLayout:
                size_hint_y: 1.3
                padding: [dp(10), dp(0)]

                Button:
                    background_color: [0,0,0,0]
                    on_press: root.add_panel()
                    BoxLayout:
                        size: self.parent.size
                        pos: self.parent.pos
                        Image:
                            source: "./asmcnc/apps/geberit_cutter_app/img/add_panel_button.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True

            BoxLayout:
                padding: [dp(25), dp(0)]

                Button:
                    background_color: [0,0,0,0]
                    on_press: root.rotate_panel()
                    BoxLayout:
                        size: self.parent.size
                        pos: self.parent.pos
                        Image:
                            source: "./asmcnc/apps/geberit_cutter_app/img/rotate_button.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True

            TextInput:
                size_hint_y: 0.4
                font_size: dp(23)
                multiline: False
                hint_text: 'Enter filename'

            BoxLayout:
                padding: [dp(25), dp(0)]

                Button:
                    background_color: [0,0,0,0]
                    on_press: root.save()
                    BoxLayout:
                        size: self.parent.size
                        pos: self.parent.pos
                        Image:
                            source: "./asmcnc/apps/maintenance_app/img/save_button_132.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True

        BoxLayout:
            orientation: 'vertical'

            BoxLayout:
                size_hint_y: 0.28
                orientation: 'horizontal'

                BoxLayout:
                    orientation: 'vertical'
                    spacing: dp(10)
                    padding: [dp(10), dp(10), dp(10), dp(0)]

                    BoxLayout:
                        orientation: 'horizontal'
                        spacing: dp(10)

                        TextInput:
                            font_size: dp(20)
                            multiline: False
                            hint_text: 'Stock length'
                            input_filter: 'int'

                        TextInput:
                            font_size: dp(20)
                            multiline: False
                            hint_text: 'Stock width'
                            input_filter: 'int'

                        TextInput:
                            font_size: dp(20)
                            multiline: False
                            hint_text: 'Stock depth'
                            input_filter: 'int'

                    BoxLayout:
                        orientation: 'horizontal'
                        spacing: dp(10)

                        TextInput:
                            font_size: dp(20)
                            multiline: False
                            hint_text: 'Feed'
                            input_filter: 'int'

                        TextInput:
                            font_size: dp(20)
                            multiline: False
                            hint_text: 'Speed'
                            input_filter: 'int'

                        TextInput:
                            font_size: dp(20)
                            multiline: False
                            hint_text: 'Pass depth'
                            input_filter: 'int'

                        TextInput:
                            font_size: dp(20)
                            multiline: False
                            hint_text: '# of passes'
                            input_filter: 'int'

                Button:
                    size_hint_x: 0.2
                    background_color: [0,0,0,0]
                    on_press: root.quit_to_lobby()
                    BoxLayout:
                        size: self.parent.size
                        pos: self.parent.pos
                        Image:
                            source: "./asmcnc/apps/shapeCutter_app/img/exit_cross.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True

            BoxLayout:
                padding: [dp(0), dp(10), dp(10), dp(10)]

                BoxLayout:
                    padding: [dp(0), dp((self.height - (self.width / 2)) / 2)]

                    BoxLayout:
                        canvas.before:
                            Color:
                                rgba: .5, .5, .5, 1
                            Line:
                                width: 2
                                rectangle: self.x, self.y, self.width, self.height

                        canvas:
                            Color:
                                rgba: 1,1,1,1
                            Rectangle:
                                size: self.size
                                pos: self.pos

                        StencilView:
                            size: self.parent.size
                            pos: self.parent.pos

                            FloatLayout:
                                id: editor_container
                                size: self.parent.size
                                pos: self.parent.pos

""")

def log(message):
    timestamp = datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + message)

class PanelWidget(Scatter):

    panel_image_filepath = "./asmcnc/apps/geberit_cutter_app/img/geberit_panel.png"
    panel_selected_image_filepath = "./asmcnc/apps/geberit_cutter_app/img/geberit_panel_selected.png"

    def __init__(self, panel_height, pos, **kwargs):
        super(PanelWidget, self).__init__(**kwargs)

        self.sm = kwargs['screen_manager']

        panel_width = panel_height / 2
        self.size_hint = (None, None)
        self.size = (panel_width, panel_height)
        self.pos = pos
        self.do_rotation=False
        self.do_scale=False

        self.panel_image = Image(source=self.panel_image_filepath, size_hint=(None,None), size=(panel_width,panel_height))
        self.add_widget(self.panel_image)

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            self.select_panel()

        return super(PanelWidget, self).on_touch_down(touch)

    def select_panel(self):
        # When clicked, show that the panel is selected by changing its colour
        current_panel_selection = self.sm.get_screen('geberit_cutter').current_panel_selection
        if current_panel_selection:
            current_panel_selection.panel_image.source = self.panel_image_filepath

        self.panel_image.source = self.panel_selected_image_filepath
        self.sm.get_screen('geberit_cutter').current_panel_selection = self

    def rotate_clockwise(self):
        self.rotation -= 90

class GeberitCutterScreen(Screen):

    svg_output_filepath = './asmcnc/apps/geberit_cutter_app/geberit_cutter_app_output.svg'

    panels_added = 0
    current_panel_selection = None

    def __init__(self, **kwargs):
        super(GeberitCutterScreen, self).__init__(**kwargs)

        self.sm = kwargs['screen_manager']
        self.m = kwargs['machine']
        self.l = kwargs['localization']

    def add_panel(self):
        if self.panels_added < 4:
            self.panels_added += 1
            new_panel = PanelWidget(self.editor_container.height, self.editor_container.pos, screen_manager=self.sm)
            new_panel.select_panel()
            self.editor_container.add_widget(new_panel)

    def rotate_panel(self):
        if self.current_panel_selection:
            self.current_panel_selection.rotate_clockwise()

    def save(self):
        self.wait_popup = popup_info.PopupWait(self.sm, self.l, self.l.get_str('Please wait'))
        Clock.schedule_once(lambda dt: self.convert_to_gcode(), 0.1)

    def convert_to_gcode(self):
        # Viewbox can be set to the container size, so that positions can then be defined in pixels rather than relative to actual size of the SVG
        dwg = svgwrite.Drawing(filename=self.svg_output_filepath, size=('2400mm','1200mm'), viewBox='0 0 %s %s' % (self.editor_container.width, self.editor_container.height))
        for panel in self.editor_container.children:
            # When a panel is drawn, a scaling and translation is applied, which vertically flips the svg
            # This is needed because kivy measures Y coords from the opposite end of the screen and draws stuff upside down
            transformation = "scale(1,-1) translate(0,%s)" % -self.editor_container.height
            # Position has to be converted to local coordinates of the container, as they are relative to the window
            panel_pos = self.editor_container.to_local(panel.x, panel.y, relative=True)
            # Second element of bbox tuple has size of panel, and swaps width/height on rotation, so saves us rotating manually
            panel_size = panel.bbox[1]

            dwg.add(dwg.rect(panel_pos, panel_size, fill='white', stroke='black', transform=transformation))
        dwg.save()

        # The svg now has to be converted to paths, as required by the gcode converter
        paths, attributes = svg2paths(self.svg_output_filepath)
        dwg = svgwrite.Drawing(filename=self.svg_output_filepath, size=('2400mm','1200mm'), viewBox='0 0 %s %s' % (self.editor_container.width, self.editor_container.height))
        for i, path in enumerate(paths):
            # Recover attributes of current path, or else transformation is lost
            path_attributes = attributes[i]
            # Convert from svgpathtools path to svgwrite path using shared attribute d
            dwg.add(svgwrite.path.Path(path.d(), fill=path_attributes['fill'], stroke=path_attributes['stroke'], transform=path_attributes['transform']))
        dwg.save()

        if sys.platform != "win32":
            cmd = "cargo run --release -- /home/pi/easycut-smartbench/src/asmcnc/apps/geberit_cutter_app/geberit_cutter_app_output.svg --off M5 --on M3 -o /home/pi/easycut-smartbench/src/jobCache/geberit_cutter_output.gcode"
            working_directory = '/home/pi/svg2gcode'
        else:
            # For this to work on windows, cargo and svg2gcode need to be installed in the right places relative to easycut
            cmd = "%s/../../../.cargo/bin/cargo.exe run --release -- %s/asmcnc/apps/geberit_cutter_app/geberit_cutter_app_output.svg --off M5 --on M3 -o %s/jobCache/geberit_cutter_output.gcode" % (os.getcwd(), os.getcwd(), os.getcwd())
            working_directory = os.getcwd() + '/../../svg2gcode'

        # This is required because command needs to be executed from svg2gcode folder
        subprocess.Popen(cmd.split(), cwd=working_directory).wait()

        self.wait_popup.popup.dismiss()
        popup_info.PopupInfo(self.sm, self.l, 500, self.l.get_str("Gcode file saved to filechooser!"))

        self.reset_editor()

    def reset_editor(self):
        self.editor_container.clear_widgets()
        self.panels_added = 0
        self.current_panel_selection = None

    def quit_to_lobby(self):
        self.sm.current = 'lobby'
