import socket
import sys
import threading
from time import sleep

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

class ServerConnection(object):

	sock = None

	def __init__(self):

		if sys.platform != 'win32' and sys.platform != 'darwin':

			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock.bind((HOST, PORT))
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