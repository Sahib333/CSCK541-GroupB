"""A server class"""

import socket
import pickle
import json
import xml.etree.ElementTree as ET
from cryptography.fernet import Fernet

class Server:
    """ Server class"""
    def __init__(self, host, port, print_screen = False, save_file = False):
        self.host = host
        self.port = port
        self.server_socket = socket.socket()
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        self.print_screen = print_screen
        self.save_file = save_file

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
        received_data = client_socket.recv(BUFFER_SIZE)

        # Split the string using \n as delimenter
        msg_parts = received_data.split(b"\n")

        # Check if msg is text or dictionary
        data_type = msg_parts[0].decode()

        if data_type == "dictionary":
            print("Data type: Dictionary")

            # Separate remaining parts of the string
            data_format = msg_parts[1].decode()
            data = msg_parts[2]

            # Deserialize dictionary
            dictionary = self.deserialize_dictionary (data, data_format)
            print("Dictionary received")

            # Print
            if self.print_screen:
                print("Received data:", dictionary)

            # Save to a file
            if self.save_file:
                with open("received_dictionary.txt","w", encoding="utf-8") as my_file:
                    my_file.write(str(dictionary))

        elif data_type == "textfile":
            print("Data type: Text file")

            # Separate remaining parts of the string
            data = msg_parts[1].decode()
            encrypted_str = msg_parts[2].decode()
            # Convert "True" or "False" string to boolean
            encrypted = encrypted_str.lower() == "true"
            print("Received data:", data)
            print("Data length:", len(data))
            print("Encrypted:", encrypted)

            # Print
            if self.print_screen:
                print("Received data:", data)

            # Save to a file
            if self.save_file:
                with open("received_text.txt","w", encoding="utf-8") as my_file:
                    my_file.write(data)

            #if encrypted:
            #    # Decrypt data
            #    fernet = Fernet(b"secretpassword")
            #    data = fernet.decrypt(data)

            # Save to a file
            #with open("received_text.txt","wb") as my_file:
            #    my_file.write(data)

    def deserialize_dictionary (self, data, data_format):
        """Deserialize the data received by the client depending on its format"""
        if data_format == "binary":
            return pickle.loads(data)

        elif data_format == "json":
            return json.loads(data)

        elif data_format == "xml":
            # Helper functions to convert XML to dictionary
            def xml_to_dict(data):
                root = ET.fromstring(data)
                return _xml_to_dict_helper(root)

            def _xml_to_dict_helper(element):
                result = {}
                for child in element:
                    if len(child):
                        result[child.tag] = _xml_to_dict_helper(child)
                    else:
                        result[child.tag] = child.text
                return result

            # Deserialize XML to dictionary
            data_dict = xml_to_dict(data)
            return data_dict


if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 12345
    BUFFER_SIZE = 1024

    server = Server(HOST, PORT, print_screen=True, save_file=True)
    server.connect()
