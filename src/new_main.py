import cProfile

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition

from asmcnc.apps import app_manager
from asmcnc.comms.smart_transfer import server_connection
from asmcnc.skavaUI import (
    screen_homing_decision,
    screen_recovery_decision,
    screen_nudge,
    screen_job_recovery,
    screen_tool_selection,
    screen_lift_z_on_pause_decision,
    screen_stop_or_resume_decision,
    screen_spindle_cooldown,
    screen_spindle_shutdown,
    screen_squaring_active,
    screen_homing_active,
    screen_homing_prepare,
    screen_squaring_manual_vs_square,
    screen_door,
    screen_job_incomplete,
    screen_job_feedback,
    screen_rebooting,
    screen_boundary_warning,
    screen_mstate_warning,
    screen_serial_failure,
    screen_error,
    screen_check_job,
    screen_file_loading,
    screen_jobstart_warning,
    screen_go,
    screen_usb_filechooser,
    screen_local_filechooser,
    screen_home,
    screen_lobby,
)
from asmcnc.comms import (
    router_machine,
    smartbench_flurry_database_connection,
    localization,
)
from asmcnc.comms.grbl_settings_manager import GRBLSettingsManagerSingleton
from asmcnc.comms.logging_system.logging_system import Logger
from asmcnc.comms.model_manager import ModelManagerSingleton
from asmcnc.core_UI import popup_manager, scaling_utils
from asmcnc.job import job_data
from asmcnc.job.yetipilot import yetipilot
from asmcnc.keyboard import custom_keyboard
from settings import settings_manager


class LoadScreen(Screen):
    """The loading screen of the Easycut application."""

    def __init__(self, **kwargs):
        """Initialize the loading screen."""
        super(LoadScreen, self).__init__(**kwargs)
        self.register_event_type("on_loading_screen_open")

        self.name = "load_screen"

        self.add_widget(Label(text="Loading..."))

    def on_enter(self, *args):
        """When the screen is entered."""
        Clock.schedule_once(lambda dt: self.dispatch("on_loading_screen_open"), 3)

    def on_loading_screen_open(self, *args):
        """Event handler for when the loading is complete."""
        pass


class EasycutApp(App):
    """The main class of the Easycut application.
    Access any of the main components of the application through this class:

    App.get_running_app().<component>
    """

    screen_manager = ScreenManager(transition=NoTransition())
    localisation = None  # type: localization.Localization
    keyboard = None  # type: custom_keyboard.Keyboard
    settings_manager = None  # type: settings_manager.Settings
    job_data = None  # type: job_data.JobData
    machine = None  # type: router_machine.RouterMachine
    yetipilot = None  # type: yetipilot.YetiPilot
    flurry_database = None
    popup_manager = None  # type: popup_manager.PopupManager
    app_manager = None
    model_manager = None  # type: ModelManagerSingleton
    smartbench_flurry_database_connection = (
        None
    )  # type: smartbench_flurry_database_connection.DatabaseEventManager

    width = 800
    height = 480

    def get_scaled_width(self, width):
        return scaling_utils.get_scaled_width(width)

    def get_scaled_height(self, height):
        return scaling_utils.get_scaled_height(height)

    def get_scaled_sp(self, sp):
        return scaling_utils.get_scaled_sp(sp)

    def build(self):
        """Build the application."""
        loading_screen = LoadScreen()

        loading_screen.bind(on_loading_screen_open=self.on_loading_screen_open)

        self.screen_manager.add_widget(loading_screen)

        return self.screen_manager

    def on_loading_screen_open(self, *args):
        """When the loading screen is open."""
        self.__create_core_modules()
        self.__create_core_screens()

    def __create_core_modules(self):
        """Create the core modules of the application."""  # TODO: REFACTOR
        Logger.info("Loading screen open")
        self.localisation = localization.Localization()
        self.keyboard = custom_keyboard.Keyboard()
        self.settings_manager = settings_manager.Settings(self.screen_manager)
        self.job_data = job_data.JobData(self.settings_manager)
        self.machine = router_machine.RouterMachine(
            self.screen_manager, self.settings_manager, self.localisation, self.job_data
        )
        self.model_manager = ModelManagerSingleton(self.machine)
        if not self.model_manager.is_machine_drywall():
            self.server_connection = server_connection.ServerConnection(
                self.settings_manager
            )
        GRBLSettingsManagerSingleton(self.machine)
        self.yetipilot = yetipilot.YetiPilot(
            self.machine, self.screen_manager, self.job_data
        )
        self.flurry_database = (
            smartbench_flurry_database_connection.DatabaseEventManager(
                self.screen_manager, self.machine, self.settings_manager
            )
        )
        self.popup_manager = popup_manager.PopupManager(
            self.screen_manager, self.machine, self.localisation
        )
        self.screen_manager.pm = self.popup_manager
        self.app_manager = app_manager.AppManagerClass(
            self.screen_manager,
            self.machine,
            self.settings_manager,
            self.localisation,
            self.keyboard,
            self.job_data,
            self.flurry_database,
            None,  # config flag
            None,  # initial version
            self.popup_manager,
        )
        self.machine.s.alarm.db = self.flurry_database  # ??
        self.machine.s.yp = self.yetipilot  # ??

    def __create_core_screens(self):
        """Create the core screens of the application."""
        lobby_screen = screen_lobby.LobbyScreen(
            name="lobby",
            screen_manager=self.screen_manager,
            machine=self.machine,
            app_manager=self.app_manager,
            localization=self.localisation,
        )
        home_screen = screen_home.HomeScreen(
            name="home",
            screen_manager=self.screen_manager,
            machine=self.machine,
            job=self.job_data,
            settings=self.settings_manager,
            localization=self.localisation,
            keyboard=self.keyboard,
        )
        local_filechooser = screen_local_filechooser.LocalFileChooser(
            name="local_filechooser",
            screen_manager=self.screen_manager,
            job=self.job_data,
            localization=self.localisation,
        )
        usb_filechooser = screen_usb_filechooser.USBFileChooser(
            name="usb_filechooser",
            screen_manager=self.screen_manager,
            job=self.job_data,
            localization=self.localisation,
        )
        go_screen = screen_go.GoScreen(
            name="go",
            screen_manager=self.screen_manager,
            machine=self.machine,
            job=self.job_data,
            app_manager=self.app_manager,
            database=self.flurry_database,
            localization=self.localisation,
            yetipilot=self.yetipilot,
        )
        jobstart_warning_screen = screen_jobstart_warning.JobstartWarningScreen(
            name="jobstart_warning",
            screen_manager=self.screen_manager,
            machine=self.machine,
            localization=self.localisation,
        )
        loading_screen = screen_file_loading.LoadingScreen(
            name="loading",
            screen_manager=self.screen_manager,
            machine=self.machine,
            job=self.job_data,
            localization=self.localisation,
        )
        checking_screen = screen_check_job.CheckingScreen(
            name="check_job",
            screen_manager=self.screen_manager,
            machine=self.machine,
            job=self.job_data,
            localization=self.localisation,
        )
        error_screen = screen_error.ErrorScreenClass(
            name="errorScreen",
            screen_manager=self.screen_manager,
            machine=self.machine,
            job=self.job_data,
            database=self.flurry_database,
            localization=self.localisation,
        )
        serial_screen = screen_serial_failure.SerialFailureClass(
            name="serialScreen",
            screen_manager=self.screen_manager,
            machine=self.machine,
            win_port="COM3",
            localization=self.localisation,
        )
        mstate_screen = screen_mstate_warning.WarningMState(
            name="mstate",
            screen_manager=self.screen_manager,
            machine=self.machine,
            localization=self.localisation,
        )
        boundary_warning_screen = screen_boundary_warning.BoundaryWarningScreen(
            name="boundary",
            screen_manager=self.screen_manager,
            machine=self.machine,
            localization=self.localisation,
        )
        rebooting_screen = screen_rebooting.RebootingScreen(
            name="rebooting",
            screen_manager=self.screen_manager,
            localization=self.localisation,
        )
        job_feedback_screen = screen_job_feedback.JobFeedbackScreen(
            name="job_feedback",
            screen_manager=self.screen_manager,
            machine=self.machine,
            database=self.flurry_database,
            job=self.job_data,
            localization=self.localisation,
            keyboard=self.keyboard,
        )
        job_incomplete_screen = screen_job_incomplete.JobIncompleteScreen(
            name="job_incomplete",
            screen_manager=self.screen_manager,
            machine=self.machine,
            database=self.flurry_database,
            job=self.job_data,
            localization=self.localisation,
            keyboard=self.keyboard,
        )
        door_screen = screen_door.DoorScreen(
            name="door",
            screen_manager=self.screen_manager,
            machine=self.machine,
            job=self.job_data,
            database=self.flurry_database,
            localization=self.localisation,
        )
        squaring_decision_screen = (
            screen_squaring_manual_vs_square.SquaringScreenDecisionManualVsSquare(
                name="squaring_decision",
                screen_manager=self.screen_manager,
                machine=self.machine,
                localization=self.localisation,
            )
        )
        prepare_to_home_screen = screen_homing_prepare.HomingScreenPrepare(
            name="prepare_to_home",
            screen_manager=self.screen_manager,
            machine=self.machine,
            localization=self.localisation,
        )
        homing_active_screen = screen_homing_active.HomingScreenActive(
            name="homing_active",
            screen_manager=self.screen_manager,
            machine=self.machine,
            localization=self.localisation,
        )
        squaring_active_screen = screen_squaring_active.SquaringScreenActive(
            name="squaring_active",
            screen_manager=self.screen_manager,
            machine=self.machine,
            localization=self.localisation,
        )
        spindle_shutdown_screen = screen_spindle_shutdown.SpindleShutdownScreen(
            name="spindle_shutdown",
            screen_manager=self.screen_manager,
            machine=self.machine,
            job=self.job_data,
            database=self.flurry_database,
            localization=self.localisation,
        )
        spindle_cooldown_screen = screen_spindle_cooldown.SpindleCooldownScreen(
            name="spindle_cooldown",
            screen_manager=self.screen_manager,
            machine=self.machine,
            localization=self.localisation,
        )
        stop_or_resume_decision_screen = (
            screen_stop_or_resume_decision.StopOrResumeDecisionScreen(
                name="stop_or_resume_job_decision",
                screen_manager=self.screen_manager,
                machine=self.machine,
                job=self.job_data,
                database=self.flurry_database,
                localization=self.localisation,
            )
        )
        lift_z_on_pause_decision_screen = (
            screen_lift_z_on_pause_decision.LiftZOnPauseDecisionScreen(
                name="lift_z_on_pause_or_not",
                screen_manager=self.screen_manager,
                machine=self.machine,
                localization=self.localisation,
            )
        )
        tool_selection_screen = screen_tool_selection.ToolSelectionScreen(
            name="tool_selection",
            screen_manager=self.screen_manager,
            machine=self.machine,
            localization=self.localisation,
        )
        job_recovery_screen = screen_job_recovery.JobRecoveryScreen(
            name="job_recovery",
            screen_manager=self.screen_manager,
            machine=self.machine,
            job=self.job_data,
            localization=self.localisation,
            keyboard=self.keyboard,
        )
        nudge_screen = screen_nudge.NudgeScreen(
            name="nudge",
            screen_manager=self.screen_manager,
            machine=self.machine,
            job=self.job_data,
            localization=self.localisation,
        )
        recovery_decision_screen = screen_recovery_decision.RecoveryDecisionScreen(
            name="recovery_decision",
            screen_manager=self.screen_manager,
            machine=self.machine,
            job=self.job_data,
            localization=self.localisation,
        )
        homing_decision_screen = screen_homing_decision.HomingDecisionScreen(
            name="homing_decision",
            screen_manager=self.screen_manager,
            machine=self.machine,
            localization=self.localisation,
        )

        # add the screens to screen manager
        self.screen_manager.add_widget(lobby_screen)
        self.screen_manager.add_widget(home_screen)
        self.screen_manager.add_widget(local_filechooser)
        self.screen_manager.add_widget(usb_filechooser)
        self.screen_manager.add_widget(go_screen)
        self.screen_manager.add_widget(jobstart_warning_screen)
        self.screen_manager.add_widget(loading_screen)
        self.screen_manager.add_widget(checking_screen)
        self.screen_manager.add_widget(error_screen)
        self.screen_manager.add_widget(serial_screen)
        self.screen_manager.add_widget(mstate_screen)
        self.screen_manager.add_widget(boundary_warning_screen)
        self.screen_manager.add_widget(rebooting_screen)
        self.screen_manager.add_widget(job_feedback_screen)
        self.screen_manager.add_widget(job_incomplete_screen)
        self.screen_manager.add_widget(door_screen)
        self.screen_manager.add_widget(squaring_decision_screen)
        self.screen_manager.add_widget(prepare_to_home_screen)
        self.screen_manager.add_widget(homing_active_screen)
        self.screen_manager.add_widget(squaring_active_screen)
        self.screen_manager.add_widget(spindle_shutdown_screen)
        self.screen_manager.add_widget(spindle_cooldown_screen)
        self.screen_manager.add_widget(stop_or_resume_decision_screen)
        self.screen_manager.add_widget(lift_z_on_pause_decision_screen)
        self.screen_manager.add_widget(tool_selection_screen)
        self.screen_manager.add_widget(job_recovery_screen)
        self.screen_manager.add_widget(nudge_screen)
        self.screen_manager.add_widget(recovery_decision_screen)
        self.screen_manager.add_widget(homing_decision_screen)


if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()
    EasycutApp().run()
    profiler.disable()
