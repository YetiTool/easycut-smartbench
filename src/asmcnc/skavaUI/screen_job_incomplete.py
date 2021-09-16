'''
Created on 13th September 2021
End of job screen with feedback and metadata sending
@author: Letty
'''
from datetime import datetime, timedelta

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivy.clock import Clock

Builder.load_string("""
<JobIncompleteScreen>

    job_incomplete_label : job_incomplete_label
    metadata_label : metadata_label
    production_notes_container : production_notes_container
    production_notes_label : production_notes_label
    production_notes : production_notes
    job_cancelled_label : job_cancelled_label
    event_details_container : event_details_container
    event_details_label : event_details_label
    event_details_input : event_details_input

    BoxLayout:
        height: dp(800)
        width: dp(480)
        canvas.before:
            Color: 
                rgba: hex('#e5e5e5ff')
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

                # HEADER
                Label:
                    id: job_incomplete_label
                    size_hint: (None,None)
                    height: dp(60)
                    width: dp(800)
                    text: "Job.nc incomplete!"
                    color: hex('#f9f9f9ff')
                    font_size: dp(30)
                    halign: "center"
                    valign: "middle"
                    markup: True
                    text_size: self.size
            # BODY
            BoxLayout:
                size_hint: (None,None)
                width: dp(800)
                height: dp(420)
                padding: [dp(0), dp(10)]
                spacing: 0
                orientation: 'vertical'
                
                # METADATA AND PRODUCTION NOTES
                BoxLayout:
                    size_hint_y: None
                    height: dp(130)
                    orientation: 'horizontal'
                    padding: [dp(20), dp(0), dp(20), dp(10)]
                    
                    Label: 
                        id: metadata_label
                        color: hex('#333333ff') #grey
                        font_size: dp(24)
                        markup: True
                        text_size: self.size
                        halign: "left"
                        valign: "middle"
                    
                    BoxLayout: 
                        id: production_notes_container
                        orientation: 'vertical'

                        Button:
                            id: production_notes_label
                            background_color: hex('#e5e5e5ff')
                            background_normal: ""
                            background_down: ""
                            color: hex('#1976d2ff')
                            text_size: self.size
                            halign: "left"
                            valign: "middle"
                            markup: True
                            font_size: dp(24)
                            size_hint_y: None
                            height: self.parent.height
                            opacity: 1
                            on_press: root.open_production_notes_text_input()
                            focus_next: production_notes
                            text: "<add your post-production notes here>"

                        TextInput:
                            id: production_notes
                            padding: [4, 2]
                            text: ""
                            color: hex('#333333ff')
                            foreground_color: hex('#333333ff')
                            text_size: self.size
                            halign: "left"
                            valign: "top"
                            markup: True
                            font_size: dp(20)
                            size_hint_y: None
                            height: dp(0)
                            opacity: 0
                            disabled: True
                            multiline: True
                            background_active: ""
                            background_normal: ""
                            background_color: hex('#e5e5e5ff')

                # EVENT DETAILS
                Label:
                    id: job_cancelled_label
                    size_hint: (None,None)
                    height: dp(30)
                    width: dp(800)
                    text: "Job cancelled due to an event."
                    # color: hex('#f9f9f9ff')
                    color: hex('#333333ff') #grey
                    font_size: dp(30)
                    halign: "center"
                    valign: "bottom"
                    markup: True

                # Event details
                BoxLayout:
                    size_hint: (None,None)
                    height: dp(240)
                    width: dp(800)
                    orientation: 'vertical'
                    spacing: 0
                    padding: [dp(0), dp(0)]

                    BoxLayout: 
                        id: event_details_container
                        orientation: 'vertical'
                        padding: [dp(20), dp(0)]

                        Button:
                            id: event_details_label
                            background_color: hex('#e5e5e5ff')
                            background_normal: ""
                            background_down: ""
                            background_disabled_normal: ""
                            background_disabled_down: ""
                            color: hex('#333333ff') #grey
                            # color: hex('#1976d2ff') # blue
                            text_size: self.size
                            halign: "left"
                            valign: "middle"
                            markup: True
                            font_size: dp(18)
                            size_hint_y: None
                            height: self.parent.height
                            opacity: 1
                            on_press: root.open_event_details_text_input()
                            focus_next: event_details_input

                        TextInput:
                            id: event_details_input
                            padding: [4, 2]
                            text: ""
                            color: hex('#333333ff')
                            foreground_color: hex('#333333ff')
                            text_size: self.size
                            halign: "left"
                            valign: "middle"
                            markup: True
                            font_size: dp(18)
                            size_hint_y: None
                            height: dp(0)
                            opacity: 0
                            disabled: True
                            multiline: True
                            background_active: ""
                            background_normal: ""
                            background_color: hex('#e5e5e5ff')

                    # Buttons
                    BoxLayout: 
                        padding: [10,0,10,10]
                        size_hint: (None, None)
                        height: dp(142)
                        width: dp(800)
                        orientation: 'horizontal'
                        BoxLayout: 
                            size_hint: (None, None)
                            height: dp(132)
                            width: dp(244.5)
                            padding: [0, 0, 184.5, 0]

                        BoxLayout: 
                            size_hint: (None, None)
                            height: dp(132)
                            width: dp(291)
                            padding: [0,0,0,dp(52)]
                            Button:
                                id: next_button
                                background_normal: "./asmcnc/apps/warranty_app/img/next.png"
                                background_down: "./asmcnc/apps/warranty_app/img/next.png"
                                border: [dp(14.5)]*4
                                size_hint: (None,None)
                                width: dp(291)
                                height: dp(79)
                                on_press: root.press_ok()
                                text: 'OK'
                                font_size: '30sp'
                                color: hex('#f9f9f9ff')
                                markup: True
                                center: self.parent.center
                                pos: self.parent.pos
                        BoxLayout: 
                            size_hint: (None, None)
                            height: dp(132)
                            width: dp(244.5)
                            padding: [193.5, 0, 0, 0]
 
""")

class JobIncompleteScreen(Screen):

    return_to_screen = StringProperty()
    event_type = 'user' # alarm, error, or user
    specific_event = 'error:13" : "Interrupt bar detected as pressed. Check all four contacts at the interrupt bar ends are not pressed. Pressing each switch a few times may clear the contact.'

    # # # Example metadata
    # metadata_string = "Project_name | Step 1 of 3" + "\n" + \
    #     "Actual runtime: 0:30:43" + "\n"+ \
    #     "Total time (with pauses): 0:45:41" + "\n"+ \
    #     "Percentage streamed: 43 %"


    # event_deets_test_string = (
    #     "Error 1: You fucked up your code. " + \
    #     "\n" + \
    #     "Check the gcode file before re-running it." + \
    #     " " + \
    #     "Recover any parts from this job before rehoming and starting a new job."
    #     )


    def __init__(self, **kwargs):
        super(JobIncompleteScreen, self).__init__(**kwargs)

        self.sm = kwargs['screen_manager']
        self.m = kwargs['machine']
        self.l = kwargs['localization']
        self.jd = kwargs['job']
        self.db = kwargs['database']

    def prep_this_screen(self, event, event_number=False):
        self.event_type = event
        if event_number: self.specific_event = event_number

    def on_pre_enter(self):
        self.close_production_notes_text_input()
        self.close_event_details_text_input()
        self.update_strings()
        self.return_to_screen = self.jd.screen_to_cancel_to_after_job

    def on_enter(self):
        self.sm.get_screen('go').is_job_started_already = False
        # self.sm.get_screen('go').loop_for_job_progress = None

    def press_ok(self):
        self.set_production_notes()
        self.set_event_notes()
        self.db.send_job_end(self.jd.job_name, False)
        self.quit_to_return_screen()

    def quit_to_return_screen(self):
        self.sm.current = self.jd.screen_to_return_to_after_job

    # PRODUCTION NOTES
    def set_focus_on_production_notes(self, dt):
        self.production_notes.focus = True

    def open_production_notes_text_input(self):
        
        self.production_notes_label.disabled = True
        self.production_notes.disabled = False
        self.production_notes_label.height = 0
        self.production_notes_label.opacity = 0
        self.production_notes.height = self.production_notes_container.height
        self.production_notes.opacity = 1
        self.production_notes_label.focus = False

        Clock.schedule_once(self.set_focus_on_production_notes, 0.3)

    def close_production_notes_text_input(self):

        self.production_notes.focus = False
        self.production_notes.disabled = True
        self.production_notes_label.disabled = False
        self.production_notes.height = 0
        self.production_notes.opacity = 0
        self.production_notes_label.height = self.production_notes_container.height
        self.production_notes_label.opacity = 1

    def set_production_notes(self):
        self.jd.metadata_dict['ProductionNotes'] = self.production_notes.text


    # EVENT NOTES
    def set_focus_on_event_details(self, dt):
        self.event_details_input.focus = True

    def open_event_details_text_input(self):

        if self.event_type == "user":
        
            self.event_details_label.disabled = True
            self.event_details_input.disabled = False
            self.event_details_label.height = 0
            self.event_details_label.opacity = 0
            self.event_details_input.height = self.event_details_container.height
            self.event_details_input.opacity = 1
            self.event_details_label.focus = False

            Clock.schedule_once(self.set_focus_on_event_details, 0.3)

    def close_event_details_text_input(self):

        self.event_details_input.focus = False
        self.event_details_label.disabled = False
        self.event_details_input.disabled = True
        self.event_details_input.height = 0
        self.event_details_input.opacity = 0
        self.event_details_label.height = self.event_details_container.height
        self.event_details_label.opacity = 1

    def set_event_notes(self):
        # Archie not sure how you wanna skin this :) 
        pass

    # UPDATE TEXT WITH LANGUAGE AND VARIABLES
    def update_strings(self):

        # Get these strings properly translated
        self.job_incomplete_label.text = self.l.get_str("Job incomplete").replace(self.l.get_str("Job"), self.jd.job_name) + "!"

        current_step = str(self.jd.metadata_dict.get('PartsCompletedSoFar', 1)/self.jd.metadata_dict.get('PartsPerJob', 1))
        total_steps = str(self.jd.metadata_dict.get('TotalNumberOfPartsRequired', 1)/self.jd.metadata_dict.get('PartsPerJob', 1))

        self.metadata_label.text = (
            self.jd.metadata_dict.get('ProjectName', self.jd.job_name) + " | " + \
            (self.l.get_str('Step X of Y').replace("X", current_step)).replace("Y", total_steps) + \
            "\n" + \
            self.l.get_str("Actual runtime:") + " " + self.jd.actual_runtime + \
            "\n" + \
            self.l.get_str("Total time (with pauses):") + " " + self.jd.total_time + \
            "\n" + \
            self.l.get_str("Percentage streamed:") + " " + str(self.jd.percent_thru_job) + " %"
            )

        self.jd.metadata_dict['ProductionNotes'] = ''
        self.production_notes.text = ''
        self.production_notes_label.text = "<" + self.l.get_str("add your post-production notes here") + ">"

        if 'user' in self.event_type:
            self.event_details_label.color = [25 / 255., 118 / 255., 210 / 255., 1.]
            self.job_cancelled_label.text = self.l.get_str("Job cancelled by the user.")
            self.event_details_label.text = "<" + self.l.get_str("add your reason for cancellation here") + ">"

        else:
            self.event_details_label.color = [51 / 255., 51 / 255., 51 / 255., 1.]
            self.job_cancelled_label.text = self.l.get_str("Job cancelled due to an event.").replace(self.l.get_str("event"), self.l.get_str(self.event_type))
            lost_position_message = self.l.get_str("Recover any parts from this job before rehoming and starting a new job.")

            if 'alarm' in self.event_type:
                self.event_details_label.text = (
                    self.specific_event + \
                    "\n" + \
                    lost_position_message
                    )            
        
            elif 'error' in self.event_type:
                error_resolution_message = self.l.get_str('Check the gcode file before re-running it.')
                self.event_details_label.text = (
                    self.specific_event + \
                    "\n" + \
                    error_resolution_message + \
                    " " + \
                    lost_position_message
                    )

