# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 17:50:59 2023

@author: kurra
"""

import socket

# Create a TCP socket and bind it to the server's IP address and port
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 1235))
sock.listen()

print("[INFO] Server started")

while True:
    # Wait for a client to connect
    conn, addr = sock.accept()
    print(f"[INFO] Client {addr} connected to server")

    while True:
        # Receive data from the client
        data = conn.recv(1024)
        if not data:
            break
        print(f"[INFO] Received message from client: {data.decode()}")

        # Send a response to the client
        response = f"Received message: {data.decode()}"
        conn.send(response.encode())

    # Close the connection with the client
    conn.close()

