import socket
import sys
import threading
from time import sleep
from kivy.clock import Clock
from datetime import datetime

PORT = 65432        # Port to listen on (non-privileged ports are > 1023)


# THINGS THIS MODULE NEEDS:
## timeout
## protection against garbage colleciton (timeout might be enough)
## better logging
## reinstate connection if it is dropped / connection polling
### maybe have this if there is a change in the IP address...

def log(message):
	timestamp = datetime.now()
	print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + str(message))


class ServerConnection(object):

	smartbench_name_filepath = '/home/pi/smartbench_name.txt'
	smartbench_name = 'My SmartBench'

	sock = None
	HOST = ''
	prev_host = ''

	run_connection_loop = True

	poll_connection = None

	def __init__(self):
		Clock.schedule_once(self.initialise_server_connection, 10)



	def initialise_server_connection(self, dt):

		log("Initialising server connection...")

		self.HOST = self.get_ip_address()
		self.prev_host = self.HOST
		self.set_up_socket()
		self.poll_connection = Clock.schedule_interval(self.check_connection, 2)

	def set_up_socket(self):

		log("Attempting to set up socket...")

		if sys.platform != 'win32' and sys.platform != 'darwin':

			if self.HOST != '':

				try: 
					self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
				pass


	def do_connection_loop(self):

		log("Starting server connection loop...")

		while self.run_connection_loop:
			try:
				try: 
					conn, addr = self.sock.accept()
				except:
					# socket object isn't available for some reason, so kill loop
					# does this also need a close?? 
					self.close_and_reconnect_socket()
					break  
				log("Accepted connection with IP address " + str(self.HOST))
				try: 
					conn.send(self.smartbench_name)
				except: 
					print("Message not sent")
				# sleep(10)
				conn.close()
			except socket.timeout as e:
				log("Timeout: " + str(e))


	def close_and_reconnect_socket(self):

		try: 
			self.run_connection_loop = False
			self.sock.shutdown()
			self.sock.close()

		except Exception as e: 
			log("Attempted to close socket, but raised exception: " + str(e))

		Clock.schedule_once(lambda dt: self.set_up_socket(), 2)



	def check_connection(self, dt):

		self.HOST = self.get_ip_address()

		if self.HOST != self.prev_host:
			self.prev_host = self.HOST
			self.close_and_reconnect_socket()

		else:
			pass


	def get_ip_address(self):

		ip_address = ''

		if sys.platform == "win32":
			try:
				hostname=socket.gethostname()
				IPAddr=socket.gethostbyname(hostname)
				ip_address = str(IPAddr)

			except:
				ip_address = ''
		else:
			try:
				f = os.popen('hostname -I')
				first_info = f.read().strip().split(' ')[0]
				if len(first_info.split('.')) == 4:
					ip_address = first_info

				else:
					ip_address = ''

			except:
				ip_address = ''

		return ip_address

	def get_smartbench_name(self):
		try:
			file = open(self.smartbench_name_filepath, 'r')
			self.smartbench_name = str(file.read())
			file.close()

		except: 
			self.smartbench_name = 'My SmartBench'