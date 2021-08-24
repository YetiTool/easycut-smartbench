'''
Created on 24 August 2020
Fake/draft job end screen
@author: Letty
'''

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

Builder.load_string("""

<FakeJobEndScreen>
    BoxLayout:
        height: dp(800)
        width: dp(480)
        canvas.before:
            Color: 
                rgba: hex('#f9f9f9ff')
            Rectangle: 
                size: self.size
                pos: self.pos

        BoxLayout:
            padding: 0
            spacing: 0
            orientation: "vertical"
            BoxLayout:
                padding: 0
                spacing: 0
                canvas:
                    Color:
                        rgba: hex('#1976d2ff')
                    Rectangle:
                        pos: self.pos
                        size: self.size
                Label:
                    size_hint: (None,None)
                    height: dp(60)
                    width: dp(800)
                    text: "Job completed!"
                    color: hex('#f9f9f9ff')
                    # color: hex('#333333ff') #grey
                    font_size: dp(30)
                    halign: "center"
                    valign: "bottom"
                    markup: True
                    text_size: self.size

            BoxLayout:
                size_hint: (None,None)
                width: dp(800)
                height: dp(420)
                padding: 0
                spacing: 10
                orientation: 'vertical'

                BoxLayout:
                    size_hint_y: None
                    height: dp(180)
                    orientation: 'horizontal'
                    padding: dp(20)


                    Label: 
                        text: root.metadata_string
                        color: hex('#333333ff') #grey
                        font_size: dp(20)
                        markup: True
                        text_size: self.size
                        halign: "left"
                        valign: "middle"

                    TextInput: 
                        text: "Production notes"
                        color: hex('#333333ff') #grey
                        font_size: dp(20)
                        markup: True
                        text_size: self.size
                        halign: "left"
                        valign: "top"
                        padding: dp(5)


                Label:
                    size_hint: (None,None)
                    height: dp(60)
                    width: dp(800)
                    text: "Did this complete successfully?"
                    # color: hex('#f9f9f9ff')
                    color: hex('#333333ff') #grey
                    font_size: dp(30)
                    halign: "center"
                    valign: "bottom"
                    markup: True

                BoxLayout:
                    size_hint: (None,None)
                    height: dp(160)
                    width: dp(800)
                    orientation: 'horizontal'
                    spacing: dp(150)
                    padding: [dp(204), 0]

                    # thumbs down button
                    Button:
                        size_hint: (None,None)
                        height: dp(160)
                        width: dp(121)
                        background_color: hex('#f9f9f9ff')
                        background_normal: ""
                        on_press: root.exit_screen()
                        BoxLayout:
                            padding: [0, dp(40), 0, 0]
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                source: "./asmcnc/apps/shapeCutter_app/img/thumbs_down.png"
                                # center_x: self.parent.center_x
                                # y: self.parent.y
                                size: self.parent.width - 40, self.parent.height - 40
                                allow_stretch: True

                    Button:
                        size_hint: (None,None)
                        height: dp(160)
                        width: dp(121)
                        background_color: hex('#f9f9f9ff')
                        background_normal: ""
                        on_press: root.exit_screen()
                        BoxLayout:
                            padding: [0, 0, 0, dp(40)]
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                source: "./asmcnc/apps/shapeCutter_app/img/thumbs_up.png"
                                # center_x: self.parent.center_x
                                # y: self.parent.y
                                size: self.parent.width - 40, self.parent.height - 40
                                allow_stretch: True  

""")

class FakeJobEndScreen(Screen):


    metadata_string = "Project_name | Step 1 of 3" + "\n" + \
        "Actual runtime: 0:30:43" + "\n"+ \
        "Total time (with pauses): 0:45:41" + "\n"+ \
        "Parts completed: 8/24"


    def __init__(self, **kwargs):
        super(FakeJobEndScreen, self).__init__(**kwargs)
        self.sm = kwargs['screen_manager']
        self.m = kwargs['machine']


    def exit_screen(self):
        self.sm.current = 'home'










