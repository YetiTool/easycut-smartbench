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
    parts_completed_container : parts_completed_container
    parts_completed_label : parts_completed_label
    parts_completed_input : parts_completed_input
    out_of_total_parts_label : out_of_total_parts_label
    production_notes_container : production_notes_container
    production_notes_label : production_notes_label
    production_notes : production_notes
    job_cancelled_label : job_cancelled_label
    # event_details_container : event_details_container
    event_details_label : event_details_label
    # event_details_input : event_details_input

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

                    BoxLayout:
                        orientation: 'vertical'
                    
                        Label: 
                            id: metadata_label
                            size_hint_y: None
                            height: dp(90)
                            color: hex('#333333ff') #grey
                            font_size: dp(20)
                            markup: True
                            text_size: self.size
                            halign: "left"
                            valign: "bottom"

                        BoxLayout:
                            id: parts_completed_container
                            size_hint_y: None
                            height: dp(30)
                            orientation: 'horizontal'

                            Label: 
                                id: parts_completed_label
                                text: "Parts completed: "
                                color: hex('#333333ff') #grey
                                font_size: dp(20)
                                markup: True
                                halign: "left"
                                valign: "top"
                                size: self.texture_size
                                text_size: self.size
                                # pos: metadata_label.x, self.y

                            TextInput:
                                id: parts_completed_input
                                padding: [4, 2]
                                size_hint_x: None
                                width: dp(50)
                                text: '0'
                                color: hex('#333333ff')
                                text_size: self.size
                                halign: "left"
                                valign: "top"
                                markup: True
                                font_size: dp(20)
                                multiline: False
                                background_color: hex('#e5e5e5ff')
                                input_filter: 'int'

                            Label: 
                                id: out_of_total_parts_label
                                text: ""
                                color: hex('#333333ff') #grey
                                font_size: dp(20)
                                markup: True
                                text_size: self.size
                                halign: "left"
                                valign: "top"
                    
                    BoxLayout: 
                        id: production_notes_container
                        orientation: 'vertical'
                        Label:
                            id: production_notes_label
                            size_hint_y: None
                            height: dp(41)
                            text: "Production notes"
                            color: hex('#333333ff') #grey
                            font_size: dp(20)
                            halign: "left"
                            valign: "bottom"
                            markup: True
                            text_size: self.size

                        TextInput:
                            id: production_notes
                            size_hint_y: None
                            height: dp(79)
                            padding: [4, 2]
                            text: ""
                            color: hex('#333333ff')
                            # foreground_color: hex('#333333ff')
                            text_size: self.size
                            halign: "left"
                            valign: "top"
                            markup: True
                            font_size: dp(20)
                            multiline: True
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

                    Label: 
                        id: event_details_label
                        padding: [dp(20), dp(0)]
                        color: hex('#333333ff') #grey
                        text_size: self.size
                        halign: "left"
                        valign: "middle"
                        markup: True
                        font_size: dp(20)

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
    event_type = '' # alarm, error, cancelled, or unsuccessful
    specific_event = ''

    def __init__(self, **kwargs):
        super(JobIncompleteScreen, self).__init__(**kwargs)

        self.sm = kwargs['screen_manager']
        self.m = kwargs['machine']
        self.l = kwargs['localization']
        self.jd = kwargs['job']
        self.db = kwargs['database']

    def prep_this_screen(self, event, event_number=False):
        self.event_type = event
        if event_number: self.specific_event = str(event_number.split(':')[1])

    def on_pre_enter(self):
        self.update_strings()
        self.return_to_screen = self.jd.screen_to_return_to_after_cancel

    def on_enter(self):
        self.sm.get_screen('go').is_job_started_already = False
 
    def press_ok(self):
        self.set_production_notes()
        self.jd.post_job_data_update_pre_send(False, extra_parts_completed=self.parts_completed_input.text)
        self.send_job_status()
        self.quit_to_return_screen()

    def quit_to_return_screen(self):
        self.sm.current = self.jd.screen_to_return_to_after_job

    def set_production_notes(self):
        self.jd.production_notes = self.production_notes.text

    def send_job_status(self):
        if 'cancelled' in self.event_type or 'unsuccessful' in self.event_type:
            self.db.send_event(0, 'Job cancelled', self.job_cancelled_label.text, 5)

        elif 'Alarm' in self.event_type:
            self.db.send_event(2, 'Job cancelled', 'Cancelled job (Alarm): ' + self.jd.job_name, 5)

        elif 'Error' in self.event_type:
            self.db.send_event(2, 'Job cancelled', 'Cancelled job (Error): ' + self.jd.job_name, 5)

        self.db.send_full_payload()
        self.db.send_job_end(self.jd.job_name, False)


    # UPDATE TEXT WITH LANGUAGE AND VARIABLES
    def update_strings(self):


        # Get these strings properly translated

        if "unsuccessful" in self.event_type:
            self.job_incomplete_label.text = self.l.get_str("Job unsuccessful").replace(self.l.get_str("Job"), self.jd.job_name) + "!"

        else:
            self.job_incomplete_label.text = self.l.get_str("Job incomplete").replace(self.l.get_str("Job"), self.jd.job_name) + "!"

        current_step = str(int(self.jd.metadata_dict.get('Parts Completed So Far', 1))/int(self.jd.metadata_dict.get('Parts Per Job', 1)))
        total_steps = str(int(self.jd.metadata_dict.get('Total Parts Required', 1))/int(self.jd.metadata_dict.get('Parts Per Job', 1)))


        if len(self.jd.metadata_dict.get('Project Name', self.jd.job_name)) > 23:
            project_name =  self.jd.metadata_dict.get('Project Name', self.jd.job_name)[:23] + "..."
        else:
            project_name = self.jd.metadata_dict.get('Project Name', self.jd.job_name)

        self.metadata_label.text = (
            project_name + " | " + (self.l.get_str('Step X of Y').replace("X", current_step)).replace("Y", total_steps) + \
            "\n" + \
            self.l.get_str("Job duration:") + " " + self.l.get_localized_days(self.jd.actual_runtime) + \
            "\n" + \
            self.l.get_str("Pause duration:") + " " + self.l.get_localized_days(self.jd.pause_duration)
            )

        self.parts_completed_input.text = str(self.jd.metadata_dict.get('Parts Completed So Far', 0))
        self.out_of_total_parts_label.text = " / " + str(self.jd.metadata_dict.get('Total Parts Required', 1))

        self.production_notes.text = self.jd.production_notes
        self.production_notes_label.text = self.l.get_str("Production Notes")


        if_loss = self.l.get_str("If SmartBench lost position, you will need to rehome SmartBench.")
        may_loss = self.l.get_str("SmartBench may have lost position, so you will need to rehome SmartBench.")
        recovery_msg = self.l.get_str("You should recover any finished parts from this job before starting a new job.")
        percent_streamed = self.l.get_str("Percentage streamed:") + " " + str(self.jd.percent_thru_job) + " %"


        if 'cancelled' in self.event_type:
            self.job_cancelled_label.text = self.l.get_str("Job cancelled by the user.")
            self.event_details_label.text = percent_streamed + "\n" + if_loss + "\n" + recovery_msg

        elif "unsuccessful" in self.event_type:
            self.job_cancelled_label.text = self.l.get_str("Job marked unsuccessful by the user.")
            self.event_details_label.text = percent_streamed + "\n" + if_loss + "\n" + recovery_msg

        else:
            self.job_cancelled_label.text = (
                self.l.get_str("Job cancelled due to event").replace(self.l.get_str("event"), self.l.get_str(self.event_type) + \
                ": " + self.specific_event)
                )

            self.event_details_label.text = percent_streamed + "\n" + may_loss + "\n" + recovery_msg
        
            if 'Error' in self.event_type:
                self.event_details_label.text = self.event_details_label.text + "\n" + self.l.get_str("Check your GCode file before re-running it.")
