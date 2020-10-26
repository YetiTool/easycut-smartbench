'''
Created on 18 August 2020

Screen to handle door command, and allow user to resume.

@author: Letty
'''
import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty, StringProperty # @UnresolvedImport
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.animation import Animation

# Kivy UI builder:
Builder.load_string("""

<DoorScreen>:

	please_wait_message: please_wait_message
	please_wait_image: please_wait_image

    canvas:
        Color: 
            rgba: [1, 1, 1, 1]
        Rectangle: 
            size: self.size
            pos: self.pos

    BoxLayout:
        orientation: 'vertical'
        padding: 0
        spacing: 0
        size_hint: (None, None)
        height: dp(480)
        width: dp(800)

        # Alarm label
        BoxLayout: 
            padding: [15,0,0,0]
            spacing: 0
            size_hint: (None, None)
            height: dp(50)
            width: dp(800)
            Label:
                size_hint: (None, None)
                font_size: '30sp'
                text: '[b]Stop bar pushed![/b]'
                color: [0,0,0,1]
                markup: True
                halign: 'left'
                height: dp(50)
                width: dp(790)
                text_size: self.size
                size: self.parent.size
                pos: self.parent.pos

        BoxLayout: 
            padding: [10,0,10,0]
            spacing: 0
            size_hint: (None, None)
            height: dp(5)
            width: dp(800)
            Image:
                id: red_underline
                source: "./asmcnc/skavaUI/img/red_underline.png"
                center_x: self.parent.center_x
                y: self.parent.y
                size: self.parent.width, self.parent.height
                allow_stretch: True
        
        # Stop image and text
        BoxLayout: 
            padding: [30,35,30,30]
            spacing: 10
            size_hint: (None, None)
            height: dp(295)
            width: dp(800)
            orientation: 'vertical'
            BoxLayout: 
                padding: [305,20,305,20]
                size_hint: (None, None)
                height: dp(170)
                width: dp(800)       
	            Image:
	                id: stop_icon
	                source: "./asmcnc/skavaUI/img/stop.png"
	                center_x: self.parent.center_x
	                y: self.parent.y
	                size: self.parent.width, self.parent.height
	                allow_stretch: True
	                size_hint: (None, None)
	                height: dp(130)
	                width: dp(130)

            FloatLayout:
            	size_hint: (None, None)
                height: dp(50)
                width: dp(740)
	            Label:
	            	id: please_wait_message
	                size_hint: (None, None)
	                font_size: '24sp'
	                color: [0,0,0,1]
	                markup: True
	                halign: 'center'
	                valign: 'middle'
	                text_size: self.size
	                size: self.parent.size
	                pos: self.parent.pos
	                height: dp(50)
	                width: dp(740)
                Image:
                	id: please_wait_image
                    source: "./asmcnc/skavaUI/img/countdown_big.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True
                    pos: self.parent.pos
                    opacity: 0



        BoxLayout: 
            padding: [180,0,180,20]
            spacing: 220
            size_hint: (None, None)
            height: dp(130)
            width: dp(800)
            orientation: 'horizontal'

            Button:
                size_hint: (None,None)
                height: dp(110)
                width: dp(110)
                background_color: hex('#F4433600')
                center: self.parent.center
                pos: self.parent.pos
                # on_press: root.show_details()
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/skavaUI/img/cancel_from_pause.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True

            Button:
                size_hint: (None,None)
                height: dp(110)
                width: dp(110)
                background_color: hex('#F4433600')
                center: self.parent.center
                pos: self.parent.pos
                # on_press: root.show_details()
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/skavaUI/img/resume_from_pause.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True
         
            
""")


# This screen only gets activated when the PHYSICAL door pin is activated. Firmware automatically flicks to door state.

class DoorScreen(Screen):
    
    dev_win_dt = 2
    
    door_label = ObjectProperty()
    door_text = StringProperty()

    right_button = ObjectProperty()
    left_button = ObjectProperty()
    
    right_button_label = ObjectProperty()
    left_button_label = ObjectProperty()   
    
    poll_for_success = None
    quit_home = False
    
    return_to_screen = 'home'
    cancel_to_screen = 'home'

    please_wait_message = ObjectProperty()



    
    def __init__(self, **kwargs):
    
        super(DoorScreen, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']

        self.please_wait_message.text = 'Spindle is being raised, please wait...'
        self.anim_text = Animation(opacity = 0, duration=2) + Animation(opacity = 0, duration=1) + Animation(opacity = 1, duration=2) + Animation(opacity = 0, duration=1)
        self.anim_text.repeat = True
        self.anim_image = Animation(opacity = 1, duration=2) + Animation(opacity = 0, duration=1) + Animation(opacity = 0, duration=2) + Animation(opacity = 0, duration=1)
        self.anim_image.repeat = True

    def on_enter(self):    
		self.anim_text.start(self.please_wait_message)
		self.anim_image.start(self.please_wait_image)

	# def check_door_state(self):
	# 	pass
	# 	# if self.m.state() == "Door: 0":
	# 	#	 self.spindle_has_raised()


	# def spindle_has_raised(self):
	# 	self.anim_text.stop(self.please_wait_message)
	# 	self.anim_image.stop(self.please_wait_image)
	# 	self.please_wait_message.opacity = 0
	# 	self.please_wait_image.opacity = 0

