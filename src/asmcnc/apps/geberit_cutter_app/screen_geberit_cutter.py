from datetime import datetime

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.scatter import Scatter

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
    def __init__(self, panel_height, pos, **kwargs):
        super(PanelWidget, self).__init__(**kwargs)

        panel_width = panel_height / 2
        self.size_hint = (None, None)
        self.size = (panel_width, panel_height)
        self.pos = pos

        image = Image(source="./asmcnc/apps/geberit_cutter_app/img/geberit_panel.png", size_hint=(None,None), size=(panel_width,panel_height))
        self.add_widget(image)

class GeberitCutterScreen(Screen):

    panels_added = 0

    def __init__(self, **kwargs):
        super(GeberitCutterScreen, self).__init__(**kwargs)

        self.sm = kwargs['screen_manager']
        self.m = kwargs['machine']
        self.l = kwargs['localization']

    def add_panel(self):
        if self.panels_added < 4:
            self.panels_added += 1
            self.editor_container.add_widget(PanelWidget(self.editor_container.height, self.editor_container.pos))

    def rotate_panel(self):
        pass

    def save(self):
        self.reset_editor()

    def reset_editor(self):
        self.editor_container.canvas.clear()
        self.panels_added = 0

    def quit_to_lobby(self):
        self.sm.current = 'lobby'
