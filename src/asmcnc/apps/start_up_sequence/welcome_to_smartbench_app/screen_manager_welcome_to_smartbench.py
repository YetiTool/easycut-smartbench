from asmcnc.apps.start_up_sequence.screens.screen_language_selection import (
    LanguageSelectionScreen,
)
from asmcnc.apps.start_up_sequence.welcome_to_smartbench_app.screens import (
    screen_welcome,
)


class ScreenManagerWelcomeToSmartBench(object):

    def __init__(self, start_sequence, screen_manager, localization):
        self.start_seq = start_sequence
        self.sm = screen_manager
        self.l = localization
        if not self.sm.has_screen("language_select"):
            language_select_screen = LanguageSelectionScreen(
                name="language_select", start_seq=self.start_seq, screen_manager=self.sm
            )
            self.sm.add_widget(language_select_screen)
        if not self.sm.has_screen("welcome"):
            welcome_screen = screen_welcome.WelcomeTextScreen(
                name="welcome",
                start_sequence=self.start_seq,
                screen_manager=self.sm,
                localization=self.l,
            )
            self.sm.add_widget(welcome_screen)
        self.start_seq.add_screen_to_sequence("language_select")
        self.start_seq.add_screen_to_sequence("welcome")
