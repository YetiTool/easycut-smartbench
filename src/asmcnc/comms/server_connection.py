import socket
import sys

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

class ServerConnection(object):

	def __init__(self):

		if sys.platform != "win32" and sys.platform != "darwin":

			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.sock:
				self.sock.bind((HOST, PORT))
				self.sock.listen()
				self.do_connection_loop()

	def do_connection_loop(self):

		while True:
			conn, addr = self.sock.accept()
			print("Connected to Archie's app")
			conn.send('HAI I AM SMARTBENCH')
			conn.close() 