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
from kivy.metrics import dp

Builder.load_string("""
<JobFeedbackScreen>

    job_completed_label : job_completed_label
    metadata_label : metadata_label
    parts_completed_label : parts_completed_label
    post_production_notes_container : post_production_notes_container
    batch_number_container : batch_number_container
    batch_number_label : batch_number_label
    post_production_notes_label : post_production_notes_label
    post_production_notes : post_production_notes
    success_question : success_question

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
                    id: job_completed_label
                    size_hint: (None,None)
                    height: dp(60)
                    width: dp(800)
                    text: "Job completed!"
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
                                color: hex('#333333ff') #grey
                                font_size: dp(20)
                                markup: True
                                halign: "left"
                                valign: "top"
                                size: self.texture_size
                                text_size: self.size
                    
                    BoxLayout: 
                        id: post_production_notes_container
                        orientation: 'vertical'

                        BoxLayout: 
                            id: batch_number_container
                            size_hint_y: None
                            height: dp(41)
                            orientation: 'horizontal'
                            padding: [dp(0), dp(11), dp(0), dp(0)]

                            Label:
                                id: batch_number_label
                                size_hint_x: None
                                color: hex('#333333ff') #grey
                                font_size: dp(20)
                                halign: "left"
                                valign: "bottom"
                                markup: True
                                text_size: self.size

                            TextInput:
                                id: batch_number_input
                                padding: [4, 2]
                                text: ""
                                color: hex('#333333ff')
                                # foreground_color: hex('#333333ff')
                                text_size: self.size
                                size_hint_x: None
                                width: dp(100)
                                halign: "left"
                                valign: "bottom"
                                markup: True
                                font_size: dp(20)
                                multiline: False
                                background_color: hex('#e5e5e5ff')
                                text: '0'


                        Label:
                            id: post_production_notes_label
                            text: "Production notes"
                            color: hex('#333333ff') #grey
                            font_size: dp(20)
                            halign: "left"
                            valign: "top"
                            markup: True
                            text_size: self.size

                        TextInput:
                            id: post_production_notes
                            size_hint_y: None
                            height: dp(56)
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

                # FEEDBACK
                Label:
                    id: success_question
                    size_hint: (None,None)
                    height: dp(30)
                    width: dp(800)
                    text: "Did this complete successfully?"
                    # color: hex('#f9f9f9ff')
                    color: hex('#333333ff') #grey
                    font_size: dp(30)
                    halign: "center"
                    valign: "bottom"
                    markup: True

                # Feedback buttons
                BoxLayout:
                    size_hint: (None,None)
                    height: dp(240)
                    width: dp(800)
                    orientation: 'horizontal'
                    spacing: dp(96)
                    padding: [dp(150), dp(20)]

                    # Thumbs down button
                    Button:
                        size_hint: (None,None)
                        height: dp(200)
                        width: dp(202)
                        background_color: hex('#e5e5e5ff')
                        background_normal: ""
                        on_press: root.confirm_job_unsuccessful()
                        BoxLayout:
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                source: "./asmcnc/skavaUI/img/thumbs_down.png"
                                # center_x: self.parent.center_x
                                # y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True
                    # Thumbs up button
                    Button:
                        size_hint: (None,None)
                        height: dp(200)
                        width: dp(202)
                        background_color: hex('#e5e5e5ff')
                        background_normal: ""
                        on_press: root.confirm_job_successful()
                        BoxLayout:
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                source: "./asmcnc/skavaUI/img/thumbs_up.png"
                                # center_x: self.parent.center_x
                                # y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True  
""")

class JobFeedbackScreen(Screen):

    return_to_screen = StringProperty()

    # Example metadata
    metadata_string = "Project_name | Step 1 of 3" + "\n" + \
        "Actual runtime: 0:30:43" + "\n"+ \
        "Total time (with pauses): 0:45:41" + "\n"+ \
        "Parts completed: 8/24"

    def __init__(self, **kwargs):
        super(JobFeedbackScreen, self).__init__(**kwargs)

        self.sm = kwargs['screen_manager']
        self.m = kwargs['machine']
        self.l = kwargs['localization']
        self.jd = kwargs['job']
        self.db = kwargs['database']

    def on_pre_enter(self):
        self.update_strings()
        self.return_to_screen = self.jd.screen_to_return_to_after_job

    def on_enter(self):
        self.sm.get_screen('go').is_job_started_already = False

    def confirm_job_successful(self):
        self.set_post_production_notes()
        self.jd.post_job_data_update_pre_send(True)
        self.db.send_job_end(True)
        self.quit_to_return_screen()

    def confirm_job_unsuccessful(self):
        self.set_post_production_notes()
        self.sm.get_screen('job_incomplete').prep_this_screen('unsuccessful', event_number=False)
        self.sm.current = 'job_incomplete'

    def quit_to_return_screen(self):
        self.sm.current = self.return_to_screen

    def set_post_production_notes(self):
        self.jd.post_production_notes = self.post_production_notes.text

    # UPDATE TEXT WITH LANGUAGE AND VARIABLES
    def update_strings(self):

        # Get these strings properly translated

        self.job_completed_label.text = self.l.get_str("Job completed").replace(self.l.get_str("Job"), self.jd.job_name) + "!"

        if len(self.jd.metadata_dict.get('Internal Order Code', '')) > 23:
            internal_order_code =  self.jd.metadata_dict.get('Internal Order Code', '')[:23] + "..."
        else:
            internal_order_code = self.jd.metadata_dict.get('Internal Order Code', '')

        self.metadata_label.text = (
            internal_order_code + " | " + self.jd.metadata_dict.get('Process Step', '') + \
            "\n" + \
            self.l.get_str("Job duration:") + " " + self.l.get_localized_days(self.jd.actual_runtime) + \
            "\n" + \
            self.l.get_str("Pause duration:") + " " + self.l.get_localized_days(self.jd.pause_duration)
            )


        self.batch_number_label.text = self.l.get_str("Batch Number: ")
        self.batch_number_label.width = dp(len(self.batch_number_label.text)*10.5)


        self.post_production_notes.text = self.jd.post_production_notes
        self.post_production_notes_label.text = self.l.get_str("Post Production Notes:")

        self.success_question.text = self.l.get_str("Did this complete successfully?")

        try:
            parts_completed_if_job_successful = int(self.jd.metadata_dict.get('Parts Made So Far', 0)) + int(self.jd.metadata_dict.get('Parts Made Per Job', 1))

            self.parts_completed_label.text = (
                self.l.get_str("Parts completed:") + " " + str(parts_completed_if_job_successful) + "/" + str(int(self.jd.metadata_dict.get('Total Parts Required', 1)))
                )

        except: 
            self.l.get_str("Parts completed:") + " 1/1"

