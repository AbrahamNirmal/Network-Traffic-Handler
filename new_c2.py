# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 17:51:09 2023

@author: kurra
"""

import socket
import time

# Create a TCP socket and connect it to the server's IP address and port
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 1235))

# Send a message to the server
message = "Hello from client 1"
sock.send(message.encode())
print(f"[INFO] Sent message from client 1: {message}")

# Wait for the switch to update its MAC table
time.sleep(2)

# Send a message to client 2 through the switch
message = "Hello from client 1 to client 2"
dst_mac = b'\x00\x11\x22\x33\x44\x55'  # MAC address of client 2
packet = dst_mac + message.encode()
sock.send(packet)
print(f"[INFO] Sent message from client 1 to client 2: {message}")

# Close the connection with the server
sock.close()
