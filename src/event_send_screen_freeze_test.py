 # -*- coding: utf-8 -*-

from kivy.config import Config
from kivy.clock import Clock
Config.set('kivy', 'keyboard_mode', 'systemanddock')
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')
Config.set('graphics', 'maxfps', '60')
Config.set('kivy', 'KIVY_CLOCK', 'interrupt')
Config.write()

import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.core.window import Window

from asmcnc.skavaUI import screen_powercycle_alert
from asmcnc.skavaUI import screen_go
from asmcnc.skavaUI import screen_home

# COMMS IMPORTS
from asmcnc.comms import router_machine  # @UnresolvedImport
from asmcnc.comms import server_connection
from asmcnc.comms import smartbench_flurry_database_connection

# NB: router_machine imports serial_connection
from asmcnc.apps import app_manager # @UnresolvedImport
from settings import settings_manager # @UnresolvedImport
from asmcnc.comms import localization

# JOB DATA IMPORT
from asmcnc.job import job_data

from random import uniform

# developer testing
Cmport = 'COM3'


class ScreenTest(App):

	def build(self):

		sm = ScreenManager(transition=NoTransition())
		l = localization.Localization()

		sett = settings_manager.Settings(sm)

		# Initialise 'j'ob 'd'ata object
		jd = job_data.JobData(localization = l)

		# Initialise 'm'achine object
		m = router_machine.RouterMachine(Cmport, sm, sett, l, jd)

		# Create database object to talk to
		db = smartbench_flurry_database_connection.DatabaseEventManager(sm, m, sett)

		am = None
		
		home_screen = screen_home.HomeScreen(name='home', screen_manager = sm, machine = m, job = jd, settings = sett, localization = l)
		go_screen = screen_go.GoScreen(name='go', screen_manager = sm, machine = m, job = jd, app_manager = am, database=db, localization = l)

		alarm_1_screen = screen_powercycle_alert.PowerCycleScreen(name='wifi1', screen_manager = sm, localization = l, database = db)
		sm.add_widget(alarm_1_screen)
		sm.add_widget(home_screen)
		sm.add_widget(go_screen)
		sm.current = 'wifi1'

		db.start_connection_to_database_thread()

		def send_an_event(db):
			db.send_event(0, 'Job cancelled', 'Cancelled job (Test): ' + "Test", 5)
			Clock.schedule_once(lambda dt: send_an_event(db), uniform(0,5))

		Clock.schedule_once(lambda dt: send_an_event(db), 0.1)

		return sm

ScreenTest().run()




