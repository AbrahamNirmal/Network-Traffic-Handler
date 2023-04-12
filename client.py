import socket
import threading

# Define a host and port for the server
HOST = '127.0.0.1'
PORT = 55555

# Create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client.connect((HOST, PORT))

# A function to continuously receive messages from the server
def receive_messages():
    while True:
        try:
            # Receive the server's message
            message = client.recv(1024).decode('utf-8')
            # Print the message
            print(message)
        except:
            # If an error occurs, close the connection
            client.close()
            break

# Start a new thread to continuously receive messages from the server
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# A loop to continuously send messages to the server
while True:
    message = input('')
    # Send the message to the server
    client.send(message.encode('utf-8'))
