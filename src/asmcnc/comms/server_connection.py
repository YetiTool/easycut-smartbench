import socket
import sys, os
import threading
from time import sleep
from kivy.clock import Clock
from datetime import datetime
import traceback

PORT = 65432        # Port to listen on (non-privileged ports are > 1023)


# THINGS THIS MODULE NEEDS:
## timeout
## protection against garbage colleciton (timeout might be enough)
## better logging
## reinstate connection if it is dropped / connection polling
### maybe have this if there is a change in the IP address...

def log(message):
	timestamp = datetime.now()
	print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' Server connection: ' + str(message))


class ServerConnection(object):

	smartbench_name_filepath = '/home/pi/smartbench_name.txt'
	smartbench_name = 'My SmartBench'

	sock = None
	HOST = ''
	prev_host = ''

	run_connection_loop = True

	poll_connection = None

	def __init__(self):

		self.get_smartbench_name()
		self.initialise_server_connection()

	def initialise_server_connection(self):

		log("Initialising server connection...")

		self.HOST = self.get_ip_address()
		log("IP address: " + str(self.HOST))
		self.prev_host = self.HOST
		self.set_up_socket()
		self.poll_connection = Clock.schedule_interval(self.check_connection, 2)

	def set_up_socket(self):

		log("Attempting to set up socket with IP address: " + str(self.HOST))

		if sys.platform != 'win32' and sys.platform != 'darwin':

			if self.HOST != '':

				try: 
					self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
					self.sock.bind((self.HOST, PORT))
					self.sock.listen(5)
					self.sock.settimeout(60)

					self.run_connection_loop = True

					t = threading.Thread(target=self.do_connection_loop)
					t.daemon = True
					t.start()

				except Exception as e: 
					log("Unable to set up socket, exception: " + str(e))
			
			else:
				log("No network available to open socket.")

		try: log("Thread is alive? " + str(t.is_alive()))
		except: log("Thread does not exist")

	def do_connection_loop(self):

		log("Starting server connection loop...")

		while self.run_connection_loop:
			try: 
				"Waiting for connection..."
				conn, addr = self.sock.accept()
				log("Accepted connection with IP address " + str(self.HOST))

				try: 
					self.get_smartbench_name()
					conn.send(self.smartbench_name)
				except: 
					print("Message not sent")

				conn.close()

			except socket.timeout as e:
				log("Timeout: " + str(e))
				traceback.print_exc()

			except Exception as E:
				# socket object isn't available for some reason but has not timed out, so kill loop
				traceback.print_exc()
				log("Exception when trying to accept: " + str(E))
				if self.run_connection_loop:
					self.close_and_reconnect_socket()
				break


	def close_and_reconnect_socket(self):

		try: 
			log("Closing socket before attempting to reconnect...")
			self.run_connection_loop = False
			self.sock.shutdown(socket.SHUT_RDWR)
			self.sock.close()

		except Exception as e: 
			traceback.print_exc()
			log("Attempted to close socket, but raised exception: " + str(e))

		log("Try to reconnect...")
		Clock.schedule_once(lambda dt: self.set_up_socket(), 2)



	def check_connection(self, dt):

		print("current IP: " + str(self.HOST))
		print("previous IP: " + str(self.prev_host))

		self.HOST = self.get_ip_address()

		if self.HOST != self.prev_host:
			self.prev_host = self.HOST
			self.close_and_reconnect_socket()


	def get_ip_address(self):

		log("Getting IP address...")

		ip_address = ''

		if sys.platform == "win32":
			try:
				hostname=socket.gethostname()
				IPAddr=socket.gethostbyname(hostname)
				ip_address = str(IPAddr)

			except:
				ip_address = ''
		elif sys.platform != "darwin":
			try:
				f = os.popen('hostname -I')
				first_info = f.read().strip().split(' ')[0]
				if len(first_info.split('.')) == 4:
					ip_address = first_info

				else:
					ip_address = ''

			except Exception as e:
				log("Could not get IP: " + str(e))
				ip_address = ''

		return ip_address


	def get_smartbench_name(self):
		try:
			file = open(self.smartbench_name_filepath, 'r')
			self.smartbench_name = str(file.read())
			file.close()

		except: 
			self.smartbench_name = 'My SmartBench'