#!/usr/bin/env python3


import socket, sys, time

target = sys.argv[1]

def traceroute(dest):
    ttl = 1
    while True:
        receiver = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sender.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
        sender.sendto(b'data', (dest, 33434))
        receiver.settimeout(2)
        try:
            data, addr = receiver.recvfrom(1024)
            print(ttl, addr[0])
            if addr[0] == dest:
                break
        except:
            print(ttl, "*")
        ttl += 1

traceroute(target)

