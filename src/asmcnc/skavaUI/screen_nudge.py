from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from asmcnc.skavaUI import widget_status_bar

Builder.load_string("""
<NudgeScreen>:

    status_container:status_container

    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: 0.9

            Button:
                on_press: root.previous_screen()
                text: 'go back'

        # GREEN STATUS BAR

        BoxLayout:
            size_hint_y: 0.08
            id: status_container

""")

class NudgeScreen(Screen):

    selected_line_index = 0
    max_index = 0
    display_list = []

    def __init__(self, **kwargs):
        super(NudgeScreen, self).__init__(**kwargs)

        self.sm = kwargs['screen_manager']
        self.m = kwargs['machine']
        self.l = kwargs['localization']

        # Green status bar
        self.status_container.add_widget(widget_status_bar.StatusBar(machine=self.m, screen_manager=self.sm))

    def previous_screen(self):
        self.sm.current = 'job_recovery'
