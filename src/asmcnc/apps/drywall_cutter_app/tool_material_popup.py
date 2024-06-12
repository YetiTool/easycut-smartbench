from kivy.uix.popup import Popup
from kivy.lang import Builder
import json

Builder.load_string("""
<Options@SpinnerOption>

    background_normal: ''
    size: self.size
    color: hex('#333333ff')
    halign: 'center'
    markup: 'True'
    font_size: 0.0175*app.width
    background_color: 0,0,0,0
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
    MATERIAL_DB = 'asmcnc/job/database/material_database.json'
    PROFILE_DB = 'asmcnc/job/database/profile_database.json'
    TOOL_DB = 'asmcnc/job/database/tool_database.json'

    def __init__(self, localization, **kwargs):
        super(ToolMaterialPopup, self).__init__(**kwargs)

        self.tool_dropdown.bind(text=self.on_tool_change)
        self.material_dropdown.bind(text=self.on_material_change)

        self.material_data = None
        self.tool_data = None
        self.profile_data = None

    def on_tool_change(self, instance, value):
        print("Tool changed to ", value)

    def on_material_change(self, instance, value):
        print("Material changed to ", value)
        self.tool_dropdown.values = self.get_tools(value)

    def on_open(self):
        # Load the material, tool and profile data
        with open(self.MATERIAL_DB) as f:
            self.material_data = json.load(f)

        with open(self.TOOL_DB) as f:
            self.tool_data = json.load(f)

        with open(self.PROFILE_DB) as f:
            self.profile_data = json.load(f)

        # Set the material dropdown values
        self.material_dropdown.values = [material['description'] for material in self.material_data]

    def get_tools(self, chosen_material=None):
        if not chosen_material:
            tool_names = [tool['description'] for tool in self.tool_data]
            return tool_names

        material_id = [material['uid'] for material in self.material_data if material['description'] == chosen_material][0]
        profile_ids = [profile['uid'] for profile in self.profile_data if profile['material']['uid'] == material_id]

        tool_names = []

        for profile in self.profile_data:
            if profile['uid'] in profile_ids:
                for tool in profile['applicable_tools']:
                    tool_names.append(tool['description'])

        return tool_names

    def confirm(self):
        self.dismiss()

    def cancel(self):
        self.dismiss()
