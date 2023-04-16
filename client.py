import socket

# create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get the local machine name
host = socket.gethostname()
# set the port number to match the switch
port = 12346

# connect to the switch
client_socket.connect((host, port))

# send the MAC address to the switch
mac_address = input('Enter MAC address: ')
client_socket.send(mac_address.encode('ascii'))

# wait for the switch to acknowledge the MAC address
ack = client_socket.recv(1024).decode('ascii')
print(ack)
if ack != 'ACK':
    print('Error: Switch did not acknowledge MAC address')
    client_socket.close()
    exit()
# enter a loop to send messages
while True:
    # get the destination MAC address and message from the user
    dest_mac = input('Enter destination MAC address (or "all" to send to all clients): ')
    message = input('Enter message: ')
    msg="mac"
    # send the message to the switch
    send_message = f'{msg}:{dest_mac}:{message}'
    client_socket.send(send_message.encode('ascii'))
    
    print("sucessfully sent to switch")
    # wait for a response from the switch
    response = client_socket.recv(1024).decode('ascii')
    
    # print the response from the switch
    print(response)
