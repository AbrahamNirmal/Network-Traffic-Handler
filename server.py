import socket
import threading

# Define a host and port for the server
HOST = '127.0.0.1'
PORT = 55555

# Create a socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the host and port
server.bind((HOST, PORT))

# Listen for incoming connections
server.listen()

# A list to hold all the clients that connect to the server
clients = []

# A dictionary to hold the switches
switches = {}

# A function to broadcast messages to all connected clients
def broadcast(message):
    for client in clients:
        client.send(message)

# A function to handle each client's connection to the server
def handle_client(client):
    while True:
        try:
            # Receive the client's message
            message = client.recv(1024)
            if message.decode('utf-8').startswith('/switch'):
                # Handle switch commands
                switch_command = message.decode('utf-8').split()
                if len(switch_command) != 3:
                    client.send('Invalid switch command. Usage: /switch [switch name] [on/off]'.encode('utf-8'))
                else:
                    switch_name = switch_command[1]
                    switch_state = switch_command[2].lower()
                    if switch_state == 'on':
                        switches[switch_name] = True
                        broadcast(f'Switch {switch_name} turned ON.'.encode('utf-8'))
                    elif switch_state == 'off':
                        switches[switch_name] = False
                        broadcast(f'Switch {switch_name} turned OFF.'.encode('utf-8'))
                    else:
                        client.send('Invalid switch state. Usage: /switch [switch name] [on/off]'.encode('utf-8'))
            elif message.decode('utf-8').startswith('/exit'):
                # Close the client's connection
                clients.remove(client)
                client.close()
                # Broadcast a message to all other clients that the client has disconnected
                message = f'{client.getpeername()} has left the chat.'.encode('utf-8')
                broadcast(message)
                break
            else:
                # Broadcast the message to all other clients
                for switch_name, switch_state in switches.items():
                    if switch_state:
                        broadcast(message)
        except:
            # If an error occurs, remove the client from the list and close the connection
            clients.remove(client)
            client.close()
            # Broadcast a message to all other clients that the client has disconnected
            message = f'{client.getpeername()} has left the chat.'.encode('utf-8')
            broadcast(message)
            break

# A function to continuously accept new client connections
def accept_clients():
    while True:
        # Accept a new client connection
        client, address = server.accept()
        # Add the client to the list of connected clients
        clients.append(client)
        # Broadcast a message to all other clients that a new client has joined
        message = f'{address} has joined the chat.'.encode('utf-8')
        broadcast(message)
        # Start a new thread to handle the client's connection
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

print('Server is running...')
# Start accepting new client connections
accept_clients()
