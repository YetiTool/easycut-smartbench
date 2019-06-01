'''
Created May 2019

@author: Letty

Screen to inform user when job is complete. 
'''
import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty # @UnresolvedImport


import sys, os


# Kivy UI builder:
Builder.load_string("""

<JobDoneScreen>:

    canvas:
        Color: 
            rgba: hex('#0D47A1')
        Rectangle: 
            size: self.size
            pos: self.pos
             
    BoxLayout:
        orientation: 'horizontal'
        padding: 70
        spacing: 70
        size_hint_x: 1

        BoxLayout:
            orientation: 'vertical'
            size_hint_x: 1

            Label:
                id: JobDone_label
                text_size: self.size
                size_hint_y: 0.5
                text: "Job Completed"
                markup: True
                font_size: '40sp'   
                valign: 'middle'
                halign: 'center'

                
            AnchorLayout: 
                Button:
                    size_hint_y: 1
                    background_color: hex('#FFFFFF00')
                    on_press:
                        root.quit_to_go()
                    BoxLayout:
                        padding: 25
                        size: self.parent.size
                        pos: self.parent.pos
                        Image:
                            id: image_delete
                            source: "./asmcnc/skavaUI/img/job_done.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True
                    
            Label: 
                size_hint_y: 0.2
                text: root.jobdone_text
                markup: True
                font_size: '20sp' 
                valign: 'top'
                

""")

# Intent of class is to send JobDone commands
# Commands are sent via sequential streaming, which is monitored to evaluate whether the op has completed or not

class JobDoneScreen(Screen):

    jobdone_text = StringProperty()

    def __init__(self, **kwargs):
    
        super(JobDoneScreen, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
    
    def quit_to_go(self):
        self.sm.current = 'go'