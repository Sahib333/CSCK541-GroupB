"""A server class"""

import os
import socket
import pickle
import json
import xml.etree.ElementTree as ET
from cryptography.fernet import Fernet
# from ast import literal_eval

class Server:
    """ Server class"""
    def __init__(self, host, port, print_screen=False, save_file=False):
        self.host = host
        self.port = port
        self.print_screen = print_screen
        self.save_file = save_file
        self.server_socket = socket.socket()
        try:
            self.server_socket.bind((host, port))
            self.server_socket.listen(5)
        except PermissionError:
            print("Permission error: Unable to bind to host and port")
        except OSError as oserr:
            print(f"OS error: {oserr}")
        except ValueError as veerr:
            print(f"Value error: {veerr}")

    def connect(self):
        """Connect to the client"""
        print(f"Server listening on {self.host}:{self.port}")
        try:
            while True:
                client_socket, addr = self.server_socket.accept()
                print(f"Connection from {addr}")
                try:
                    self.handle_client(client_socket)
                except ConnectionError as ceerr:
                    print(f"Error accepting the connection: {ceerr}")
                finally:
                    client_socket.close()
        except KeyboardInterrupt:
            print("Connection terminated by user.")
        except socket.error as sockerr:
            print("A socket error occurred:")
            print(sockerr)


    def handle_client(self, client_socket):
        """Receive data type (dictionary or text file)"""
        # Receiving the data
        received_data = client_socket.recv(BUFFER_SIZE)
        # Split the string using #| as delimiter
        msg_parts = received_data.split(b"#|")
        # Check if msg is text or dictionary
        data_type = msg_parts[0].decode()

        try:
            if data_type == "dictionary":
                print("Data type: Dictionary")
                # Separate remaining parts of the string
                data_format = msg_parts[1].decode()
                data = msg_parts[2]
                # Deserialize dictionary
                dictionary = self.deserialize_dictionary(data, data_format)
                print("Dictionary received")

                # Print to screen
                if self.print_screen:
                    print("Received data:")
                    for key, value in dictionary.items():
                        print(f"{key}: {value}")

                # Save the dictionary to a file
                if self.save_file:
                    with open("received_dictionary.txt", "w", encoding="utf-8") as my_file:
                        my_file.write(str(dictionary))
                    print("Dictionary saved to: " + os.path.abspath("received_dictionary.txt"))


            elif data_type == "textfile":
                print("Data type: Text file")
                encrypted_str = msg_parts[2].decode()

                # Check encryption and separate remaining parts of the string
                if encrypted_str == "True":  
                    data = self.decrypt_string(msg_parts)
                else:
                    data = msg_parts[1].decode()

                # Print to screen
                if self.print_screen:
                    print("Received data:", data)


                # Save to a file
                if self.save_file:
                    with open("received_text.txt", "w", encoding="utf-8") as my_file:
                        my_file.write(data)
                    print("Text file saved to: " + os.path.abspath("received_text.txt"))

        except OSError as oserr:
            print("OS Error occurred:")
            print(oserr)
        except pickle.UnpicklingError as unperr:
            print("Binary deserialization error occurred:")
            print(unperr)
        except json.JSONDecodeError as jsonerr:
            print("JSON deserialisation error occurred:")
            print(jsonerr)
        except ET.ParseError as xmlerr:
            print("XML deserialization error occurred:")
            print(xmlerr)

    def decrypt_string(self, data):
        # Decrypt the text file
        try:
            key=eval(data[3].decode('utf-8'))
            fernet = Fernet(key)
            data = fernet.decrypt(eval(data[1])).decode()
            return data

        except fernet.InvalidToken as ferrerr:
            print("Error occurred with encryption key:")
            print(ferrerr)
        except TypeError as tyerr:
            print("Error occurred due to token:")
            print(tyerr)

    def deserialize_dictionary(self, data, data_format):
        """Deserialize the data received by the client depending on its format"""

        if data_format == "binary":
            return pickle.loads(data)

        if data_format == "json":
            return json.loads(data)

        if data_format == "xml":
            # Helper functions to convert XML to dictionary
            def xml_to_dict(data):
                root = ET.fromstring(data)
                return xml_to_dict_helper(root)

            def xml_to_dict_helper(element):
                result = {}
                for child in element:
                    if len(child):
                        result[child.tag] = xml_to_dict_helper(child)
                    else:
                        result[child.tag] = child.text
                return result

            # Deserialize XML to dictionary
            data_dict = xml_to_dict(data)
            return data_dict

        else:
            raise ValueError("Data format is invalid please select binary, json or xml")


if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 12345
    BUFFER_SIZE = 4096

    server = Server(HOST, PORT, True, True)
    server.connect()
