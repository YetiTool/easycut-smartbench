# -*- coding: utf-8 -*-
"""
Created on 6 Aug 2021
@author: Dennis
Screen shown after update to display new release notes
"""
import kivy, os
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty, DictProperty
from datetime import datetime

Builder.load_string(
    """

<ScrollReleaseNotes>:

    release_notes: release_notes
    BoxLayout:
        padding:[0, app.get_scaled_height(15), 0, 0]
        RstDocument:
            id: release_notes
            base_font_size: app.get_scaled_width(30)
            underline_color: 'e5e5e5'
            colors: root.color_dict

<ReleaseNotesScreen>:

    version_number_label : version_number_label
    please_read_label : please_read_label
    scroll_release_notes : scroll_release_notes
    url_label : url_label
    next_button : next_button

    canvas:
        Color: 
            rgba: hex('#e5e5e5')
        Rectangle: 
            size: self.size
            pos: self.pos

    BoxLayout:
        orientation: 'vertical'
        padding:[0, app.get_scaled_height(5.0000000000160005), 0, 0]

        BoxLayout:
            size_hint_y: 0.4
            orientation: 'vertical'
            BoxLayout:
                size_hint_y: 0.6
                orientation: 'horizontal'
                padding:[app.get_scaled_width(15), 0]
                spacing:app.get_scaled_width(10)
                Image:
                    size_hint_x: 0.06
                    source: "./asmcnc/skavaUI/img/green_tick.png"
                    allow_stretch: True
                Label:
                    id: version_number_label
                    font_size: str(0.0375*app.width) + 'sp'
                    color: hex('#333333')
                    text_size: self.size
                    size: self.texture_size
                    valign: "middle"
                    halign: "left"
            Label:
                id: please_read_label
                size_hint_y: 0.4
                padding:[app.get_scaled_width(15), 0]
                color: hex('#333333')
                font_size: str(0.0225*app.width) + 'sp'
                text_size: self.size
                size: self.texture_size

        BoxLayout:
            padding:[app.get_scaled_width(15), app.get_scaled_height(2.0000000000016), dp(0.025)*app.width, 0]
            spacing:app.get_scaled_width(15)

            ScrollReleaseNotes:
                id: scroll_release_notes

            BoxLayout:
                orientation: 'vertical'
                size_hint_x: 0.25
                Image:
                    size_hint_y: 0.4
                    source: "./asmcnc/skavaUI/img/qr_release_notes_grey.png"
                Label:
                    id: url_label
                    size_hint_y: 0.6
                    color: hex('#333333')
                    font_size: str(0.01625*app.width) + 'sp'
                    height: self.texture_size[1]
                    text_size: self.size
                    markup: True
                    valign: "top"
                    halign: "left"

        BoxLayout:
            padding:[app.get_scaled_width(250), app.get_scaled_height(2.0000000000016), app.get_scaled_width(250), dp(0.0208333333333)*app.height]
            size_hint_y: 0.25

            Button:
                id: next_button
                # text: 'Next...'
                font_size: str(0.0375*app.width) + 'sp'
                background_normal: "./asmcnc/skavaUI/img/next.png"
                on_press: root.next_screen()
                color: hex('f9f9f9ff')

"""
)


def log(message):
    timestamp = datetime.now()
    print(timestamp.strftime("%H:%M:%S.%f")[:12] + " " + str(message))


def filter_version_to_filename(character):
    try:
        int(character)
        return True
    except:
        return False


class ScrollReleaseNotes(ScrollView):
    text = StringProperty("")
    color_dict = DictProperty(
        {
            "background": "e5e5e5ff",
            "link": "1976d2ff",
            "paragraph": "333333ff",
            "title": "333333ff",
            "bullet": "333333ff",
        }
    )


class ReleaseNotesScreen(Screen):
    data_consent_app = None
    user_has_confirmed = False

    def __init__(self, **kwargs):
        super(ReleaseNotesScreen, self).__init__(**kwargs)
        self.start_seq = kwargs["start_sequence"]
        self.sm = kwargs["screen_manager"]
        self.version = kwargs["version"]
        self.l = kwargs["localization"]
        # Filename consists of just the version digits followed by .txt, so can be found by filtering out non integers from version name
        # Two dots before filename mean parent directory, as file is at the top of the filetree, not in src
        self.release_notes_filename = "../" + self.version.replace(".", "") + ".txt"
        self.scroll_release_notes.release_notes.source = self.release_notes_filename
        self.update_strings()

    def update_strings(self):
        self.version_number_label.text = self.l.get_str(
            "Software updated successfully to version"
        ).replace(self.l.get_str("version"), self.version)
        self.please_read_label.text = self.l.get_str(
            "These release notes contain critical information about how SmartBench has changed (in English)."
        )
        self.url_label.text = (
            self.l.get_str("For full release notes, go to:")
            + "\n"
            + """https://www.yetitool.com
/SUPPORT
/KNOWLEDGE-BASE
/smartbench1-console-
operations-software-
updates-release-notes"""
        )
        self.next_button.text = self.l.get_str("Next") + "..."

    def next_screen(self):
        os.system(
            'sudo sed -i "s/power_cycle_alert=True/power_cycle_alert=False/" /home/pi/easycut-smartbench/src/config.txt'
        )
        self.start_seq.next_in_sequence()
