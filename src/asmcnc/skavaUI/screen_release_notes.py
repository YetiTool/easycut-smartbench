'''
Created on 6 Aug 2021
@author: Dennis
Screen shown after update to display new release notes
'''

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty

from datetime import datetime

Builder.load_string("""

<ScrollReleaseNotes>:

    text_container: text_container

    Label:
        id: text_container
        color: hex('#474747')
        size_hint_y: None
        height: self.texture_size[1]
        text_size: self.width, None
        font_size: '20sp'
        markup: True

<ReleaseNotesScreen>:

    version_number_label: version_number_label
    scroll_release_notes: scroll_release_notes
    url_label: url_label

    canvas:
        Color: 
            rgba: hex('#FFFFFF')
        Rectangle: 
            size: self.size
            pos: self.pos

    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            size_hint_y: 0.15
            orientation: 'vertical'
            Label:
                id: version_number_label
                font_size: '30sp'
                color: hex('#000000')
            Label:
                text: 'These release notes contain critical information about how SmartBench has changed (in English).'
                color: hex('#474747')
                font_size: '18sp'

        BoxLayout:
            padding: [dp(20), dp(20), dp(20), dp(0)]
            spacing: dp(15)

            ScrollReleaseNotes:
                id: scroll_release_notes

            BoxLayout:
                orientation: 'vertical'
                size_hint_x: 0.3
                Image:
                    source: "./asmcnc/skavaUI/img/qr_release_notes.png"
                Label:
                    id: url_label
                    color: hex('#848484')
                    font_size: '13sp'

        BoxLayout:
            padding: [dp(250), dp(10)]
            size_hint_y: 0.25

            Button:
                text: 'NEXT'
                font_size: '25sp'
                background_color: 0,0,0,0
                on_press: root.switch_screen()

                canvas.before:
                    Color:
                        rgba: hex('#1976d2ff')
                    RoundedRectangle:
                        size: self.size
                        pos: self.pos

""")

def log(message):
    timestamp = datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + str(message))

def filter_version_to_filename(character):
    try:
        int(character)
        return True
    except:
        return False

class ScrollReleaseNotes(ScrollView):
    text = StringProperty('')

class ReleaseNotesScreen(Screen):

    def __init__(self, **kwargs):
        super(ReleaseNotesScreen, self).__init__(**kwargs)
        self.sm = kwargs['screen_manager']
        self.version = kwargs['version']

        # Filename consists of just the version digits followed by .txt, so can be found by filtering out non integers from version name
        # Two dots before filename mean parent directory, as file is at the top of the filetree, not in src
        self.release_notes_filename = '../' + filter(filter_version_to_filename, self.version) + '.txt'

        self.version_number_label.text = 'Console software updated successfully to ' + self.version
        self.scroll_release_notes.effect_cls = kivy.effects.scroll.ScrollEffect

        self.read_release_notes()

        self.url_label.text = 'To learn more about these\nrelease notes, go to:\nhttps://www.yetitool.com\n/SUPPORT/KNOWLEDGE-BASE\n/smartbench1-console-\noperations-software-\nupdates-release-notes'

    def read_release_notes(self):
        try:
            file = open(self.release_notes_filename, 'r')
            self.release_notes = str(file.read())
            file.close()

            self.scroll_release_notes.text_container.text = self.release_notes
        except:
            log("Unable to read in release notes")

    def switch_screen(self):
        self.sm.current = 'restart_smartbench'
