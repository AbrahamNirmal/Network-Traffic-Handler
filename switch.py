import socket

# create a dictionary for the ARP table
arp_table = {}

# create a socket object
switch_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get the local machine name
host = socket.gethostname()

# set the port number
port = 12346

# bind the socket to a specific address and port
switch_socket.bind((host, port))

# listen for incoming connections
switch_socket.listen(3)

# wait for two clients to connect
client_sockets = []
while len(client_sockets) < 3:
    client_socket, address = switch_socket.accept()
    print("Connection from: ", address)
    
    # receive the first message from the client
    message = client_socket.recv(1024)
    print(message.decode('ascii'))
    acknowledgement = bytes('ACK', 'utf-8')
    client_socket.send(acknowledgement)
    
    # update the ARP table with the MAC address of the client
    arp_entry = message.decode('ascii')
    print(arp_entry)
    arp_table[arp_entry] = client_socket
    client_sockets.append(client_socket)
print("entering into packet exchange")
print(arp_table)
while True:
    # receive a message from a client
    message = client_sockets[0].recv(1024)
    if message:
        print(message.decode('ascii'))
        chunks=message.decode('ascii').split(':')
        print(chunks)
        # check if the message is for a specific client or all clients
        if chunks[0]=='mac':
            mac_address = chunks[1]
            print('Found mac in message')
            if mac_address in arp_table:
                # forward the message to the specified client
                client_socket = arp_table[mac_address]
                client_socket.send(message)
            else:
                # send an error message back to the client
                response = "Error: MAC address not found in ARP table."
                client_sockets[0].send(response.encode('ascii'))
        else:
            # forward the message to all clients
            for mac_address, client_socket in arp_table.items():
                client_socket.send(message)
    
    # receive a message from the other client
    message = client_sockets[1].recv(1024)
    if message:
        print(message.decode('ascii'))
        
        # check if the message is for a specific client or all clients
        if "to MAC address " in message.decode('ascii'):
            mac_address = message.decode('ascii').split("to MAC address ")[-1][:-1]
            if mac_address in arp_table:
                # forward the message to the specified client
                client_socket = arp_table[mac_address]
                client_socket.send(message)
            else:
                # send an error message back to the client
                response = "Error: MAC address not found in ARP table."
                client_sockets[1].send(response.encode('ascii'))
        else:
            # forward the message to all clients
            for mac_address, client_socket in arp_table.items():
                client_socket.send(message)

# close the sockets
client_sockets[0].close()
client_sockets[1].close()
switch_socket.close()
