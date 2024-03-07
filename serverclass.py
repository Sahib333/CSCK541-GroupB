import socket
import pickle
import json
import xml.etree.ElementTree as ET
from cryptography.fernet import Fernet

class Server:
    """ Server class"""
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket()
        self.server_socket.bind(host, port)
        self.server_socket.listen(5)

    def connect(self):
        """connect"""
        print(f"Server listening on {self.host}:{self.port}")
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Connection from {addr}")
            self.handle_client(client_socket)

    def handle_client(self, client_socket):
        """Receive data type (dictionary or text file)"""
        data_type = client_socket.recv().decode()

        if data_type == "dictionary":
            format_encryption = client_socket.recv().decode().split(",")
            data_format = format_encryption[0]
            encrypted = format_encryption[1]

            data = client_socket.recv()

            dictionary = self.handle_data (data, data_format, encrypted)
            print("Dictionary received")

            # Save to a file
            with open("received_dictionary.txt","w", encoding="utf-8") as my_file:
                my_file.write(str(dictionary))

        elif data_type == "text":
            encrypted = client_socket.recv().decode()

            data = client_socket.recv()

            if encrypted:
                # Decrypt data
                fernet = Fernet(b"secretpassword")
                decrypted_data = fernet.decrypt(data)

            # Save to a file
            with open("received_text.txt","wb") as my_file:
                my_file.write(decrypted_data)

        client_socket.close()

    def handle_data (self, data, data_format, encrypted):
        """data handler"""
        if data_format == "binary":
            if encrypted:
                # Decrypt data
                fernet = Fernet(b"secretpassword")
                decrypted_data = fernet.decrypt(data)
            return pickle.loads(decrypted_data)

        elif data_format == "json":
            return json.loads(data.decode())

        elif data_format == "xml":
            return ET.fromstring(data.decode())

if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 12345

    server = Server(HOST, PORT)
    server.connect()
