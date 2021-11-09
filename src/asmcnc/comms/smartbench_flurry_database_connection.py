# -*- coding: utf-8 -*-
from kivy.clock import Clock
import json, socket, datetime, time
from requests import get
import threading, Queue
from time import sleep
import traceback

def log(message):
	timestamp = datetime.datetime.now()
	print (timestamp.strftime('%H:%M:%S.%f')[:12] + ' ' + str(message))

try:
	import amqpstorm

except Exception as e:
	print(str(e))
	amqpstorm = None
	log("Couldn't import amqpstorm lib")


class DatabaseEventManager():

	z_lube_percent_left_next = 50
	spindle_brush_percent_left_next = 50
	calibration_percent_left_next = 50
	initial_consumable_intervals_found = False

	VERBOSE = True

	public_ip_address = ''

	updates_and_events_channel = None
	routine_update_thread = None

	thread_for_send_event = None

	event_send_timeout = 5*60

	def __init__(self, screen_manager, machine, settings_manager):

		self.queue = 'machine_data'
		self.m = machine
		self.sm = screen_manager
		self.jd = self.m.jd
		self.set = settings_manager

		self.event_queue = Queue.Queue()

	def __del__(self):

		log("Database Event Manager closed - garbage collected!")

	
	## SET UP CONNECTION TO DATABASE
	# This is called from screen_welcome, when all connections are set up
	##------------------------------------------------------------------------

	def start_connection_to_database_thread(self):

		if amqpstorm:

			initial_connection_thread = threading.Thread(target=self.do_updates_and_events_loop)
			initial_connection_thread.daemon = True
			initial_connection_thread.start()

	def do_updates_and_events_loop(self):

		self.event_queue.put( (self.set_up_amqpstorm_connection, []) )
		last_send = time.time()
		event_sent = True

		while True: 

			try:

				if time.time() > last_send + 10:

					if self.m.s.m_state == "Idle":
						log("Send 'alive'")
						self.publish_event(self.alive_data(), "Alive", False)

					else:
						log("Send routine update")
						self.publish_event(self.generate_full_payload_data(), "Routine Full Payload", False)

					last_send = time.time()

				if event_sent or (time.time() > event_get_time + self.event_send_timeout):
					try: 
						event_task, args = self.event_queue.get(block=True, timeout=10)
						event_get_time = time.time()
						event_sent = False

					except:
						pass

				if event_task and not event_sent:
					try:
						event_task(*args)
						event_sent = True

					except Exception as event_exception:
						print(str(event_exception))
						raise event_exception
					

			except amqpstorm.AMQPConnectionError as e: 

				if 'connection timed out' in e: 
					print("connection time out")
					print(str(e))
					log(traceback.format_exc())

				else:
					print(str(e))
					log(traceback.format_exc())
					self.event_queue.put( (self.reinstate_channel_or_connection_if_missing, []) )

			except Exception as E: 

				print(str(E))
				log(traceback.format_exc())
				self.event_queue.put( (self.reinstate_channel_or_connection_if_missing, []) )


	def set_up_amqpstorm_connection(self):

		log("Try to set up amqpstorm connection")

		if self.set.ip_address and self.set.wifi_available:

			try:

				self.connection = amqpstorm.Connection('sm-receiver.yetitool.com', 'console', '2RsZWRceL3BPSE6xZ6ay9xRFdKq3WvQb', port=5672, timeout=60)
				log("Connection established")

				self.updates_and_events_channel = self.connection.channel()
				self.updates_and_events_channel.queue.declare(queue=self.queue)

				self.event_queue.task_done()

			except Exception as e:
				log("AMPQ storm connection exception: " + str(e))
				log(traceback.format_exc())


	def reinstate_channel_or_connection_if_missing(self):

		log("Attempt to reinstate channel or connection")

		try:

			if self.connection.is_closed:
				log("Connection is closed, set up new connection")
				self.set_up_amqpstorm_connection()

			elif self.updates_and_events_channel.is_closed:
				if self.VERBOSE: log("Channel is closed, set up new channel")
				self.updates_and_events_channel = self.connection.channel()
				self.updates_and_events_channel.queue.declare(queue=self.queue)

			else: 

				try:
					log("Close connection and start again") 
					self.connection.close()
					self.set_up_amqpstorm_connection()

				except:
					log("sleep and try reinstating connection again in a minute") 
					sleep(10)
					self.reinstate_channel_or_connection_if_missing()

		except:

			# Try closing both, just in case something weird has happened
			try: self.updates_and_events_channel.close()
			except: pass

			try: self.connection.close()
			except: pass

			self.connection = None
			self.set_up_amqpstorm_connection()



	## PUBLISH EVENT TO DATABASE
	##------------------------------------------------------------------------
	def publish_event(self, data, exception_type, is_event):

		if self.VERBOSE: log("Publishing data: " + exception_type)

		if self.set.wifi_available:
			print("Wifi wifi_available, attempt to publish")
			self.updates_and_events_channel.basic.publish(json.dumps(data), self.queue, exchange='')
			print("Did publish")
			if is_event: 
				self.event_queue.task_done()
			if self.VERBOSE: log(data)

		else: 
			print("No WiFi available")



	## ROUTINE EVENTS
	##------------------------------------------------------------------------

	# send alive 'ping' to server when SmartBench is Idle
	def alive_data(self):

		data = {
				"payload_type": "alive",
				"machine_info": {
					"name": self.m.device_label,
					"location": self.m.device_location,
					"hostname": self.set.console_hostname,
					"ec_version": self.m.sett.sw_version,
					"public_ip_address": self.set.public_ip_address
				},
				"time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			}

		return data


	### FUNCTIONS FOR SENDING FULL PAYLOAD

	def generate_full_payload_data(self):

		z_lube_limit_hrs = self.m.time_to_remind_user_to_lube_z_seconds / 3600
		z_lube_used_hrs = self.m.time_since_z_head_lubricated_seconds / 3600
		z_lube_hrs_left = round(z_lube_limit_hrs - z_lube_used_hrs, 2)
		z_lube_percent_left = round((z_lube_hrs_left / z_lube_limit_hrs) * 100,
									2)  # This was percentage left, not percentage used

		# spindle brush
		spindle_brush_limit_hrs = self.m.spindle_brush_lifetime_seconds / 3600
		spindle_brush_used_hrs = self.m.spindle_brush_use_seconds / 3600
		spindle_brush_hrs_left = round(spindle_brush_limit_hrs - spindle_brush_used_hrs, 2)
		spindle_brush_percent_left = round((spindle_brush_hrs_left / spindle_brush_limit_hrs) * 100,
										   2)  # This was percentage left, not percentage used

		# calibration
		calibration_limit_hrs = self.m.time_to_remind_user_to_calibrate_seconds / 3600
		calibration_used_hrs = self.m.time_since_calibration_seconds / 3600
		calibration_hrs_left = round(calibration_limit_hrs - calibration_used_hrs, 2)
		calibration_percent_left = round((calibration_hrs_left / calibration_limit_hrs) * 100,
										 2)  # This was percentage left, not percentage used

		# Set initial values for the next percentage interval so that it doesn't go through each interval every time
		if not self.initial_consumable_intervals_found:
			self.find_initial_consumable_intervals(z_lube_percent_left, spindle_brush_percent_left,
												   calibration_percent_left)

		# Check if consumables have passed thresholds for sending events
		self.check_consumable_percentages(z_lube_percent_left, spindle_brush_percent_left, calibration_percent_left)


		# Human readable machine status:
		status = self.m.state()

		if 'Door' in status: 
			if '3' in status:
				status = "Resuming"
			else: 
				status = "Paused"

		data = {
				"payload_type": "full",
				"machine_info": {
					"name": self.m.device_label,
					"location": self.m.device_location,
					"hostname": self.set.console_hostname,
					"ec_version": self.m.sett.sw_version,
					"public_ip_address": self.set.public_ip_address
				},
				"statuses": {
					"status": status,

					"z_lube_%_left": z_lube_percent_left,
					"z_lube_hrs_before_next": z_lube_hrs_left,

					"spindle_brush_%_left": spindle_brush_percent_left,
					"spindle_brush_hrs_before_next": spindle_brush_hrs_left,

					"calibration_%_left": calibration_percent_left,
					"calibration_hrs_before_next": calibration_hrs_left,

					"file_name": self.jd.job_name or '',
					"job_time": self.sm.get_screen('go').time_taken_seconds or '',
					"gcode_line": self.m.s.g_count or 0,
					"job_percent": self.jd.percent_thru_job or 0.0,
					"overload_peak": float(self.sm.get_screen('go').overload_peak) or 0.0

				},
				"time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			}

		return data


	def find_initial_consumable_intervals(self, z_lube_percent, spindle_brush_percent, calibration_percent):

		def find_current_interval(value):
			# This looks stupid but I don't have a better idea without using loops
			if value < 50:
				if value < 25:
					if value < 10:
						if value < 5:
							if value < 0:
								if value < -10:
									return -25
								return -10
							return 0
						return 5
					return 10
				return 25
			return 50

		self.z_lube_percent_left_next = find_current_interval(z_lube_percent)
		self.spindle_brush_percent_left_next = find_current_interval(spindle_brush_percent)
		self.calibration_percent_left_next = find_current_interval(calibration_percent)

		self.initial_consumable_intervals_found = True

	def check_consumable_percentages(self, z_lube_percent, spindle_brush_percent, calibration_percent):
		# The next percentage to set the threshold to once one has been passed
		next_percent_dict = {50: 25, 25: 10, 10: 5, 5: 0, 0: -10, -10: -25, -25: -25}
		# The severity that passing each percentage corresponds to
		severity_dict = {50: 0, 25: 1, 10: 1, 5: 2, 0: 2, -10: 2, -25: 2}
		# The percentage that was last passed, used to check whether the percentage has increased
		previous_percent_dict = {50: 50, 25: 50, 10: 25, 5: 10, 0: 5, -10: 0, -25: -10}

		if z_lube_percent < self.z_lube_percent_left_next:
			self.send_event(severity_dict[self.z_lube_percent_left_next], 'Z-lube percentage left',
							'Z-lube percentage passed below ' + str(self.z_lube_percent_left_next) + '%', 2)
			self.z_lube_percent_left_next = next_percent_dict[self.z_lube_percent_left_next]

		if spindle_brush_percent < self.spindle_brush_percent_left_next:
			self.send_event(severity_dict[self.spindle_brush_percent_left_next], 'Spindle brush percentage left',
							'Spindle brush percentage passed below ' + str(self.spindle_brush_percent_left_next) + '%',
							2)
			self.spindle_brush_percent_left_next = next_percent_dict[self.spindle_brush_percent_left_next]

		if calibration_percent < self.calibration_percent_left_next:
			self.send_event(severity_dict[self.calibration_percent_left_next], 'Calibration percentage left',
							'Calibration percentage passed below ' + str(self.calibration_percent_left_next) + '%', 2)
			self.calibration_percent_left_next = next_percent_dict[self.calibration_percent_left_next]

		# In case any percentages somehow increased past their previous threshold
		if z_lube_percent > previous_percent_dict[self.z_lube_percent_left_next] or spindle_brush_percent > \
				previous_percent_dict[self.spindle_brush_percent_left_next] or calibration_percent > \
				previous_percent_dict[self.calibration_percent_left_next]:
			self.find_initial_consumable_intervals(z_lube_percent, spindle_brush_percent, calibration_percent)


	## UNIQUE EVENTS
	##------------------------------------------------------------------------

	### BEGINNING AND END OF JOB
	def send_job_end(self, successful):

		if amqpstorm:

			data =  {
					"payload_type": "job_end",
					"machine_info": {
						"name": self.m.device_label,
						"location": self.m.device_location,
						"hostname": self.set.console_hostname,
						"ec_version": self.m.sett.sw_version,
						"public_ip_address": self.set.public_ip_address
					},
					"job_data": {
						"job_name": self.jd.job_name or '',
						"successful": successful,
						"actual_job_duration": self.jd.actual_runtime,
						"actual_pause_duration": self.jd.pause_duration
					},
					"time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
				}

			self.event_queue.put( (self.publish_event, [data, "Job End", True]) )


	def send_job_summary(self, successful):

		if amqpstorm:

			data =  {
					"payload_type": "job_summary",
					"machine_info": {
						"name": self.m.device_label,
						"location": self.m.device_location,
						"hostname": self.set.console_hostname,
						"ec_version": self.m.sett.sw_version,
						"public_ip_address": self.set.public_ip_address
					},
					"job_data": {
						"job_name": self.jd.job_name or '',
						"successful": successful,
						"post_production_notes": self.jd.post_production_notes,
						"batch_number": self.jd.batch_number,
						"parts_made_so_far": self.jd.metadata_dict.get('Parts Made So Far', 0)
					},
					"time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
				}

			self.event_queue.put( (self.publish_event, [data, "Job Summary", True]) )

		self.jd.post_job_data_update_post_send()

	def send_job_start(self):

		if amqpstorm:

			data = {
					"payload_type": "job_start",
					"machine_info": {
						"name": self.m.device_label,
						"location": self.m.device_location,
						"hostname": self.set.console_hostname,
						"ec_version": self.m.sett.sw_version,
						"public_ip_address": self.set.public_ip_address
					},
					"job_data": {
						"job_name": self.jd.job_name or '',
						"job_start": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
					},
					"metadata": {

					},
					"time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			}

			metadata_in_json_format = {k.translate(None, ' '): v for k, v in self.jd.metadata_dict.iteritems()}

			data["metadata"] = metadata_in_json_format

			self.event_queue.put( (self.publish_event, [data, "Job Start", True]) )


	### FEEDS AND SPEEDS
	def send_spindle_speed_info(self):

		if amqpstorm:

			data = {
				"payload_type": "spindle_speed",
				"machine_info": {
					"name": self.m.device_label,
					"location": self.m.device_location,
					"hostname": self.set.console_hostname,
					"ec_version": self.m.sett.sw_version,
					"public_ip_address": self.set.public_ip_address
				},
				"speeds": {
					"spindle_speed": self.m.spindle_speed(),
					"spindle_percentage": self.sm.get_screen('go').speedOverride.speed_rate_label.text,
					"max_spindle_speed_absolute": self.sm.get_screen('go').spindle_speed_max_absolute or '',
					"max_spindle_speed_percentage": self.sm.get_screen('go').spindle_speed_max_percentage or ''
				}
			}

			self.event_queue.put( (self.publish_event, [data, "Spindle speed", True]) )


	def send_feed_rate_info(self):

		if amqpstorm:

			data = {
				"payload_type": "feed_rate",
				"machine_info": {
					"name": self.m.device_label,
					"location": self.m.device_location,
					"hostname": self.set.console_hostname,
					"ec_version": self.m.sett.sw_version,
					"public_ip_address": self.set.public_ip_address
				},
				"feeds": {
					"feed_rate": self.m.feed_rate(),
					"feed_percentage": self.sm.get_screen('go').feedOverride.feed_rate_label.text,
					"max_feed_rate_absolute": self.sm.get_screen('go').feed_rate_max_absolute or '',
					"max_feed_rate_percentage": self.sm.get_screen('go').feed_rate_max_percentage or ''
				}
			}

			self.event_queue.put( (self.publish_event, [data, "Feed rate", True]) )


	### JOB CRITICAL EVENTS, INCLUDING ALARMS AND ERRORS

	# Severity
	# 0 - info
	# 1 - warning
	# 2 - critical

	# Type
	# 0 - errors
	# 1 - alarms
	# 2 - maintenance
	# 3 - job pause
	# 4 - job resume
	# 5 - job cancel
	# 6 - job start
	# 7 - job end
	# 8 - job unsuccessful

	def send_event(self, event_severity, event_description, event_name, event_type):

		if amqpstorm:

			data = {
					"payload_type": "event",
					"machine_info": {
						"name": self.m.device_label,
						"location": self.m.device_location,
						"hostname": self.set.console_hostname,
						"ec_version": self.m.sett.sw_version,
						"public_ip_address": self.set.public_ip_address
					},
					"event": {
						"severity": event_severity,
						"type": event_type,
						"name": event_name,
						"description": event_description
					},
					"time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
				}

			self.event_queue.put( (self.publish_event, [data, "Event: " + str(event_name), True]) )







