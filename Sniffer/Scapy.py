from scapy.all import *


def show_packet(packet):
    print(packet.show())

sniff(filter="icmp",iface="en0",prn=show_packet,count=10)