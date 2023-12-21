"""
Created on 13th September 2021
End of job screen with feedback and metadata sending
@author: Letty
"""
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen

Builder.load_string(
    """
<JobIncompleteScreen>

    job_incomplete_label : job_incomplete_label
    metadata_label : metadata_label
    parts_completed_container : parts_completed_container
    parts_completed_label : parts_completed_label
    parts_completed_input : parts_completed_input
    out_of_total_parts_label : out_of_total_parts_label
    post_production_notes_container : post_production_notes_container
    batch_number_container : batch_number_container
    batch_number_label : batch_number_label
    batch_number_input : batch_number_input
    post_production_notes_label : post_production_notes_label
    post_production_notes : post_production_notes
    job_cancelled_label : job_cancelled_label
    # event_details_container : event_details_container
    event_details_label : event_details_label
    # event_details_input : event_details_input
    next_button : next_button

    on_touch_down: root.on_touch()

    BoxLayout:
        height: dp(1.66666666667*app.height)
        width: dp(0.6*app.width)
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
                    height: dp(0.125*app.height)
                    width: dp(1.0*app.width)
                    color: hex('#f9f9f9ff')
                    font_size: dp(0.0375*app.width)
                    halign: "center"
                    valign: "middle"
                    markup: True
                    text_size: self.size
            # BODY
            BoxLayout:
                size_hint: (None,None)
                width: dp(1.0*app.width)
                height: dp(0.875*app.height)
                padding:[0, dp(0.0208333333333)*app.height]
                spacing: 0
                orientation: 'vertical'
                
                # METADATA AND PRODUCTION NOTES
                BoxLayout:
                    size_hint_y: None
                    height: dp(0.270833333333*app.height)
                    orientation: 'horizontal'
                    padding:[dp(0.025)*app.width, 0, dp(0.025)*app.width, dp(0.0208333333333)*app.height]

                    BoxLayout:
                        orientation: 'vertical'
                    
                        Label: 
                            id: metadata_label
                            size_hint_y: None
                            height: dp(0.1875*app.height)
                            color: hex('#333333ff') #grey
                            font_size: dp(0.025*app.width)
                            markup: True
                            text_size: self.size
                            halign: "left"
                            valign: "bottom"

                        BoxLayout:
                            id: parts_completed_container
                            size_hint_y: None
                            height: dp(0.0625*app.height)
                            orientation: 'horizontal'

                            Label: 
                                id: parts_completed_label
                                size_hint_x: None
                                color: hex('#333333ff') #grey
                                font_size: dp(0.025*app.width)
                                markup: True
                                halign: "left"
                                valign: "top"
                                text_size: self.size

                            TextInput:
                                id: parts_completed_input
                                padding:[dp(0.005)*app.width, dp(0.00416666666667)*app.height]
                                size_hint_x: None
                                width: dp(0.0625*app.width)
                                color: hex('#333333ff')
                                text_size: self.size
                                halign: "left"
                                valign: "top"
                                markup: True
                                font_size: dp(0.025*app.width)
                                multiline: False
                                background_color: hex('#e5e5e5ff')
                                input_filter: 'int'

                            Label: 
                                id: out_of_total_parts_label
                                size_hint_x: None
                                color: hex('#333333ff') #grey
                                font_size: dp(0.025*app.width)
                                markup: True
                                halign: "left"
                                valign: "top"
                                text_size: self.size
                    
                    BoxLayout: 
                        id: post_production_notes_container
                        orientation: 'vertical'

                        BoxLayout: 
                            id: batch_number_container
                            size_hint_y: None
                            height: dp(0.0854166666667*app.height)
                            orientation: 'horizontal'
                            padding:[0, dp(0.0229166666667)*app.height, 0, 0]

                            Label:
                                id: batch_number_label
                                size_hint_x: 0.45
                                color: hex('#333333ff') #grey
                                font_size: dp(0.025*app.width)
                                halign: "left"
                                valign: "bottom"
                                markup: True
                                text_size: self.size

                            BoxLayout:
                                size_hint_y: 1
                                size_hint_x: 0.55
                                TextInput:
                                    id: batch_number_input
                                    padding:[dp(0.005)*app.width, dp(0.00416666666667)*app.height]
                                    color: hex('#333333ff')
                                    # foreground_color: hex('#333333ff')
                                    text_size: self.size
                                    size_hint_x: 1
                                    width: dp(0.125*app.width)
                                    halign: "left"
                                    valign: "bottom"
                                    markup: True
                                    font_size: dp(0.025*app.width)
                                    multiline: False
                                    background_color: hex('#e5e5e5ff')


                        Label:
                            id: post_production_notes_label
                            text: "Production notes"
                            color: hex('#333333ff') #grey
                            font_size: dp(0.025*app.width)
                            halign: "left"
                            valign: "top"
                            markup: True
                            text_size: self.size

                        TextInput:
                            id: post_production_notes
                            size_hint_y: None
                            height: dp(0.116666666667*app.height)
                            padding:[dp(0.005)*app.width, dp(0.00416666666667)*app.height]
                            text: ""
                            color: hex('#333333ff')
                            # foreground_color: hex('#333333ff')
                            text_size: self.size
                            halign: "left"
                            valign: "top"
                            markup: True
                            font_size: dp(0.025*app.width)
                            multiline: True
                            background_color: hex('#e5e5e5ff')

                # EVENT DETAILS
                Label:
                    id: job_cancelled_label
                    size_hint: (None,None)
                    height: dp(0.125*app.height)
                    width: dp(1.0*app.width)
                    # color: hex('#f9f9f9ff')
                    color: hex('#333333ff') #grey
                    font_size: dp(0.0375*app.width)
                    halign: "center"
                    valign: "bottom"
                    markup: True

                # Event details
                BoxLayout:
                    size_hint: (None,None)
                    height: dp(0.4375*app.height)
                    width: dp(1.0*app.width)
                    orientation: 'vertical'
                    spacing: 0
                    padding:[0, 0]

                    Label: 
                        id: event_details_label
                        padding:[dp(0.025)*app.width, 0]
                        color: hex('#333333ff') #grey
                        text_size: self.size
                        halign: "left"
                        valign: "middle"
                        markup: True
                        font_size: dp(0.025*app.width)

                    # Buttons
                    BoxLayout: 
                        padding:[dp(0.0125)*app.width, 0, dp(0.0125)*app.width, dp(0.0208333333333)*app.height]
                        size_hint: (None, None)
                        height: dp(0.185416666667*app.height)
                        width: dp(1.0*app.width)
                        orientation: 'horizontal'
                        BoxLayout: 
                            size_hint: (None, None)
                            height: dp(0.164583333333*app.height)
                            width: dp(0.305625*app.width)
                            padding:[0, 0, dp(0.230625)*app.width, 0]

                        BoxLayout: 
                            size_hint: (None, None)
                            height: dp(0.164583333333*app.height)
                            width: dp(0.36375*app.width)
                            # padding: [0,0,0,dp(52)]
                            Button:
                                id: next_button
                                background_normal: "./asmcnc/skavaUI/img/next.png"
                                background_down: "./asmcnc/skavaUI/img/next.png"
                                background_disabled_down: "./asmcnc/skavaUI/img/next.png"
                                background_disabled_normal: "./asmcnc/skavaUI/img/next.png"
                                border: [dp(14.5)]*4
                                size_hint: (None,None)
                                width: dp(0.36375*app.width)
                                height: dp(0.164583333333*app.height)
                                on_press: root.press_ok()
                                text: 'OK'
                                font_size: str(0.03375*app.width) + 'sp'
                                color: hex('#f9f9f9ff')
                                markup: True
                                center: self.parent.center
                                pos: self.parent.pos
                        BoxLayout: 
                            size_hint: (None, None)
                            height: dp(0.164583333333*app.height)
                            width: dp(0.305625*app.width)
                            padding:[dp(0.241875)*app.width, 0, 0, 0]
 
"""
)


class JobIncompleteScreen(Screen):
    return_to_screen = StringProperty()
    event_type = ""
    specific_event = ""

    def __init__(self, **kwargs):
        super(JobIncompleteScreen, self).__init__(**kwargs)
        self.sm = kwargs["screen_manager"]
        self.m = kwargs["machine"]
        self.l = kwargs["localization"]
        self.jd = kwargs["job"]
        self.db = kwargs["database"]
        self.kb = kwargs["keyboard"]
        self.text_inputs = [
            self.parts_completed_input,
            self.batch_number_input,
            self.post_production_notes,
        ]

    def on_touch(self):
        for text_input in self.text_inputs:
            text_input.focus = False

    def prep_this_screen(self, event, event_number=False):
        self.event_type = event
        if event_number:
            self.specific_event = str(event_number.split(":")[1])
        if not "unsuccessful" in self.event_type:
            self.db.send_job_end(False)
        self.send_job_status()
        self.sm.get_screen("go").is_job_started_already = False

    def on_pre_enter(self):
        self.update_strings()
        self.return_to_screen = self.jd.screen_to_return_to_after_cancel
        self.kb.setup_text_inputs(self.text_inputs)

    def press_ok(self):
        if self.db.set.ip_address:
            self.next_button.text = self.l.get_str("Processing")
            self.next_button.disabled = True
            self.set_post_production_notes()
            Clock.schedule_once(self.send_end_of_job_updates, 0.1)
        else:
            self.jd.post_job_data_update_pre_send(
                False, extra_parts_completed=int(self.parts_completed_input.text)
            )
            self.quit_to_return_screen()

    def send_end_of_job_updates(self, dt):
        self.jd.post_job_data_update_pre_send(
            False, extra_parts_completed=int(self.parts_completed_input.text)
        )
        self.db.send_job_summary(False)
        self.quit_to_return_screen()

    def on_leave(self):
        self.next_button.text = self.l.get_str("Ok")
        self.next_button.disabled = False

    def quit_to_return_screen(self):
        self.sm.current = self.jd.screen_to_return_to_after_job

    def set_post_production_notes(self):
        self.jd.post_production_notes = self.post_production_notes.text
        self.jd.batch_number = self.batch_number_input.text

    def send_job_status(self):
        if "cancelled" in self.event_type:
            self.db.send_event(
                0, "Job cancelled", "Cancelled job (User): " + self.jd.job_name, 5
            )
        elif "Alarm" in self.event_type:
            self.db.send_event(
                2, "Job cancelled", "Cancelled job (Alarm): " + self.jd.job_name, 1
            )
        elif "Error" in self.event_type:
            self.db.send_event(
                2, "Job cancelled", "Cancelled job (Error): " + self.jd.job_name, 0
            )
        elif "unsuccessful" in self.event_type:
            self.db.send_event(
                1, "Job unsuccessful", "Unsuccessful job: " + self.jd.job_name, 8
            )

    def update_strings(self):
        self.next_button.text = self.l.get_str("Ok")
        self.next_button.disabled = False
        if "unsuccessful" in self.event_type:
            self.job_incomplete_label.text = (
                self.l.get_str("Job unsuccessful").replace(
                    self.l.get_str("Job"), self.jd.job_name
                )
                + "!"
            )
        else:
            self.job_incomplete_label.text = (
                self.l.get_str("Job incomplete").replace(
                    self.l.get_str("Job"), self.jd.job_name
                )
                + "!"
            )
        internal_order_code = self.jd.metadata_dict.get("Internal Order Code", "")
        if len(internal_order_code) > 23:
            internal_order_code = internal_order_code[:23] + "... | "
        elif len(internal_order_code) > 0:
            internal_order_code = internal_order_code + " | "
        self.metadata_label.text = (
            internal_order_code
            + self.jd.metadata_dict.get("Process Step", "")
            + "\n"
            + self.l.get_str("Job duration:")
            + " "
            + self.l.get_localized_days(self.jd.actual_runtime)
            + "\n"
            + self.l.get_str("Pause duration:")
            + " "
            + self.l.get_localized_days(self.jd.pause_duration)
        )
        self.parts_completed_label.text = self.l.get_str("Parts completed:") + " "
        self.parts_completed_label.width = dp(
            len(self.parts_completed_label.text) * 10.5
        )
        try:
            self.parts_completed_input.text = str(
                int(self.jd.metadata_dict.get("Parts Made So Far", 0))
            )
        except:
            self.parts_completed_input.text = str(0)
        try:
            self.out_of_total_parts_label.text = " / " + str(
                int(self.jd.metadata_dict.get("Total Parts Required", 1))
            )
        except:
            self.out_of_total_parts_label.text = " / " + str(1)
        self.batch_number_label.text = self.l.get_str("Batch Number:") + " "
        self.batch_number_label.width = dp(len(self.batch_number_label.text) * 10.5)
        self.batch_number_input.text = self.jd.batch_number
        self.post_production_notes.text = self.jd.post_production_notes
        self.post_production_notes_label.text = self.l.get_str("Post Production Notes:")
        if_loss = self.l.get_str(
            "If SmartBench lost position, you will need to rehome SmartBench."
        )
        may_loss = self.l.get_str(
            "SmartBench may have lost position, so you will need to rehome SmartBench."
        )
        recovery_msg = self.l.get_str(
            "You should recover any finished parts from this job before starting a new job."
        )
        percent_streamed = (
            self.l.get_str("Percentage streamed:")
            + " "
            + str(self.jd.percent_thru_job)
            + " %"
        )
        if "cancelled" in self.event_type:
            self.job_cancelled_label.text = self.l.get_str("Job cancelled by the user.")
            self.event_details_label.text = (
                percent_streamed + "\n" + if_loss + "\n" + recovery_msg
            )
        elif "unsuccessful" in self.event_type:
            self.job_cancelled_label.text = self.l.get_str(
                "Job marked unsuccessful by the user."
            )
            self.event_details_label.text = (
                percent_streamed + "\n" + if_loss + "\n" + recovery_msg
            )
        else:
            self.job_cancelled_label.text = self.l.get_str(
                "Job cancelled due to event"
            ).replace(
                self.l.get_str("event"),
                self.l.get_str(self.event_type.lower()) + ": " + self.specific_event,
            )
            self.event_details_label.text = (
                percent_streamed + "\n" + may_loss + "\n" + recovery_msg
            )
            if "Error" in self.event_type:
                self.event_details_label.text = (
                    self.event_details_label.text
                    + " "
                    + self.l.get_str("Check your GCode file before re-running it.")
                )
