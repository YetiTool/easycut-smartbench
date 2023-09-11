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

    filename_input:filename_input
    feed_input:feed_input
    speed_input:speed_input
    depth_input:depth_input

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
                padding: [dp(15), dp(0)]

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

            BoxLayout:
                padding: [dp(15), dp(0)]

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

                    # BoxLayout:
                    #     orientation: 'horizontal'
                    #     spacing: dp(10)

                    #     TextInput:
                    #         font_size: dp(20)
                    #         multiline: False
                    #         hint_text: 'Stock length'
                    #         input_filter: 'int'
                    #         disabled: True

                    #     TextInput:
                    #         font_size: dp(20)
                    #         multiline: False
                    #         hint_text: 'Stock width'
                    #         input_filter: 'int'
                    #         disabled: True

                    #     TextInput:
                    #         font_size: dp(20)
                    #         multiline: False
                    #         hint_text: 'Stock depth'
                    #         input_filter: 'int'
                    #         disabled: True

                    BoxLayout:
                        orientation: 'horizontal'
                        spacing: dp(10)

                        TextInput:
                            id: feed_input
                            font_size: dp(20)
                            multiline: False
                            hint_text: 'Feed'
                            input_filter: 'int'

                        TextInput:
                            id: speed_input
                            font_size: dp(20)
                            multiline: False
                            hint_text: 'Speed'
                            input_filter: 'int'

                        TextInput:
                            id: depth_input
                            font_size: dp(20)
                            multiline: False
                            hint_text: 'Pass depth'
                            input_filter: 'int'

                        # TextInput:
                        #     font_size: dp(20)
                        #     multiline: False
                        #     hint_text: '# of passes'
                        #     input_filter: 'int'

                    TextInput:
                        id: filename_input
                        font_size: dp(20)
                        multiline: False
                        hint_text: 'Enter filename'

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
                padding: [dp(5), dp((self.height - (self.width / 2)) / 2)]

                BoxLayout:
                    width: dp(600)
                    height: dp(300)
                    size_hint: (None, None)

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
    raw_gcode_filepath = './asmcnc/apps/geberit_cutter_app/geberit_cutter_raw_gcode.nc'

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
        if not (self.filename_input.text and self.feed_input.text and self.speed_input.text and self.depth_input.text):
            popup_info.PopupError(self.sm, self.l, "Please ensure that every text box is filled in.")
            return

        if self.filename_input.text.endswith(('.nc','.NC','.gcode','.GCODE','.GCode','.Gcode','.gCode')):
            self.wait_popup = popup_info.PopupWait(self.sm, self.l)
            Clock.schedule_once(lambda dt: self.convert_to_gcode(), 0.5)
        else:
            popup_info.PopupError(self.sm, self.l, "Please ensure that the filename ends with a valid GCode file extension.")

    def convert_to_gcode(self):
        def generate_svg():
            # Viewbox can be set to the container size, so that positions can then be defined in pixels rather than relative to actual size of the SVG
            # The height and width are switched - this is necessary so that everything is drawn in full size but out of bounds, which is fixed by a reflection further down
            dwg = svgwrite.Drawing(filename=self.svg_output_filepath, size=('1200mm','2400mm'), viewBox='0 0 %s %s' % (self.editor_container.height, self.editor_container.width))
            for panel in self.editor_container.children:
                # Position has to be converted to local coordinates of the container, as they are relative to the window
                panel_pos = self.editor_container.to_local(panel.x, panel.y, relative=True)

                # The long side has to be drawn parallel to the y axis - to solve this, this matrix transformation performs a reflection in the line y=x
                # This means that the long side can be drawn parallel to the x axis, directly from the kivy coords, instead of figuring out how to switch all the x/y coords
                transformation = "matrix(0 1 1 0 0 0)"
                # Additionally, when a panel is drawn, a scaling and translation is applied, which vertically flips the svg
                # This is needed because kivy measures Y coords from the opposite end of the screen and draws stuff upside down
                transformation += " scale(1,-1) translate(0,%s)" % -self.editor_container.height

                # Now rotate around the centre of the panel, which again needs the coord converted
                panel_centre = self.editor_container.to_local(*panel.center, relative=True)
                # Then add rotation
                transformation += " rotate(%s,%s,%s)" % (panel.rotation, panel_centre[0], panel_centre[1])

                # If the panel is turned sideways
                if int(panel.rotation) % 180 != 0:
                    # Then rotation will mess up its position so align centre first
                    # It is important to note that this has to be added after the rotation, because transformations are performed right to left
                    transformation += " translate(%s,%s)" % (panel.width/2, -panel.height/4)

                panel_size = (panel.width, panel.height)

                # Create rectangle for panel background
                dwg.add(dwg.rect(panel_pos, panel_size, fill='white', stroke='black', transform=transformation))

                # Set up objects for the detail of the panel as relative to rectangle position and size
                # The same transform can be used as the rectangle transform as it is done relative to the centre of the panel
                big_circle_centre = (panel_pos[0] + (panel.width / 2), panel_pos[1] + (panel.height / 4))
                big_circle_radius = panel.height / 10
                dwg.add(dwg.circle(big_circle_centre, big_circle_radius, fill='white', stroke='black', transform=transformation))

                small_circle_centre = (panel_pos[0] + (panel.width / 2), panel_pos[1] + (panel.height * 0.45))
                small_circle_radius = panel.height / 40
                dwg.add(dwg.circle(small_circle_centre, small_circle_radius, fill='white', stroke='black', transform=transformation))

                small_rect_pos = (panel_pos[0] + (panel.width / 4), panel_pos[1] + (panel.height * 0.78))
                small_rect_size = (panel.width / 2, panel.width / 4)
                dwg.add(dwg.rect(small_rect_pos, small_rect_size, fill='white', stroke='black', transform=transformation))

                rounded_rect_size = (panel.width / 6, panel.width / 16)
                roundedness = rounded_rect_size[0] / 10

                rounded_rect_left_pos = (panel_pos[0] + (panel.width * 0.18), panel_pos[1] + (panel.height * 0.37))
                dwg.add(dwg.rect(rounded_rect_left_pos, rounded_rect_size, roundedness, roundedness, fill='white', stroke='black', transform=transformation))

                rounded_rect_right_pos = (panel_pos[0] + (panel.width * 0.82) - rounded_rect_size[0], panel_pos[1] + (panel.height * 0.37))
                dwg.add(dwg.rect(rounded_rect_right_pos, rounded_rect_size, roundedness, roundedness, fill='white', stroke='black', transform=transformation))
            dwg.save()

            convert_svg_to_paths()

        def convert_svg_to_paths():
            # The svg now has to be converted to paths, as required by the gcode converter
            paths, attributes = svg2paths(self.svg_output_filepath)
            dwg = svgwrite.Drawing(filename=self.svg_output_filepath, size=('1200mm','2400mm'), viewBox='0 0 %s %s' % (self.editor_container.height, self.editor_container.width))
            for i, path in enumerate(paths):
                # Recover attributes of current path, or else transformation is lost
                path_attributes = attributes[i]
                # Convert from svgpathtools path to svgwrite path using shared attribute d
                dwg.add(svgwrite.path.Path(path.d(), fill=path_attributes['fill'], stroke=path_attributes['stroke'], transform=path_attributes['transform']))
            dwg.save()

            convert_svg_to_gcode()

        def convert_svg_to_gcode():
            # Now, convert to gcode
            if sys.platform != "win32":
                cmd = "cargo run --release -- /home/pi/easycut-smartbench/src/asmcnc/apps/geberit_cutter_app/geberit_cutter_app_output.svg"
                # As svg2gcode does not allow for spindle speed or depth to be set, both of those are included in the spindle on command
                cmd += " --off M5 --on M3S%sG1Z%sF%s --feedrate %s -o /home/pi/easycut-smartbench/src/asmcnc/apps/geberit_cutter_app/geberit_cutter_raw_gcode.nc" % (self.speed_input.text, "-" + self.depth_input.text, self.feed_input.text, self.feed_input.text)
                working_directory = '/home/pi/svg2gcode'
            else:
                # For this to work on windows, cargo and svg2gcode need to be installed in the right places relative to easycut
                cmd = "%s/../../../.cargo/bin/cargo.exe run --release -- %s/asmcnc/apps/geberit_cutter_app/geberit_cutter_app_output.svg" % (os.getcwd(), os.getcwd())
                cmd +=  " --off M5 --on M3S%sG1Z%sF%s --feedrate %s -o %s/asmcnc/apps/geberit_cutter_app/geberit_cutter_raw_gcode.nc" % (self.speed_input.text, "-" + self.depth_input.text, self.feed_input.text, self.feed_input.text, os.getcwd())
                working_directory = os.getcwd() + '/../../svg2gcode'

            # This is required because command needs to be executed from svg2gcode folder
            subprocess.Popen(cmd.split(), cwd=working_directory).wait()

            process_gcode()

        def process_gcode():
            # Anything that svg2gcode can't be forced to do, has to be done manually

            with open(self.raw_gcode_filepath) as f:
                raw_gcode = f.readlines()

            def map_gcodes(line):
                # Stop turning off spindle throughout file by deleting all M5 commands
                if 'M5' in line:
                    line = line.replace('M5', '')
                return line

            processed_gcode = map(map_gcodes, raw_gcode)
            # Then turn spindle off at the end
            processed_gcode.append('M5')

            with open('./jobCache/' + self.filename_input.text, 'w+') as f:
                f.write(''.join(processed_gcode))

            self.wait_popup.popup.dismiss()
            popup_info.PopupInfo(self.sm, self.l, 500, self.l.get_str("Gcode file saved to filechooser!"))

            self.reset_editor()

        generate_svg()

    def reset_editor(self):
        self.editor_container.clear_widgets()
        self.panels_added = 0
        self.current_panel_selection = None
        self.filename_input.text = ""
        self.feed_input.text = ""
        self.speed_input.text = ""
        self.depth_input.text = ""

    def quit_to_lobby(self):
        self.sm.current = 'lobby'
