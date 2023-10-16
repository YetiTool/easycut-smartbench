from datetime import datetime

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.scatter import Scatter
from kivy.clock import Clock

from asmcnc.skavaUI import popup_info

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
        self.gtg = kwargs['geometry_to_gcode']

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
            dwg = self.gtg.create_empty_svg(self.svg_output_filepath, '1200mm', '2400mm', self.editor_container.height, self.editor_container.width)
            for panel in self.editor_container.children:
                # Position has to be converted to local coordinates of the container, as they are relative to the window
                panel_pos = self.editor_container.to_local(panel.x, panel.y, relative=True)
                panel_centre = self.editor_container.to_local(*panel.center, relative=True)

                self.gtg.create_geberit_panel(dwg, panel_pos, panel_centre, panel.rotation, panel.width, panel.height)
            dwg.save()

            Clock.schedule_once(lambda dt: convert_svg_to_paths(), 0.5)

        def convert_svg_to_paths():
            # Need to convert to paths for gcode conversion to work
            self.gtg.convert_svg_to_paths(self.svg_output_filepath, '1200mm', '2400mm', self.editor_container.height, self.editor_container.width)

            Clock.schedule_once(lambda dt: convert_svg_to_gcode(), 0.5)

        def convert_svg_to_gcode():
            # Now, convert to gcode
            self.gtg.convert_svg_to_gcode(self.svg_output_filepath, self.raw_gcode_filepath, self.speed_input.text, self.depth_input.text, self.feed_input.text)

            Clock.schedule_once(lambda dt: process_gcode(), 0.5)

        def process_gcode():
            # Anything that svg2gcode can't be forced to do, has to be done manually

            with open(self.raw_gcode_filepath) as f:
                raw_gcode = f.readlines()

            processed_gcode = self.gtg.post_process_gcode(raw_gcode)

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
