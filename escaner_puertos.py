#!/usr/bin/env python3

import socket
import argparse, os
import signal, subprocess
import threading
import sys
from tqdm import tqdm
import time


def def_handler(sig, frame):

	print("\n[!] Saliendo del programa\n")
	sys.exit(1)

signal.signal(signal.SIGINT, def_handler)


def get_arguments():

	parser = argparse.ArgumentParser(description='Escaner de puertos con objetos')
	parser.add_argument("-t", "--target", dest="target", required=True, help="Introduce una ip para hacerle el escaneo de puertos")

	options = parser.parse_args()

	return options.target


class Target:

	def __init__(self, ip):
		self.ip = ip
		self.lista_puertos = []
	def hilos(self):

		lista_hilos = []

		start = time.time()
		for port in tqdm(range(1,65536)):
			hilo = threading.Thread(target=self.agregar_puerto, args=(port,))
			hilo.start()
			lista_hilos.append(hilo)

		for hilo in lista_hilos:

			hilo.join()

		stop = time.time()

		tiempo = stop - start

		self.mostrar_puertos(tiempo)

	def mostrar_puertos(self, tiempo):

		print("\n--------------------Puertos abiertos--------------------\n")

		for port in self.lista_puertos:
			print(f"\t [+] {port}")

		print(f"\n[t] El escaneo a durado {tiempo} segundos")

	def agregar_puerto(self, puerto):


		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(1)

		if s.connect_ex((self.ip, puerto)) == 0:
			self.lista_puertos.append(puerto)
			s.close()
		else:
			s.close()

	def __str__(self):

		return ("\n[+] Escaneo de puertos de una ip concreta\n")


if __name__ == '__main__':

	ip = get_arguments()

	objeto = Target(ip)
	objeto.hilos()

