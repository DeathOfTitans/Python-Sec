from scapy.all import *


def show_packet(packet):
    print(packet.show())

sniff(filter="icmp",iface="wlan0",prn=show_packet,count=10)