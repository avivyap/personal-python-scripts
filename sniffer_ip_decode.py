#!/usr/bin/env python3

from ctypes import *
import socket
import struct
import sys
import os

class IP(Structure):

	_fields_ = [

		("version",             c_ubyte,        4),
		("ihl",                 c_ubyte,        4),
		("tos",                 c_ubyte,        8),
		("len",                 c_ushort,       16),
		("id",                  c_ushort,       16),
		("offset",              c_ushort,       16),
		("ttl",                 c_ubyte,        8),
		("protocol_num",        c_ubyte,        8),
		("sum",                 c_ushort,       16),
		("src",                 c_uint32,       32),
		("dst",                 c_uint32,       32)

]
	def __new__(cls, socket_buffer=None):
		return cls.from_buffer_copy(socket_buffer) #esto lo que hace es recibir el buffer que es un conjunto de bytes sin iterpretar y pasarlos por la tablita de arriba y traducirlo

	def __init__(self, socket_buffer=None):

		self.src_address = socket.inet_ntoa(struct.pack("<L", self.src))
		self.dst_address = socket.inet_ntoa(struct.pack("<L", self.dst))


def sniff(host):

	if os.name == 'nt':

		socket_protocol = socket.IPPROTO_IP

	else:

		socket_protocol = socket.IPPROTO_ICMP

	sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)

	sniffer.bind((host, 0))

	sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

	if os.name == 'nt':

			sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

	protocols = {

		1:"ICMP",
		6: "TCP",
		17: "UDP",
		2: "IGMP",
		89: "OSPF"
}

	try:

		while True:

			raw_buffer = sniffer.recvfrom(65535)[0]
			ip_header = IP(raw_buffer[0:20]) #mirar esto
			protocol_name = protocols.get(ip_header.protocol_num, f"Desconocido({ip_header.protocol_num})")
			print(f"[+] Protocolo: {protocol_name} {ip_header.src_address} -> {ip_header.dst_address}")

	except KeyboardInterrupt:

		if os.name == 'nt':
			sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

		sys.exit()



if __name__ == '__main__':

	if len(sys.argv) == 2:

		host = sys.argv[1]

	else:

		host = '192.168.88.4'

	sniff(host)
