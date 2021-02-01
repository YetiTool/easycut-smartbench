'''
Created on 1 February 2021
@author: Letty

Screen to provide user with important safety information prior to every job start.
'''

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_string("""

#:import hex kivy.utils.get_color_from_hex


<JobstartWarningScreen>:

	Button: 
		on_press: root.continue_to_go_screen()

""")



class JobstartWarningScreen(Screen):


    def __init__(self, **kwargs):

        super(JobstartWarningScreen, self).__init__(**kwargs)
        self.m=kwargs['machine']
        self.sm=kwargs['screen_manager']


    def continue_to_go_screen(self):
    	self.sm.current = 'go'

