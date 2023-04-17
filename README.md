# End to End Communication between clients with automatic ARP updating.

In this project we’ve implemented an end-end communication between multiple clients with a client and server code where we have a switch in the server implementation that automatically updates the mac addresses of the connected clients to the ARP table.

We can run the client code on different machines connected over a network and pass messages between each client, the client can select which client they wish to send the message to and once the message is broadcasted the server checks if the MAC address is present in the ARP table and sends the message to the respective client and if the MAC address is not present in the ARP table it shows the error and broadcasts the message to all the clients.


The main functions in the code that handle the ARP table and message passing are:

 add_to_arp_table():  is called when a new client connects to the server, and it adds an entry to the ARP table.

send_message(): is called when a client wants to send a message to another client, and it uses the ARP table to get the recipient's socket address.

handle_client(): is called in a new thread for each connected client, and it listens for incoming messages and calls send_message() to forward them to the appropriate recipient.


How to run the code:

First clone the code and run the server code.

Next run the client code on any number of machines and it will prompt to enter the mac address and once you enter the mac address it gets updated in the ARP table.

Each time a new client joins the other clients are notified that a new client has joined the chat, and you can enter the message to be sent and enter the mac address of the client the message is to be sent to.

And then after everything is done we can close client connections.

Requirements:

Install Python.

Commands:

Python switch_server.py

Python client1.py



