import socket
import json

import select


class Server:
    __ip = None
    __port = None
    __listening = False
    __server_socket = None
    __connection_list = []
    __functions = {}

    def __init__(self, **kwargs):
        self.__ip = kwargs["ip"]
        self.__port = kwargs["port"]

        self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__server_socket.bind((self.__ip, self.__port))

    def register_function(self, name, pointer):
        self.__functions[name] = pointer

    def listen(self):
        self.__listening = True
        self.__server_socket.listen(1)
        self.__connection_list.append(self.__server_socket)
        while self.__listening:
            READ_SOCKETS, WRITE_SOCKETS, ERROR_SOCKETS = select.select(self.__connection_list, [], [])
            for sock in READ_SOCKETS:  # New connection:
                # Handle the case in which there is a new connection recieved through server_socket
                if sock == self.__server_socket:
                    fd, addr = self.__server_socket.accept()
                    self.__connection_list.append(fd)  # add socket descriptor
                else:  # Some incoming message from a client
                    try:  # Data recieved from client, process it
                        data = sock.recv(4096)
                        if data:
                            try:
                                json_object = json.loads(data.decode())
                                print("DEBUG", json_object)
                                method_name = json_object.get("method", None)

                                if not method_name:
                                    raise Exception("Invalid method name!")

                                params = json_object.get("parameters", {})

                                ret = self.__functions[method_name](**params)
                                data_to_send = {
                                    "return": ret
                                }
                                sock.sendall(json.dumps(data_to_send).encode())
                            except Exception as e:
                                data_to_send = {
                                    "error": True,
                                    "message": str(e)
                                }
                                sock.sendall(json.dumps(data_to_send).encode())

                    except Exception as msg:
                        sock.close()
                        try:
                            self.__connection_list.remove(sock)
                        except ValueError as msg:
                            print("{}:{}.".format(type(msg).__name__, msg))
                        continue


server_singleton = Server(ip="", port=6666)


def remote_method(func):
    server_singleton.register_function(func.__name__, func)

    def wrapper(*args):
        func_result = func(*args)
        return func_result

    return wrapper


# dummy code

GLOBAL_DUMMY = 0


@remote_method
def set_global_dummy(value):
    global GLOBAL_DUMMY
    GLOBAL_DUMMY = value
    return True


@remote_method
def get_global_dummy():
    global GLOBAL_DUMMY
    return GLOBAL_DUMMY


def main():
    server_singleton.listen()


if __name__ == '__main__':
    main()
