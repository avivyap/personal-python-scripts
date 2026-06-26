#!/usr/bin/env python3

import signal
import sys
import socket
import select,sys
import argparse
from termcolor import colored

def description():

	parser = argparse.ArgumentParser(description="listener")
	parser.add_argument("-p", "--port", dest="port", type=int, required=True, help="Port to start listen")

	options = parser.parse_args()
	return options

def def_handler(sig,frame):

	print(colored("\n[+] Exiting...\n",'red'))
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

		print(f"Listening on 0.0.0.0 {port}")

		socket_client, ip_client = sock.accept()

		info_client = f"{ip_client}"

		print("Connection received on " + info_client)

		while True:

			r, _, _ = select.select([socket_client, sys.stdin], [], [])

			for i in r:

				if i == socket_client:
					data = socket_client.recv(1024)

					if not data:
						return

					print(data.decode(errors="ignore"), end="")

				else:
					msg = sys.stdin.readline()
					socket_client.send(msg.encode())

		socket_client.close()
		sock.close()

	except PermissionError:

		print(colored("\n[!] To use this port, you must be root.\n",'red'))
		return


	except OSError:

		print(colored("\n[!] The port is in use.\n",'red'))
		return

def main():

	options = description()
	port = options.port

	socket = create_socket()

	listener(socket, port)

if __name__ == '__main__':

	main()
