#!/usr/bin python3
""" TCP Client """

import socket
import select
import sys

def prompt() :
    sys.stdout.write("<You> ")
    # sys.stdout.flush()

if(len(sys.argv) < 3):
    print("Usage : python {0} hostname port".format(sys.argv[0]))
    sys.exit()

host = sys.argv[1]
port = int(sys.argv[2])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(200)

# connect to remote host
try:
    s.connect((host, port))
except:
    print("Unable to connect")
    sys.exit()

print("Connected to remote host. Start sending messages")

while True:
    socket_list = [sys.stdin, s]
    # Get the list sockets which are readable
    read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])

    for sock in read_sockets: #incoming message from remote server
        if sock == s:
            data = sock.recv(4096)
            if not data:
                print('\nDisconnected from chat server')
                sys.exit()
            else: # print data
                print(data.decode(), end="")
        else: #user entered a message
            msg = sys.stdin.readline()
            print("\x1b[1A" + "\x1b[2K", end="") # erase last line
            s.sendall(msg.encode())
