import threading, Queue
import json, socket, datetime, time
from time import sleep
from random import uniform

def log(message):
	timestamp = datetime.datetime.now()
	print (timestamp.strftime('%H:%M:%S.%f')[:12] + ' ' + str(message))

	# if "Event executed" in message:
	# 	for i in xrange(1,100000,1):
	# 		def func():
	# 			pass
	# 	print (timestamp.strftime('%H:%M:%S.%f')[:12] + ' ' + str("Finish executing"))


event_queue = Queue.Queue()

def send_events_to_database():

	def do_event_sending_loop():

		while True:

			log("Get event")
			try:
				event_task, args = event_queue.get(block=True)
				log("Got event")
				event_task(*args)
				sleep(0.1)

			except:
				log("Empty")

			



	thread_for_send_event = threading.Thread(target=do_event_sending_loop) #, args=(data, exception_type))
	thread_for_send_event.daemon = True
	thread_for_send_event.start()



def put_events_into_queue():

	counter = 11

	while True: 

		log("Putting event in queue " + str(counter))
		event_queue.put( (log, ["Event executed " + str(counter)]) )
		log("Event staged " + str(counter))

		counter+=1
		# sleep(0.9)
		sleep_time = uniform(0, 1)
		log(sleep_time)
		sleep(sleep_time)

def fill_queue():

	counter = 0

	for counter in xrange(1,11,1):

		log("Putting event in queue " + str(counter))
		event_queue.put( (log, ["Event executed " + str(counter)]) )
		log("Event staged " + str(counter))


fill_queue()
send_events_to_database()
put_events_into_queue()