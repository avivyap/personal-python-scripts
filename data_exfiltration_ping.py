#!/usr/bin/env python3

import sys
import signal
from scapy.all import sniff, ICMP, Raw

decoded_output = ""


def signal_handler(sig, frame):
    print("\n[!] Saliendo...")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


def process_packet(packet):
    global decoded_output

    if not packet.haslayer(ICMP) or packet[ICMP].type != 8:
        return

    if not packet.haslayer(Raw):
        return

    payload = packet[Raw].load
    last_4_bytes = payload[-4:]

    try:
        decoded_chars = last_4_bytes.decode("utf-8", errors="ignore")
        decoded_output += decoded_chars
        print(decoded_chars, end="", flush=True)
    except Exception as e:
        pass

def main():

    sniff(
        iface="tun0",
        filter="icmp",
        prn=process_packet,
        store=False
    )


if __name__ == "__main__":
    main()
