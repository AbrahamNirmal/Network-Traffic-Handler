import socket
import threading
from cryptography.fernet import Fernet

# Prompt the user to enter their MAC address
mac_address = input("Enter your MAC address: ")

# Generate a key for encryption
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect(('192.168.1.42', 5000))

# Send the MAC address to the server
client_socket.send(mac_address.encode())

# Receive the encryption key from the server
key = client_socket.recv(1024)
cipher_suite = Fernet(key)

def receive():
    global cipher_suite

    while True:
        # Receive data from the server
        data = client_socket.recv(1024)

        # Decrypt the data
        decrypted_data = cipher_suite.decrypt(data)

        if not data:
            # Close the socket if the server has disconnected
            client_socket.close()
            break
        else:
            # Print the decrypted data
            print(decrypted_data.decode())

def send():
    global cipher_suite
try:
    while True:
        # Prompt the user to enter a message
        message = input("")

        # Encrypt the message and append the recipient's MAC address
        recipient_mac_address = input("Enter the recipient's MAC address: ")
        encrypted_message = cipher_suite.encrypt(f"{recipient_mac_address}:{message}".encode())

        # Send the encrypted message to the server
        client_socket.send(encrypted_message)
except EOFError:
        print("User disconnected or won't exist")
except KeyboardInterrupt:
        print("Program interrupted by user. Exiting...")
receive_thread = threading.Thread(target=receive)
send_thread = threading.Thread(target=send)

receive_thread.start()
send_thread.start()
