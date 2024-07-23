from kivy.app import App
from kivy.uix.popup import Popup
from kivy.lang import Builder

from asmcnc.comms.localization import Localization
from asmcnc.comms.logging_system.logging_system import Logger

from asmcnc.core_UI import scaling_utils

Builder.load_string("""
#:import paths asmcnc.paths

<Options@SpinnerOption>

    background_normal: ''
    size: self.size
    color: hex('#333333ff')
    halign: 'left'
    markup: 'True'
    font_size: 0.0175*app.width
    background_color: color_provider.get_rgba('black')
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
    halign: 'left'
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
    float_layout:float_layout
    title_label:title_label
    description_label:description_label
    lead_in_warning_label:lead_in_warning_label
    cutter_link_label:cutter_link_label

    auto_dismiss: False
    size_hint: (None,None)
    size: (dp(app.get_scaled_width(577)), dp(app.get_scaled_height(350)))
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
            pos_hint: {'x': -0.31, 'y': 0.61 if app.width == 800 else 0.64}
            text: root.l.get_str('Tool & Material selection')
            font_size: app.get_scaled_sp('20sp')
            color: hex('#F9F9F9')
        
        Label:
            id: description_label
            text: root.l.get_str('Shapes only supports YetiPilot profiles.')
            halign: 'center'
            color: hex('#333333')
            size_hint: (0.75, None)
            pos_hint: {'center_x': 0.5, 'center_y': 0.95}
            font_size: app.get_scaled_sp('16sp')
            
        Image:
            id: material_label
            source: paths.get_resource('material_icon.png')
            pos_hint: {'center_x': 0.1, 'center_y': 0.75}
            allow_stretch: True
            size_hint: None, None
            size: app.get_scaled_width(68), app.get_scaled_height(29)

        Choices:
            id: material_dropdown
            size_hint: (0.7, 0.13)
            pos_hint: {'center_x': 0.55, 'center_y': 0.75}

        Image:
            id: tool_label
            source: paths.get_resource('tool_icon.png')
            pos_hint: {'center_x': 0.1, 'center_y': 0.55}
            size_hint: None, None
            size: app.get_scaled_width(68), app.get_scaled_height(16)
            allow_stretch: True

        Choices:
            id: tool_dropdown
            size_hint: (0.7, 0.13)
            pos_hint: {'center_x': 0.55, 'center_y': 0.55}
            
        Label:
            id: lead_in_warning_label
            text: root.l.get_str('WARNING: Using a compression tool will add a lead in to your toolpath automatically')
            text_size: (0.65*self.parent.width, None)
            pos_hint: {'center_x': 0.5, 'center_y': 0.40}
            color: hex('#333333')
            size_hint: (0.75, None)
            halign: 'center'
            opacity: 0
            font_size: app.get_scaled_sp('16sp')
            
        Label:
            id: cutter_link_label
            text: root.l.get_str('Yeti Tool cutters available from <url>').replace('<url>', 'www.yetitool.com/about/partners')
            pos_hint: {'center_x': 0.5, 'center_y': 0.25}
            color: hex('#333333')
            halign: 'center'
            font_size: app.get_scaled_sp('16sp')
            text_size: (0.65*self.parent.width, None)
            
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

    l = Localization()

    def __init__(self, localization, config, drywall_cutter_screen, **kwargs):
        super(ToolMaterialPopup, self).__init__(**kwargs)

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

            tool = self.profile_db.get_tool_by_description(value)
            if tool['generic_definition']['required_operations']['lead_in'] and False:  # Disabled for now
                self.ids['lead_in_warning_label'].opacity = 1
                return

        # Always hide the warning if the tool is not a compression tool
        self.ids['lead_in_warning_label'].opacity = 0

    def on_material_change(self, instance, value):
        Logger.debug("Material changed to " + value)
        self.tool_dropdown.values = self.profile_db.get_tool_names(self.profile_db.get_material_id(value))
        self.tool_dropdown.text = ''
        self.confirm_button.disabled = True
        self.confirm_button.opacity = 0.5

    def on_open(self):
        # Fix weird scaling bug with title label
        self.title_label.pos_hint['x'] = 0
        if scaling_utils.is_screen_big():
            self.title_label.pos_hint['y'] = 1.1
        else:
            self.title_label.pos_hint['y'] = 1.075
        self.float_layout.do_layout()
        #self.update_strings()
        self.load_config()
        if self.material_dropdown.text == '' or self.material_dropdown.text == '':  # Only disable if one is empty
            self.confirm_button.disabled = True
            self.confirm_button.opacity = 0.5

    def update_strings(self):
        self.title_label.text = self.l.get_str('Tool & Material selection')
        self.description_label.text = self.l.get_str('Shapes only supports YetiPilot profiles.')
        self.lead_in_warning_label.text = self.l.get_str('WARNING: Using a compression tool will add a lead in to your toolpath automatically')
        self.cutter_link_label.text = self.l.get_str('Yeti Tool cutters available from') + ' www.yetitool.com/about/partners'

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
