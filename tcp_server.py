""" Simple TCP Server """
import socket

def print_client_response(data):
    """ Will print client response in a new manner """
    print("===BEGIN CLIENT RESPONSE")
    print("Client send: {0}".format(data.decode()))
    print("===END CLIENT RESPONSE")

SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SOCKET.bind(('', 1337)) # empty addr string means INADDR_ANY

print("Listening...")
SOCKET.listen(1)
CLIENT, ADDR = SOCKET.accept()
print("Connected by", ADDR)
while True:
    DATA = CLIENT.recv(1024)
    if not DATA or DATA.decode()[0:4].find("exit") != -1:
        print("Client requested exit.")
        break
    print_client_response(DATA)
    CLIENT.sendall("Echo: {0}".format(DATA.decode()).encode()) # must encode()
CLIENT.close()
