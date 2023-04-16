import socket

# create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get the local machine name
host = socket.gethostname()

# set the port number to listen on
port = 12347

# bind the socket to a public host, and a port
server_socket.bind((host, port))

# set the number of clients that can be queued up
server_socket.listen(5)

print('Server listening on port', port)

# create a dictionary to store the ARP table
arp_table = {}

# enter a loop to listen for connections
while True:
    # wait for a client to connect
    client_socket, addr = server_socket.accept()
    
    print('Connected to', addr)

    
    # receive the MAC address from the client
    mac_address = client_socket.recv(1024).decode('ascii')
    
    print('Received MAC address', mac_address)
    
    # add the MAC address to the ARP table
    arp_table[mac_address] = addr
    
    # send a confirmation message to the client
    client_socket.send(b'ACK')
    
    # enter a loop to receive messages from the client
    while True:
        # receive a message from the client
        message = client_socket.recv(1024).decode('ascii')
        
        # check if the message is for all clients
        if message.startswith('all:'):
            # send the message to all clients except the sender
            sender_mac = [k for k, v in arp_table.items() if v == addr][0]
            for mac, client_addr in arp_table.items():
                if client_addr != addr:
                    send_message = f'{sender_mac}: {message[4:]}'
                    switch_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    switch_socket.connect(client_addr)
                    switch_socket.send(send_message.encode('ascii'))
                    switch_socket.close()
            
        # check if the message is for a specific client
        elif ':' in message:
            # get the MAC address of the recipient from the message
            recipient_mac = message.split(':')[0]
            
            # check if the MAC address is in the ARP table
            if recipient_mac in arp_table:
                # send the message to the recipient
                send_message = message.split(':')[1].strip()
                switch_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                switch_socket.connect(arp_table[recipient_mac])
                switch_socket.send(send_message.encode('ascii'))
                switch_socket.close()
                
                # send an acknowledgement to the sender
                sender_mac = [k for k, v in arp_table.items() if v == addr][0]
                ack_message = f'Message sent to {recipient_mac} ({arp_table[recipient_mac]})'
                client_socket.send(ack_message.encode('ascii'))
            
            else:
                # send an error message to the sender
                error_message = f'Error: MAC address {recipient_mac} not found in ARP table'
                client_socket.send(error_message.encode('ascii'))
        
        # if the message is not formatted correctly, send an error message to the sender
        else:
            error_message = 'Error: Message must be in the format "MAC address: message"'
            client_socket.send(error_message.encode('ascii'))
