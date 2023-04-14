# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 17:29:25 2023

@author: kurra
"""

import socket
import threading

# Define a host and port for the switch
HOST = '127.0.0.1'
PORT = 55555

# Define the MAC address table for the switch
mac_table = {}

# Create a socket object
switch = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the host and port
switch.bind((HOST, PORT))

# Listen for incoming connections
switch.listen()

# A list to hold all the connected devices
devices = []

# A function to handle each device's connection to the switch
def handle_device(device, port):
    while True:
        try:
            # Receive the device's packet
            packet = device.recv(1024)
            print(packet)
            # Get the source MAC address from the packet
            src_mac = packet[:6]
            # Get the destination MAC address from the packet
            dst_mac = packet[6:12]
            # Update the MAC address table with the source MAC address and port
            mac_table[src_mac] = port
            # Check if the destination MAC address is in the MAC address table
            if dst_mac in mac_table:
                # Forward the packet to the appropriate port
                dst_port = mac_table[dst_mac]
                for dev in devices:
                    if dev['port'] == dst_port:
                        dev['device'].send(packet)
            else:
                # Broadcast the packet to all connected devices
                for dev in devices:
                    if dev['device'] != device:
                        dev['device'].send(packet)
        except:
            # If an error occurs, remove the device from the list and close the connection
            devices.remove({'device': device, 'port': port})
            device.close()
            # Remove the device's MAC address from the MAC address table
            for mac, prt in mac_table.items():
                if prt == port:
                    del mac_table[mac]
            break

# A function to continuously accept new device connections
def accept_devices():
    while True:
        # Accept a new device connection
        device, address = switch.accept()
        # Get the MAC address of the device from the first packet
        mac = device.recv(1024)[:6]
        # Get the port number of the device based on the number of connected devices
        port = len(devices) + 1
        # Add the device and port to the list of connected devices
        devices.append({'device': device, 'port': port})
        # Add the device's MAC address to the MAC address table
        mac_table[mac] = port
        print(f"Device with MAC address {mac.hex()} connected to port {port}")
        # Start a new thread to handle the device's connection
        thread = threading.Thread(target=handle_device, args=(device, port))
        thread.start()

print('Switch is running...')
# Start accepting new device connections
accept_devices()
