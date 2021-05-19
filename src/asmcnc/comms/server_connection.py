import socket
import sys
import threading
from time import sleep

# HOST = ''  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

class ServerConnection(object):

	sock = None
	HOST = None

	def __init__(self):

		if sys.platform != 'win32' and sys.platform != 'darwin':

			self.HOST = self.get_ip_address()

			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock.bind((self.HOST, PORT))
			self.sock.listen(5)

			t = threading.Thread(target=self.do_connection_loop)
			t.daemon = True
			t.start()

	def do_connection_loop(self):

		print("loop starting")

		while True:
			print("loop running")
			conn, addr = self.sock.accept()
			print("Connected to Archie's app")
			try: conn.send("HAI I AM SMARTBENCH","utf-8")
			except: print("could not send")
			sleep(10)
			conn.close()


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