'''
Created on 5 March 2020
Job Cancelled Screen for the Shape Cutter App

@author: Letty
'''

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen


Builder.load_string("""

<ShapeCutterExitScreenClass>:
    
    BoxLayout:
        height: dp(800)
        width: dp(480)
        canvas:
            Rectangle: 
                pos: self.pos
                size: self.size
                source: "./asmcnc/apps/shapeCutter_app/img/landing_background.png"

        BoxLayout:
            padding: 0
            spacing: 0
            orientation: "vertical"       
                
            Label:
                size_hint: (None,None)
                height: dp(90)
                width: dp(800)
                text: "Leaving Shape Cutter..."
                font_size: 30
                halign: "center"
                valign: "bottom"
                markup: True
                   
                    
            BoxLayout:
                size_hint: (None,None)
                width: dp(800)
                height: dp(390)
                padding: 0,110,0,110
                spacing: 0
                Label:
                    size_hint: (None,None)
                    height: dp(170)
                    width: dp(800)
                    halign: "center"
                    valign: "middle"
                    text: "Bye!"
                    color: 0,0,0,1
                    font_size: 26
                    markup: True

""")

class ShapeCutterExitScreenClass(Screen):

    info_button = ObjectProperty()   
    
    def __init__(self, **kwargs):
        super(ShapeCutterExitScreenClass, self).__init__(**kwargs)
        self.shapecutter_sm = kwargs['shapecutter']
        self.m=kwargs['machine']

        
        

    def on_enter(self):
        self.poll_for_success = Clock.schedule_once(self.exit_screen, 1.5)
 
    def exit_screen(self, dt):
        self.shapecutter_sm.return_to_EC()
        
    def on_pre_leave(self):
        self.purge_screens()
    
    def on_leave(self):
        self.sm.remove_widget(self.sm.get_screen('sCexit'))
    
    def purge_screens(self):
        self.sm.remove_widget(self.sm.get_screen('sClanding'))
        self.sm.remove_widget(self.sm.get_screen('sCdimensions'))
        self.sm.remove_widget(self.sm.get_screen('sCApIs'))
        
        self.sm.remove_widget(self.sm.get_screen('sC1'))
        self.sm.remove_widget(self.sm.get_screen('sC2'))
        self.sm.remove_widget(self.sm.get_screen('sC3'))
        self.sm.remove_widget(self.sm.get_screen('sC4'))
        self.sm.remove_widget(self.sm.get_screen('sC5'))
        self.sm.remove_widget(self.sm.get_screen('sC6'))
        self.sm.remove_widget(self.sm.get_screen('sC7'))
        self.sm.remove_widget(self.sm.get_screen('sC8'))
        self.sm.remove_widget(self.sm.get_screen('sC9'))
        self.sm.remove_widget(self.sm.get_screen('sC10'))
        self.sm.remove_widget(self.sm.get_screen('sC11'))
        self.sm.remove_widget(self.sm.get_screen('sC12'))
        self.sm.remove_widget(self.sm.get_screen('sC13'))
        self.sm.remove_widget(self.sm.get_screen('sC14'))
        self.sm.remove_widget(self.sm.get_screen('sC15'))
        self.sm.remove_widget(self.sm.get_screen('sC16'))
        self.sm.remove_widget(self.sm.get_screen('sC17'))
        self.sm.remove_widget(self.sm.get_screen('sC18'))
        self.sm.remove_widget(self.sm.get_screen('sC19'))
        self.sm.remove_widget(self.sm.get_screen('sC20'))
        self.sm.remove_widget(self.sm.get_screen('sC21'))
        self.sm.remove_widget(self.sm.get_screen('sC22'))
        self.sm.remove_widget(self.sm.get_screen('sC23'))
        self.sm.remove_widget(self.sm.get_screen('sC24'))
        self.sm.remove_widget(self.sm.get_screen('sC25'))
        self.sm.remove_widget(self.sm.get_screen('sC26'))
        self.sm.remove_widget(self.sm.get_screen('sC27'))
        self.sm.remove_widget(self.sm.get_screen('sC28'))
        self.sm.remove_widget(self.sm.get_screen('sC29'))
        self.sm.remove_widget(self.sm.get_screen('sC30'))
        self.sm.remove_widget(self.sm.get_screen('sC31'))
        self.sm.remove_widget(self.sm.get_screen('sC32'))
        self.sm.remove_widget(self.sm.get_screen('sC33'))
        self.sm.remove_widget(self.sm.get_screen('sC34'))
        self.sm.remove_widget(self.sm.get_screen('sC35'))
        self.sm.remove_widget(self.sm.get_screen('sC36'))
        
        if self.sm.has_screen('sCsavejob'):        
            self.sm.remove_widget(self.sm.get_screen('sCsavejob'))
            self.sm.remove_widget(self.sm.get_screen('sCfeedback'))
            self.sm.remove_widget(self.sm.get_screen('sCrepeat'))

