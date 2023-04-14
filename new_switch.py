# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 18:06:20 2023

@author: kurra
"""

import socket
import struct

def handle_device(device, conn):
    # Get device's MAC address
    mac = device.recv(6)
    # Add device's MAC address and connection to the mac_table
    mac_table[mac] = conn
    print(f"[INFO] Device {mac} connected to switch")

def handle_packet(packet, conn):
    # Extract the destination MAC address from the packet
    dst_mac = packet[:6]
    # If the destination MAC address is not in the mac_table, flood the packet
    if dst_mac not in mac_table:
        print("[INFO] Destination MAC address not found in mac_table. Flooding packet.")
        for _, device_conn in mac_table.items():
            if device_conn != conn:
                device_conn.send(packet)
    else:
        # If the destination MAC address is in the mac_table, send the packet to the appropriate device
        device_conn = mac_table[dst_mac]
        device_conn.send(packet)

# Create a UDP socket and bind it to the switch's IP address and port
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('localhost', 1234))

# Define a dictionary to store MAC addresses and their corresponding connections
mac_table = {}

print("[INFO] Switch started")

while True:
    # Receive data from a device
    data, addr = sock.recvfrom(1024)
    conn = addr[0], addr[1]
    print(mac_table)
    # If the data is a device registration message, handle it
    if data == b"register":
        handle_device(sock, conn)
    else:
        # If the data is a packet, handle it
        handle_packet(data, conn)
