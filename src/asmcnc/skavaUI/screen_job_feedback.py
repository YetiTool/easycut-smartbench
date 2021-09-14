'''
Created on 13th September 2021
End of job screen with feedback and metadata sending
@author: Letty
'''

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivy.clock import Clock

Builder.load_string("""
<JobFeedbackScreen>

    job_completed_label : job_completed_label
    metadata_label : metadata_label
    production_notes_container : production_notes_container
    production_notes_label : production_notes_label
    production_notes : production_notes
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
                        id: metadata_label
                        color: hex('#333333ff') #grey
                        font_size: dp(20)
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
                            color: hex('#333333ff')
                            text_size: self.size
                            halign: "left"
                            valign: "top"
                            markup: True
                            font_size: dp(20)
                            size_hint_y: None
                            height: self.parent.height
                            opacity: 1
                            on_press: root.open_production_notes_text_input()
                            focus_next: production_notes

                        TextInput:
                            id: production_notes
                            padding: [4, 2]
                            text: ""
                            color: hex('#333333ff')
                            text_size: self.size
                            halign: "left"
                            valign: "top"
                            markup: True
                            font_size: dp(20)
                            size_hint_y: None
                            height: dp(0)
                            opacity: 0
                            on_text_validate: root.close_production_notes_text_input()
                            disabled: True
                            multiline: True

                Label:
                    id: success_question
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
                    spacing: dp(96)
                    padding: [dp(200), 0, dp(200), dp(10)]
                    # thumbs down button
                    Button:
                        size_hint: (None,None)
                        height: dp(150)
                        width: dp(152)
                        background_color: hex('#e5e5e5ff')
                        background_normal: ""
                        on_press: root.confirm_job_successful()
                        BoxLayout:
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                source: "./asmcnc/skavaUI/img/thumbs_down.png"
                                # center_x: self.parent.center_x
                                # y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True
                    Button:
                        size_hint: (None,None)
                        height: dp(150)
                        width: dp(152)
                        background_color: hex('#e5e5e5ff')
                        background_normal: ""
                        on_press: root.confirm_job_unsuccessful()
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

    # # Example metadata
    # metadata_string = "Project_name | Step 1 of 3" + "\n" + \
    #     "Actual runtime: 0:30:43" + "\n"+ \
    #     "Total time (with pauses): 0:45:41" + "\n"+ \
    #     "Parts completed: 8/24"

    def __init__(self, **kwargs):
        super(JobFeedbackScreen, self).__init__(**kwargs)

        self.sm = kwargs['screen_manager']
        self.m = kwargs['machine']
        self.l = kwargs['localization']
        self.jd = kwargs['job']
        self.db = kwargs['database']

    def prep_this_screen(self, screen_to_exit_to, actual_runtime, total_time):
        self.update_strings(actual_runtime, total_time)
        self.return_to_screen = screen_to_exit_to

    def on_enter(self):
        self.sm.get_screen('go').is_job_started_already = False
        # self.sm.get_screen('go').loop_for_job_progress = None
        self.db.send_job_end(self.jd.job_name)

    def confirm_job_successful(self):
        self.set_production_notes()
        # Archie please add what needs sending here as approp
        self.quit_to_return_screen()

    def confirm_job_unsuccessful(self):
        self.set_production_notes()
        # Archie please add what needs sending here as approp
        self.quit_to_return_screen()

    def quit_to_return_screen(self):
        self.sm.current = self.return_to_screen
        

    # PRODUCTION NOTES
    def set_focus_on_production_notes(self, dt):
        self.production_notes.focus = True

    def open_production_notes_text_input(self):
        
        self.production_notes_label.disabled = True
        self.production_notes.disabled = False
        self.production_notes_label.height = 0
        self.production_notes_label.opacity = 0

        print("Height: " + str(self.production_notes_container.height))

        self.production_notes.height = self.production_notes_container.height
        self.production_notes.opacity = 1
        self.production_notes_label.focus = False

        Clock.schedule_once(self.set_focus_on_production_notes, 0.3)

    def close_production_notes_text_input(self):

        self.set_production_notes()

        self.production_notes.focus = False
        self.production_notes.disabled = True
        self.production_notes_label.disabled = False
        self.production_notes.height = 0
        self.production_notes.opacity = 0

        print("Height: " + str(self.production_notes_container.height))

        self.production_notes_label.height = self.production_notes_container.height
        self.production_notes_label.opacity = 1

    def set_production_notes(self):
        if self.production_notes.focus:
            self.jd.metadata_dict['ProductionNotes'] = self.production_notes.text
            self.production_notes_label.text = self.production_notes.text

    # UPDATE TEXT WITH LANGUAGE AND VARIABLES
    def update_strings(self, actual_runtime, total_time):

        # Add these strings to language dict

        self.job_completed_label.text = self.l.get_str("Job completed").replace(self.l.get_str("Job"), self.jd.job_name)

        current_step = str(self.jd.metadata_dict.get('PartsCompletedSoFar', 1)/self.jd.metadata_dict.get('PartsPerJob', 1))
        total_steps = str(self.jd.metadata_dict.get('TotalNumberOfPartsRequired', 1)/self.jd.metadata_dict.get('PartsPerJob', 1))

        self.metadata_label.text = (
            self.jd.metadata_dict.get('ProjectName', self.jd.job_name) + " | " + \
            (self.l.get_str('Step X of Y').replace("X", current_step)).replace("Y", total_steps) + \
            "\n" + \
            self.l.get_str("Actual runtime:") + " " + actual_runtime + \
            "\n" + \
            self.l.get_str("Total time (with pauses):") + " " + total_time + \
            "\n" + \
            self.l.get_str("Parts completed:") + " " + str(self.jd.metadata_dict.get('PartsCompletedSoFar', 1)) + "/" + str(self.jd.metadata_dict.get('TotalNumberOfPartsRequired', 1))
            )

        self.jd.metadata_dict['ProductionNotes'] = ''
        self.production_notes.text = ''
        self.production_notes_label.text = self.l.get_str("Production notes")

        self.success_question = self.l.get_str("Did this complete successfully?")