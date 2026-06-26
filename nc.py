#!/usr/bin/env python3

import signal
import sys
import socket
import socket
import argparse
from termcolor import colored

def description():

	parser = argparse.ArgumentParser(description="listener")
	parser.add_argument("-p", "--port", dest="port", type=int, required=True, help="Port to start listen")

	options = parser.parse_args()
	return options

def def_handler(sig,frame):

	print(colored("\n[+] Saliendo...\n",'red'))
	sys.exit(1)


signal.signal(signal.SIGINT, def_handler)

def create_socket():

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4 & TCP
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	return s

def listener(sock, port):

	try:

		sock.bind(("0.0.0.0", port))
		sock.listen(1)

		print("Listening on 0.0.0.0 1212")

		socket_client, ip_client = sock.accept()

		while True:

			try:
				data = socket_client.recv(1024)

				if not data:

					break

				print(data.decode(errors="ignore"), end="")

				cmd = input() + "\n"
				socket_client.send(cmd.encode())


			except KeyboardInterrupt:

				break

		socket_client.close()
		sock.close()


	except OSError:

		print(colored("\n[!] El puerto esta en uso\n",'red'))

def main():

	options = description()
	port = options.port

	socket = create_socket()

	listener(socket, port)

if __name__ == '__main__':

	main()
