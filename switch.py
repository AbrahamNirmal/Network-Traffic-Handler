import socket
import threading
import select
from cryptography.fernet import Fernet

# Generate a key for encryption
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the socket object to a specific IP address and port number
server_socket.bind(('localhost', 5000))

# Listen for incoming connections
server_socket.listen()

# Create a dictionary to keep track of connected clients
clients = {}

# Create a dictionary to keep track of MAC addresses
arp_table = {}

def handle_client(client_socket, addr):
    global clients, cipher_suite, key, arp_table

    # Add the client to the clients dictionary
    clients[addr] = client_socket

    # Receive the client's MAC address
    mac_address = client_socket.recv(1024).decode()

    # Add the MAC address to the ARP table
    arp_table[mac_address] = addr

    # Notify all clients that a new client has connected
    broadcast(f"{mac_address} has joined the chat!".encode(), client_socket)

    while True:
        try:
        # Receive data from the client
            data = client_socket.recv(1024)

            # Decrypt the data
            decrypted_data = cipher_suite.decrypt(data)
            if not data:
                # Remove the client from the clients dictionary and ARP table
                del clients[addr]
                del arp_table[mac_address]

                # Notify all clients that a client has disconnected
                broadcast(f"{mac_address} has left the chat!".encode(), client_socket)
                break
            else:
                # Determine the recipient of the message
                print(decrypted_data)
                decrypted_data = decrypted_data.decode()
                recipient_mac_address = decrypted_data.split(":")[0]
                #recipient_mac_address = recipient_mac_address.split('b')[1]
                print(recipient_mac_address)
                # Check if the recipient is in the ARP table
                if recipient_mac_address in arp_table:
                    recipient_socket = clients[arp_table[recipient_mac_address]]
                    decrypted_data = bytes(decrypted_data,'utf-8')
                    # Send the encrypted message to the recipient
                    recipient_socket.send(cipher_suite.encrypt(decrypted_data))
                else:
                    # Notify the sender that the recipient is not available
                    client_socket.send(cipher_suite.encrypt(f"Recipient {recipient_mac_address} is not available".encode()))
                    broadcast(decrypted_data.encode(), sock)
        except Exception as e:
            print(f"cleint doesn't exist {addr}: {e}")
            break

def broadcast(data, sender_socket):
    global clients, cipher_suite

    encrypted_data = cipher_suite.encrypt(data)

    for client_addr, client_socket in clients.items():
        if client_socket != sender_socket:
            client_socket.send(encrypted_data)

def add_mac_address():
    global arp_table
    mac_address = input("Enter MAC address: ")
    ip_address = input("Enter IP address: ")
    arp_table[mac_address] = ip_address

def delete_mac_address():
    global arp_table
    mac_address = input("Enter MAC address: ")
    if mac_address in arp_table:
        del arp_table[mac_address]
    else:
        print(f"MAC address {mac_address} not found in ARP table.")

def show_arp_table():
    global arp_table
    for mac_address, ip_address in arp_table.items():
        print(f"MAC address: {mac_address}, IP address: {ip_address}")
while True:
    read_sockets, _,exception_sockets = select.select([server_socket] + list(clients.values()), [], [])
    print(arp_table)
    for sock in read_sockets:
        if sock == server_socket:
            client_socket, addr = server_socket.accept()
            print(addr)
            client_socket.send(key)
            threading.Thread(target=handle_client, args=(client_socket, addr)).start()
        else:
            try:
                data = sock.recv(1024)
                decrypted_data = cipher_suite.decrypt(data)
                decrypted_data = decrypted_data.decode()
                recipient_mac_address = decrypted_data.split(":")[0]
                print(recipient_mac_address)
                if recipient_mac_address in arp_table:
                    recipient_socket = clients[arp_table[recipient_mac_address]]
                    recipient_socket.send(cipher_suite.encrypt(decrypted_data))
                else:
                    client_socket.send(cipher_suite.encrypt(f"Recipient {recipient_mac_address} is not andu".encode()))
                    broadcast(decrypted_data.encode(), sock)
            except:
                mac_address = [k for k, v in clients.items() if v == sock][0]
                print("mac addres to be removed is",mac_address)
                inv_map = {v: k for k, v in arp_table.items()}
                del clients[mac_address]
                mac_address = inv_map[mac_address]
                print(arp_table)
                del arp_table[mac_address]
                broadcast(f"{mac_address} has left the chat!".encode(), sock)
                sock.close()
                break