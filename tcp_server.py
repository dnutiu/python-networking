#!/usr/bin python3
""" A simple chat TCP server """
import socket
import select

def broadcast_data (sock, message):
    """ Sends a message to all sockets in the connection list except for itself. """
    # Do not send the message to master socket and the client who has send us the message
    for SOCKET in CONNECTION_LIST:
        if SOCKET != SERVER_SOCKET:
            try:
                SOCKET.sendall(message)
            except: # Connection was closed.
                SOCKET.close()
                try:
                    CONNECTION_LIST.remove(socket)
                except ValueError:
                    print("Can't remove socket")

CONNECTION_LIST = []
RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2
PORT = 1337

SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER_SOCKET.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
SERVER_SOCKET.bind(("", PORT)) # empty addr string means INADDR_ANY

print("Listening...")
SERVER_SOCKET.listen(10) # 10 connections

CONNECTION_LIST.append(SERVER_SOCKET)
print("Server started!")

while True:
    # Get the list sockets which are ready to be read through select
    READ_SOCKETS, WRITE_SOCKETS, ERROR_SOCKETS = select.select(CONNECTION_LIST, [], [])
    for SOCK in READ_SOCKETS: # New connection
        if SOCK == SERVER_SOCKET: # Handle the case in which there is a new connection recieved through server_socket
            SOCKFD, ADDR = SERVER_SOCKET.accept()
            CONNECTION_LIST.append(SOCKFD) # add socket descriptor
            print("Client ({0}, {1}) connected".format(ADDR[0], ADDR[1]))
            broadcast_data(SOCKFD, "[{0}:{1}] entered room\n".format(ADDR[0],
                                    ADDR[1]).encode())
        else: # Some incoming message from a client
            try: # Data recieved from client, process it
                DATA = SOCK.recv(RECV_BUFFER)
                if DATA:
                    message = "[{}:{}]:{}".format(ADDR[0], ADDR[1], DATA.decode())
                    print(message, end = "")
                    broadcast_data(SOCK, message.encode())
            except Exception as msg:
                print(type(msg).__name__, " occured just now")
                broadcast_data(SOCK, "Client ({0}, {1}) is offline\n"
                                     .format(ADDR[0], ADDR[1]).encode())
                print("Client ({}, {}) is offline".format(ADDR[0], ADDR[1]))
                SOCK.close()
                try:
                    CONNECTION_LIST.remove(SOCK)
                except ValueError:
                    print("Can't remove element.")
                continue

SERVER_SOCKET.close()
