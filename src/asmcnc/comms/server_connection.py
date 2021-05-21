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

	is_socket_available = True

	poll_connection = None

	def __init__(self):

		self.get_smartbench_name()
		self.initialise_server_connection()

	def __del__(self):
  		log("Server connection class has been deleted")

	def initialise_server_connection(self):

		log("Initialising server connection...")

		self.HOST = self.get_ip_address()
		log("IP address: " + str(self.HOST))
		self.prev_host = self.HOST
		self.poll_connection = Clock.schedule_interval(self.check_connection, 2)
		self.set_up_socket()

	def set_up_socket(self):

		log("Attempting to set up socket with IP address: " + str(self.HOST))

		if sys.platform != 'win32' and sys.platform != 'darwin':

			if self.HOST != '':

				try: 
					self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
					self.sock.bind((self.HOST, PORT))
					self.sock.listen(5)
					self.sock.settimeout(20)

					self.is_socket_available = True

					try: 
						log("Thread is alive? " + str(t.is_alive()))
					except:
						t = threading.Thread(target=self.do_connection_loop)
						t.daemon = True
						t.start()

				except Exception as e: 
					log("Unable to set up socket, exception: " + str(e))
			
			else:
				log("No IP address available to open socket with.")


	def do_connection_loop(self):

		log("Starting server connection loop...")

		while True:
			try: 
				"Waiting for connection..."
				if self.is_socket_available:
					conn, addr = self.sock.accept()
					log("Accepted connection with IP address " + str(self.HOST))

					try: 
						self.get_smartbench_name()
						conn.send(self.smartbench_name)
					except: 
						print("Message not sent")

					conn.close()

				else: 
					log("Socket unavailable, waiting for it to come back online...")

			except socket.timeout as e:
				log("Timeout: " + str(e))

			except Exception as E:
				# socket object isn't available but has not timed out
				# reestablish socket if needs be
				log("Exception when trying to accept: " + str(E))
				if self.is_socket_available:
					self.close_and_reconnect_socket()
					sleep(20)


	def close_and_reconnect_socket(self):

		try: 
			log("Closing socket before attempting to reconnect...")
			self.is_socket_available = False
			self.sock.shutdown(socket.SHUT_RDWR)
			self.sock.close()

		except Exception as e: 
			log("Attempted to close socket, but raised exception: " + str(e))

		log("Try to reconnect...")
		new_event = Clock.schedule_once(lambda dt: self.set_up_socket(), 2)


	def check_connection(self, dt):

		self.HOST = self.get_ip_address()

		if self.HOST != self.prev_host:
			self.prev_host = self.HOST
			self.close_and_reconnect_socket()

	def get_ip_address(self):

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
				ip_address = ''

		return ip_address


	def get_smartbench_name(self):
		try:
			file = open(self.smartbench_name_filepath, 'r')
			self.smartbench_name = str(file.read())
			file.close()

		except: 
			self.smartbench_name = 'My SmartBench'