#!/usr/bin python3
""" TCP Client """

import socket
import select
import sys

if len(sys.argv) < 3:
    print("Usage : python {0} hostname port".format(sys.argv[0]))
    sys.exit()

HOST = sys.argv[1]
PORT = int(sys.argv[2])

MASTER_SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
MASTER_SOCK.settimeout(200)

# connect to remote host
try:
    MASTER_SOCK.connect((HOST, PORT))
except Exception as msg:
    print(type(msg).__name__)
    print("Unable to connect")
    sys.exit()

print("Connected to remote host. Start sending messages")

while True:
    SOCKET_LIST = [sys.stdin, MASTER_SOCK]
    # Get the list sockets which are readable
    READ_SOCKETS, WRITE_SOCKETS, ERROR_SOCKETS = select.select(SOCKET_LIST, [], [])

    for sock in READ_SOCKETS: #incoming message from remote server
        if sock == MASTER_SOCK:
            data = sock.recv(4096)
            if not data:
                print('\nDisconnected from chat server')
                sys.exit()
            else: # print data
                print(data.decode(), end="")
        else: #user entered a message
            msg = sys.stdin.readline()
            print("\x1b[1A" + "\x1b[2K", end="") # erase last line
            MASTER_SOCK.sendall(msg.encode())
