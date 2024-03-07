"""A server class"""

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
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)

    def connect(self):
        """Connect to the client"""
        print(f"Server listening on {self.host}:{self.port}")
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Connection from {addr}")
            self.handle_client(client_socket)
            client_socket.close()

    def handle_client(self, client_socket):
        """Receive data type (dictionary or text file)"""
        # Converting the data received into a string
        received_data = client_socket.recv(BUFFER_SIZE).decode()
        print(received_data)
        msg_parts = received_data.split(",")
        data_type = msg_parts[0]

        if data_type == "dictionary":
            print("Data type: dictionary")
            data_format = msg_parts[1]
            data = str(msg_parts[2:])
            print(data)
            print(type(data))

            dictionary = self.deserialize_dictionary (data, data_format)
            print("Dictionary received")

            # Save to a file
            with open("received_dictionary.txt","w", encoding="utf-8") as my_file:
                my_file.write(str(dictionary))

        elif data_type == "text":
            data = msg_parts[1]
            encrypted = bool(msg_parts[2])
            print(data)
            print(type(encrypted))

            #if encrypted:
            #    # Decrypt data
            #    fernet = Fernet(b"secretpassword")
            #    data = fernet.decrypt(data)

            # Save to a file
            with open("received_text.txt","wb") as my_file:
                my_file.write(data)

    def deserialize_dictionary (self, data, data_format):
        """Deserialize the data received by the client depending on its format"""
        if data_format == "binary":
            return pickle.loads(data)

        elif data_format == "json":
            return json.loads(data)

        elif data_format == "xml":
            return ET.fromstring(data)

if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 12345
    BUFFER_SIZE = 1024

    server = Server(HOST, PORT)
    server.connect()
