"""
Created on 28 Jan 2022
@author: Archie
YetiTool's UI for SmartBench
www.yetitool.com

#######################################################
Z HEAD QC APPLICATION

Used in production to carry out quality control checks. 
#######################################################

#######################################################
PLATFORM

This app needs following platform changes to run
as default application at startup: 

touch /home/pi/YETI_ZHEADQC_PROD_JIG.txt

#######################################################
"""

from .asmcnc.comms.logging_system.logging_system import Logger
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.clock import Clock
from .asmcnc.comms.router_machine import RouterMachine
from .settings.settings_manager import Settings
from .asmcnc.job.job_data import JobData
from .asmcnc.comms.localization import Localization
from .asmcnc.keyboard.custom_keyboard import Keyboard
from .asmcnc.comms import usb_storage
from .asmcnc.comms import smartbench_flurry_database_connection
from .asmcnc.skavaUI.screen_home import HomeScreen
from .asmcnc.skavaUI.screen_squaring_manual_vs_square import (
    SquaringScreenDecisionManualVsSquare,
)
from .asmcnc.skavaUI.screen_homing_prepare import HomingScreenPrepare
from .asmcnc.skavaUI.screen_homing_active import HomingScreenActive
from .asmcnc.skavaUI.screen_squaring_active import SquaringScreenActive
from .asmcnc.skavaUI import screen_door
from .asmcnc.skavaUI import screen_error
from .asmcnc.production.z_head_qc_jig.z_head_qc_connecting import ZHeadQCConnecting
from .asmcnc.production.z_head_qc_jig.z_head_qc_pcb_set_up import ZHeadPCBSetUp
from .asmcnc.production.z_head_qc_jig.z_head_qc_pcb_set_up_outcome import (
    ZHeadPCBSetUpOutcome,
)
from .asmcnc.production.z_head_qc_jig.z_head_qc_home import ZHeadQCHome
from .asmcnc.production.z_head_qc_jig.z_head_qc_warranty_choice import (
    ZHeadWarrantyChoice,
)
from .asmcnc.production.z_head_qc_jig.z_head_qc_1 import ZHeadQC1
from .asmcnc.production.z_head_qc_jig.z_head_qc_2 import ZHeadQC2
from .asmcnc.production.z_head_qc_jig.z_head_qc_3 import ZHeadQC3
from .asmcnc.production.z_head_qc_jig.z_head_qc_4 import ZHeadQC4
from .asmcnc.production.z_head_qc_jig.z_head_qc_5 import ZHeadQC5
from .asmcnc.production.z_head_qc_jig.z_head_qc_6 import ZHeadQC6
from .asmcnc.production.z_head_qc_jig.z_head_qc_7 import ZHeadQC7
from .asmcnc.production.z_head_qc_jig.z_head_qc_8 import ZHeadQC8
from .asmcnc.production.z_head_qc_jig.z_head_qc_aftr_apr_21 import (
    ZHeadQCWarrantyAfterApr21,
)
from .asmcnc.production.z_head_qc_jig.z_head_qc_b4_apr_21 import (
    ZHeadQCWarrantyBeforeApr21,
)
from .asmcnc.production.z_head_qc_jig.z_head_qc_db1 import ZHeadQCDB1
from .asmcnc.production.z_head_qc_jig.z_head_qc_db2 import ZHeadQCDB2
from .asmcnc.production.z_head_qc_jig.z_head_qc_db_success import ZHeadQCDBSuccess
from .asmcnc.production.z_head_qc_jig.z_head_qc_db_fail import ZHeadQCDBFail
from .asmcnc.production.z_head_mechanics_jig.z_head_mechanics_monitor import (
    ZHeadMechanicsMonitor,
)
from .asmcnc.production.database.calibration_database import CalibrationDatabase

Cmport = "COM3"


class ZHeadQC(App):

    def build(self):
        Logger.info("Starting diagnostics")
        sm = ScreenManager(transition=NoTransition())
        sett = Settings(sm)
        l = Localization()
        kb = Keyboard(localization=l)
        jd = JobData(localization=l, settings_manager=sett)
        m = RouterMachine(Cmport, sm, sett, l, jd)
        db = smartbench_flurry_database_connection.DatabaseEventManager(sm, m, sett)
        calibration_db = CalibrationDatabase()
        calibration_db.set_up_connection()
        usb_stick = usb_storage.USB_storage(sm, l)
        usb_stick.enable()
        if m.s.is_connected():
            Clock.schedule_once(m.s.start_services, 1)
        error_screen = screen_error.ErrorScreenClass(
            name="errorScreen",
            screen_manager=sm,
            machine=m,
            job=jd,
            database=db,
            localization=l,
        )
        sm.add_widget(error_screen)
        door_screen = screen_door.DoorScreen(
            name="door",
            screen_manager=sm,
            machine=m,
            job=jd,
            database=db,
            localization=l,
        )
        sm.add_widget(door_screen)
        home_screen = HomeScreen(
            name="home",
            screen_manager=sm,
            machine=m,
            job=jd,
            settings=sett,
            localization=l,
            keyboard=kb,
        )
        sm.add_widget(home_screen)
        squaring_decision_screen = SquaringScreenDecisionManualVsSquare(
            name="squaring_decision", screen_manager=sm, machine=m, localization=l
        )
        sm.add_widget(squaring_decision_screen)
        prepare_to_home_screen = HomingScreenPrepare(
            name="prepare_to_home", screen_manager=sm, machine=m, localization=l
        )
        sm.add_widget(prepare_to_home_screen)
        homing_active_screen = HomingScreenActive(
            name="homing_active", screen_manager=sm, machine=m, localization=l
        )
        sm.add_widget(homing_active_screen)
        squaring_active_screen = SquaringScreenActive(
            name="squaring_active", screen_manager=sm, machine=m, localization=l
        )
        sm.add_widget(squaring_active_screen)
        z_head_qc_1 = ZHeadQC1(name="qc1", sm=sm, m=m, l=l)
        sm.add_widget(z_head_qc_1)
        z_head_qc_2 = ZHeadQC2(name="qc2", sm=sm, m=m, l=l)
        sm.add_widget(z_head_qc_2)
        z_head_qc_3 = ZHeadQC3(name="qc3", sm=sm, m=m)
        sm.add_widget(z_head_qc_3)
        z_head_qc_4 = ZHeadQC4(name="qc4", sm=sm, m=m)
        sm.add_widget(z_head_qc_4)
        z_head_qc_5 = ZHeadQC5(name="qc5", sm=sm, m=m, calibration_db=calibration_db)
        sm.add_widget(z_head_qc_5)
        z_head_qc_6 = ZHeadQC6(name="qc6", sm=sm, m=m)
        sm.add_widget(z_head_qc_6)
        z_head_qc_7 = ZHeadQC7(name="qc7", sm=sm, m=m, l=l)
        sm.add_widget(z_head_qc_7)
        z_head_qc_8 = ZHeadQC8(name="qc8", sm=sm, m=m, l=l)
        sm.add_widget(z_head_qc_8)
        z_head_qc_connecting = ZHeadQCConnecting(
            name="qcconnecting", sm=sm, m=m, usb=usb_stick
        )
        sm.add_widget(z_head_qc_connecting)
        z_head_qc_pcb_set_up = ZHeadPCBSetUp(name="qcpcbsetup", sm=sm, m=m)
        sm.add_widget(z_head_qc_pcb_set_up)
        z_head_qc_pcb_set_up_outcome = ZHeadPCBSetUpOutcome(
            name="qcpcbsetupoutcome", sm=sm, m=m
        )
        sm.add_widget(z_head_qc_pcb_set_up_outcome)
        z_head_qc_home = ZHeadQCHome(name="qchome", sm=sm, m=m, usb=usb_stick)
        sm.add_widget(z_head_qc_home)
        z_head_qc_warranty_choice = ZHeadWarrantyChoice(
            name="qcWC", sm=sm, m=m, usb=usb_stick
        )
        sm.add_widget(z_head_qc_warranty_choice)
        z_head_qc_warranty_after_apr_21 = ZHeadQCWarrantyAfterApr21(
            name="qcW136", sm=sm, m=m, l=l
        )
        sm.add_widget(z_head_qc_warranty_after_apr_21)
        z_head_qc_warranty_before_apr_21 = ZHeadQCWarrantyBeforeApr21(
            name="qcW112", sm=sm, m=m, l=l
        )
        sm.add_widget(z_head_qc_warranty_before_apr_21)
        z_head_qc_db1 = ZHeadQCDB1(name="qcDB1", sm=sm, m=m)
        sm.add_widget(z_head_qc_db1)
        z_head_qc_db2 = ZHeadQCDB2(
            name="qcDB2", sm=sm, m=m, calibration_db=calibration_db
        )
        sm.add_widget(z_head_qc_db2)
        z_head_qc_db_success = ZHeadQCDBSuccess(name="qcDB3", sm=sm, m=m)
        sm.add_widget(z_head_qc_db_success)
        z_head_qc_db_fail = ZHeadQCDBFail(name="qcDB4", sm=sm, m=m)
        sm.add_widget(z_head_qc_db_fail)
        z_head_mechanics_monitor = ZHeadMechanicsMonitor(
            name="monitor", sm=sm, m=m, l=l
        )
        sm.add_widget(z_head_mechanics_monitor)
        sm.current = "qcconnecting"
        return sm


if __name__ == "__main__":
    ZHeadQC().run()
