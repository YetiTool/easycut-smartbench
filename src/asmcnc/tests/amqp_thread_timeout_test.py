import json, socket, datetime, time
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


connection = None
updates_and_events_channel = None

def set_up_connection():

	global connection
	connection = amqpstorm.Connection('sm-receiver.yetitool.com', 'console', '2RsZWRceL3BPSE6xZ6ay9xRFdKq3WvQb', port=5672, heartbeat=5*60, timeout=5*60)
	log("Connection established")

	global updates_and_events_channel
	updates_and_events_channel = connection.channel()
	updates_and_events_channel.queue.declare(queue='machine_data')


def publish_event_with_temp_channel(data, exception_type):



	def inner_function_to_thread(data, exception_type):

		log("hey again")

		log("Publishing data: " + exception_type)

		global updates_and_events_channel


		try: 
			updates_and_events_channel.basic.publish(exchange='', routing_key= 'machine_data', body=json.dumps(data))
			log(data)

			if "Job End" in exception_type:
				updates_and_events_channel.basic.publish(exchange='', routing_key= 'machine_data', body=json.dumps(generate_full_payload_data()))
				log(data)

		
		except Exception as e:
			log(exception_type + " send exception: " + str(e))


	temp_thread_for_event = threading.Thread(target=inner_function_to_thread, args=(data, exception_type))
	temp_thread_for_event.daemon = True
	temp_thread_for_event.start()


def send_event(event_description):

	if amqpstorm:

		data = {
				"payload_type": "event",
				"machine_info": {
					"name": "Hello I SmartBench",
					"location": "POSIZIONE SMARTBENCH",
					"hostname": "Zheng-Yi-Sao",
					"ec_version": "1.2.3",
					"public_ip_address": ""
				},
				"event": {
					"severity": 1,
					"type": "1",
					"name": "Alarm",
					"description": event_description
				},
				"time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			}

	publish_event_with_temp_channel(data, "Event: " + str(event_description))


set_up_connection()

sleep(10)

for i in xrange(0,11,1):
	send_event(str(i))


start_time = time.time()

while True: 

	if time.time() > start_time + 5*60: 
		break

	else:
		global updates_and_events_channel
		updates_and_events_channel.check_for_errors()
		sleep(10)




