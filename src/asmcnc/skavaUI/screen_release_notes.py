# -*- coding: utf-8 -*-
'''
Created on 6 Aug 2021
@author: Dennis
Screen shown after update to display new release notes
'''

import kivy, os
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty, DictProperty

from asmcnc.core_UI.data_and_wifi import data_consent_manager

from datetime import datetime

Builder.load_string("""

<ScrollReleaseNotes>:

    release_notes: release_notes

    RstDocument:
        id: release_notes
        base_font_size: 30
        underline_color: 'f9f9f9'
        colors: root.color_dict

<ReleaseNotesScreen>:

    version_number_label: version_number_label
    scroll_release_notes: scroll_release_notes
    url_label: url_label

    canvas:
        Color: 
            rgba: hex('#f9f9f9')
        Rectangle: 
            size: self.size
            pos: self.pos

    BoxLayout:
        orientation: 'vertical'
        padding: [dp(0), dp(5), dp(0), dp(0)]

        BoxLayout:
            size_hint_y: 0.25
            orientation: 'vertical'
            BoxLayout:
                orientation: 'horizontal'
                Image:
                    size_hint_x: 0.1
                    source: "./asmcnc/skavaUI/img/green_tick.png"
                Label:
                    id: version_number_label
                    font_size: '30sp'
                    color: hex('#333333')
                    text_size: self.size
            Label:
                text: 'These release notes contain critical information about how SmartBench has changed (in English).'
                color: hex('#333333')
                font_size: '18sp'

        BoxLayout:
            padding: [dp(20), dp(5), dp(20), dp(0)]
            spacing: dp(15)

            ScrollReleaseNotes:
                id: scroll_release_notes

            BoxLayout:
                orientation: 'vertical'
                size_hint_x: 0.3
                Image:
                    source: "./asmcnc/skavaUI/img/qr_release_notes_grey.png"
                Label:
                    id: url_label
                    color: hex('#333333')
                    font_size: '13sp'

        BoxLayout:
            padding: [dp(250), dp(10)]
            size_hint_y: 0.3

            Button:
                text: 'Next...'
                font_size: '30sp'
                background_normal: "./asmcnc/apps/warranty_app/img/next.png"
                on_press: root.switch_screen()
                color: hex('f9f9f9ff')

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

    color_dict = DictProperty({
                    'background': 'f9f9f9ff',
                    'link': '1976d2ff',
                    'paragraph': '333333ff',
                    'title': '333333ff',
                    'bullet': 'f9f9f9ff'})

class ReleaseNotesScreen(Screen):

    data_consent_app = None
    user_has_confirmed = False

    def __init__(self, **kwargs):
        super(ReleaseNotesScreen, self).__init__(**kwargs)
        self.sm = kwargs['screen_manager']
        self.version = kwargs['version']

        # Filename consists of just the version digits followed by .txt, so can be found by filtering out non integers from version name
        # Two dots before filename mean parent directory, as file is at the top of the filetree, not in src
        self.release_notes_filename = '../' + (self.version).replace(".","") + '.txt'
        self.scroll_release_notes.release_notes.source = self.release_notes_filename

        self.version_number_label.text = 'Console software updated successfully to ' + self.version

        self.url_label.text = 'To learn more about this\nrelease, go to:\nhttps://www.yetitool.com\n/SUPPORT/KNOWLEDGE-BASE\n/smartbench1-console-\noperations-software-\nupdates-release-notes'

        self.check_data_consent_screen()

    # This is incomplete
    def check_data_consent_screen(self):
        data_consent = (os.popen('grep "user_has_seen_privacy_notice" /home/pi/easycut-smartbench/src/config.txt').read())

        if data_consent.endswith('False') or not data_consent:
            self.data_consent_app = data_consent_manager.DataConsentManager(self.sm, False)

    def switch_screen(self):
        user_has_confirmed = True
        if not self.data_consent_app: # test this
            self.sm.current = 'welcome'

        else: 
            self.data_consent_app.open_data_consent('welcome')

    def on_leave(self):
        if self.sm.current != 'alarmScreen' and self.sm.current != 'errorScreen' and self.sm.current != 'door': 
            if self.user_has_confirmed:
                self.sm.remove_widget(self.sm.get_screen('release_notes'))
