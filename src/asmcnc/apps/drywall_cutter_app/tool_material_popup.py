from kivy.app import App
from kivy.uix.popup import Popup
from kivy.lang import Builder

from asmcnc.comms.logging_system.logging_system import Logger

Builder.load_string("""
<Options@SpinnerOption>

    background_normal: ''
    size: self.size
    color: hex('#333333ff')
    halign: 'center'
    markup: 'True'
    font_size: 0.0175*app.width
    background_color: color_provider.get_rgba('black')
    text_size : self.width, None
    canvas.before:
        Color:
            rgba: hex('#e5e5e5ff')
        Rectangle:
            pos: self.pos
            size: self.size


<Choices@Spinner>
    option_cls: Factory.get("Options")
    background_normal: ''
    size: self.size
    color: hex('#333333ff')
    background_color: 0,0,0,0
    text_size : self.width, None
    halign: 'center'
    canvas.before:
        Color:
            rgba: hex('ccccccff')
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(5), dp(5)]

<ToolMaterialPopup>:
    tool_dropdown:tool_dropdown
    confirm_button:confirm_button
    material_dropdown:material_dropdown

    auto_dismiss: False
    size_hint: (None,None)
    size: (dp(app.get_scaled_width(577)), dp(app.get_scaled_height(301)))
    title: ''
    separator_height: 0
    background: './asmcnc/apps/drywall_cutter_app/img/cutting_depths_popup.png'

    FloatLayout:
        id: float_layout
        size_hint: (None, None)
        size: (dp(app.get_scaled_width(577)), dp(app.get_scaled_height(301)))
        pos_hint: {'y': -0.05}
        
        Label:
            id: title_label
            pos_hint: {'x': -0.31, 'y': 0.45}
            text: 'Tool & Material selection'
            font_size: app.get_scaled_sp('20sp')
            color: hex('#F9F9F9')
        
        Label:
            id: description_label
            text: 'Shapes Lite currently only supports YetiPilot profiles. Full Toolbox coming soon'
            text_size: (0.65*self.parent.width, None)
            halign: 'center'
            color: hex('#333333')
            size_hint: (0.75, None)
            pos_hint: {'center_x': 0.5, 'center_y': 0.75}
            
        Label:
            id: material_label
            text: 'Material'
            font_size: app.get_scaled_sp('15sp')
            color: hex('#333333')
            size_hint: (None, None)
            pos_hint: {'center_x': 0.15, 'center_y': 0.55}

        Choices:
            id: material_dropdown
            size_hint: (0.65, 0.1)
            pos_hint: {'center_x': 0.55, 'center_y': 0.55}

        Label:
            id: tool_label
            text: 'Tool'
            font_size: app.get_scaled_sp('15sp')
            color: hex('#333333')
            size_hint: (None, None)
            pos_hint: {'center_x': 0.15, 'center_y': 0.35}

        Choices:
            id: tool_dropdown
            size_hint: (0.65, 0.1)
            pos_hint: {'center_x': 0.55, 'center_y': 0.35}
        
        BoxLayout:
            orientation: 'horizontal'
            pos_hint: {'x': 0.625, 'y': 0.075}
            size_hint: (None, None)
            size: (dp(app.get_scaled_width(189)),dp(app.get_scaled_height(23)))
            spacing: dp(app.get_scaled_width(20))

            Button:
                id: cancel_button
                on_press: root.cancel()
                size_hint: (None,None)
                width: dp(app.get_scaled_width(83))
                height: dp(app.get_scaled_height(23))
                background_color: [0,0,0,0]
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/apps/drywall_cutter_app/img/cancel_button.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True

            Button:
                id: confirm_button
                on_press: root.confirm()
                size_hint: (None,None)
                width: dp(app.get_scaled_width(86))
                height: dp(app.get_scaled_height(23))
                background_color: [0,0,0,0]
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/apps/drywall_cutter_app/img/confirm_button.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True
""")


class ToolMaterialPopup(Popup):

    def __init__(self, localization, config, drywall_cutter_screen, **kwargs):
        super(ToolMaterialPopup, self).__init__(**kwargs)

        self.l = localization
        self.dwt_config = config
        self.drywall_cutter_screen = drywall_cutter_screen

        self.tool_dropdown.bind(text=self.on_tool_change)
        self.material_dropdown.bind(text=self.on_material_change)
        self.dwt_config.bind(active_profile=self.load_config)

        self.profile_db = App.get_running_app().profile_db

    def on_tool_change(self, instance, value):
        if value != '':
            self.confirm_button.disabled = False
            self.confirm_button.opacity = 1
            Logger.debug("Tool changed to " + value)

    def on_material_change(self, instance, value):
        Logger.debug("Material changed to " + value)
        self.tool_dropdown.values = self.profile_db.get_tool_names(self.profile_db.get_material_id(value))
        self.tool_dropdown.text = ''
        self.confirm_button.disabled = True
        self.confirm_button.opacity = 0.5

    def on_open(self):
        self.load_config()
        if self.material_dropdown.text == '' or self.material_dropdown.text == '':  # Only disable if one is empty
            self.confirm_button.disabled = True
            self.confirm_button.opacity = 0.5

    def load_config(self, *args):
        if self.dwt_config.active_config.material:
            material = self.profile_db.get_material_name(self.dwt_config.active_config.material)
            self.material_dropdown.text = material
        if self.dwt_config.active_config.cutter_type:
            tool = self.profile_db.get_tool_name(self.dwt_config.active_config.cutter_type)
            self.tool_dropdown.text = tool
        # Set the material dropdown values
        self.material_dropdown.values = self.profile_db.get_material_names(self.dwt_config.app_type)

    def confirm(self):
        self.dwt_config.on_parameter_change('material', self.profile_db.get_material_id(self.material_dropdown.text))
        self.dwt_config.on_parameter_change('cutter_type', self.profile_db.get_tool_id(self.tool_dropdown.text))
        self.drywall_cutter_screen.update_toolpaths()
        self.dismiss()

    def cancel(self):
        self.dismiss()
