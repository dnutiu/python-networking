import socket
import json


class ClientException(Exception):
    def __init__(self, message):
        super().__init__(message)


class RemoteException(Exception):
    def __init__(self, message):
        super().__init__(message)


class Client:
    __ip = None
    __port = None
    __connected = False
    __received_data = None
    __socket = None

    def __init__(self, **kwargs):
        self.__ip = kwargs["ip"]
        self.__port = kwargs["port"]
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __handle_received_data(self):
        if self.__received_data:
            json_dict = json.loads(self.__received_data)

            if json_dict.get("error", False):
                raise RemoteException("Exception: {}".format(json_dict.get("message", None)))

            return json_dict.get("return", None)
        else:
            raise ClientException("Response is empty!")

    def remote_call(self, method, **kwargs):
        if self.__connected:
            # Make the method call
            data_to_send = {
                "method": method,
                "parameters": kwargs
            }
            self.__socket.sendall(json.dumps(data_to_send).encode())
            # Handle response
            data = self.__socket.recv(4096)
            if not data:
                raise ClientException("Error receiving data from remote end! Broken pipe.")
            else:
                self.__received_data = data.decode()
                return self.__handle_received_data()

        else:
            raise ClientException("Currently not connected!")

    def connect(self):
        try:
            self.__socket.connect((self.__ip, self.__port))
            self.__connected = True
        except Exception:
            raise ClientException(
                "Could not connect to remote host! ip: {0} server: {1}\n".format(self.__ip, self.__port))


def main():
    client = Client(ip="127.0.0.1", port=6666)
    client.connect()

    x = client.remote_call("get_global_dummy")
    print(x)
    x = client.remote_call("set_global_dummy", value=10)
    print(x)
    x = client.remote_call("get_global_dummy")
    print(x)


if __name__ == '__main__':
    main()
