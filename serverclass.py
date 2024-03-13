"""A server class"""
import os
import socket
import pickle
import json
import xml.etree.ElementTree as ET
from cryptography.fernet import Fernet

class Server:
    """ Server class"""
    def __init__(self, host, port, print_screen=False, save_file=False):
        self.host = host
        self.port = port
        self.print_screen = print_screen
        self.save_file = save_file
        self.server_socket = socket.socket()
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)

    def connect(self):
        """Connect to the client"""
        print(f"Server listening on {self.host}:{self.port}")
        try:
            while True:
                client_socket, addr = self.server_socket.accept()
                print(f"Connection from {addr}")
                try:
                    self.handle_client(client_socket)
                except Exception as e:
                    print(f"An error occured: {e}")
                finally:
                    client_socket.close()
        except KeyboardInterrupt:
            print("Connection terminated by user.")
        except Exception as e:
            print(f"An error occured: {e}")

    def handle_client(self, client_socket):
        """Receive data type (dictionary or text file)"""
        # Receiving the data
        received_data = client_socket.recv(BUFFER_SIZE)
        # Split the string using #| as delimiter
        msg_parts = received_data.split(b"#|")
        # Check if msg is text or dictionary
        data_type = msg_parts[0].decode()
        print(data_type)

        try:
            if data_type == "dictionary":
                print("Data type: Dictionary")
                # Separate remaining parts of the string
                data_format = msg_parts[1].decode()
                data = msg_parts[2]
                # Deserialize dictionary
                dictionary = self.deserialize_dictionary (data, data_format)
                print("Dictionary received")

                # Print to screen
                try:
                    if self.print_screen:
                        print("Received data:")
                        for key, value in dictionary.items():
                            print(f"{key}: {value}")
                except Exception as e:
                    print(f"An error occured when printing dictionary: {e}")
                # Save to a file
                try:
                    if self.save_file:
                        with open("received_dictionary.txt","w", encoding="utf-8") as my_file:
                            my_file.write(str(dictionary))
                        print("Dictionary saved to: " + os.path.abspath("received_dictionary.txt"))
                except Exception as e:
                    print(f"An error occured when saving the dictionary: {e}")

            elif data_type == "textfile":
                print("Data type: Text file")
                encrypted_str = msg_parts[2].decode()

                # Check encryption and separate remaining parts of the string
                try:
                    if encrypted_str=="True":
                        key = eval(msg_parts[3].decode('utf-8'))
                        fernet = Fernet(key)
                        data= fernet.decrypt(eval(msg_parts[1])).decode()
                    else:
                        data = msg_parts[1].decode()
                except Exception as e:
                    print(f"An error occured when decoding the text: {e}")

                # Print to screen
                try:
                    if self.print_screen:
                        print("Received data:", data)
                except Exception as e:
                    print(f"An error occured when printing text to screen: {e}")

                # Save to a file
                try:
                    if self.save_file:
                        with open("received_text.txt","w", encoding="utf-8") as my_file:
                            my_file.write(data)
                        print("Text file saved to: " + os.path.abspath("received_text.txt"))
                except Exception as e:
                    print(f"An error occured when saving the text file :{e}")

        except Exception as e:
            print(f"An error occured when receiving the data: {e}")

    def deserialize_dictionary (self, data, data_format):
        """Deserialize the data received by the client depending on its format"""
        try:
            if data_format == "binary":
                return pickle.loads(data)

            elif data_format == "json":
                return json.loads(data)

            elif data_format == "xml":
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

        except Exception as e:
            print(f"An error occured when deserializing the dictionary: {e}")


if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 12345
    BUFFER_SIZE = 4096

    server = Server(HOST, PORT, True, True)
    server.connect()
