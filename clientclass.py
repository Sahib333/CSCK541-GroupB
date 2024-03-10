"""Client class"""

import socket
import pickle
import json
import xml.etree.ElementTree as ET
from cryptography.fernet import Fernet

class Client:
    """Client class"""
    def __init__(self, host, port, print_screen, save_file):
        self.host = host
        self.port = port
        self.client_socket = socket.socket()
        self.client_socket.connect((host, port))
        self.print_screen = print_screen
        self.save_file = save_file

    def send_dictionary (self, data_format, data):
        """Class method to send dictionary"""
        # Serialise dictionary
        serialized_data = self.serialize_dictionary(data_format, data)

        if data_format == "binary":
            # if the data format is binary we don't need to encode it
            msg = f"dictionary\n{data_format}\n"
            enconded_msg = msg.encode() + serialized_data
        else:
            # Create string with serialized dictionary and data format
            msg = f"dictionary\n{data_format}\n{serialized_data}"
            # Encode the string before sending it
            enconded_msg = msg.encode()

        # Encode the string before sending it
        self.client_socket.send(enconded_msg)

        # Save dictionary to a file
        if self.save_file:
            dict_str = ""
            for key, value in data.items():
                dict_str += f"{key}: {value}\n"

            with open("received_dictionary.txt", "w", encoding="utf-8") as my_file:
                my_file.write(dict_str)

    def send_textfile (self, file_path, encrypted):
        """Send text file"""
        #if encrypted:
        #    data = self.encrypt_data(data)

        with open(file_path, "r") as file:
            content = file.read()

        msg = f"textfile\n{content}\n{encrypted}"
        print(msg)
        self.client_socket.send(msg.encode())

    #def encrypt_data(self, data):
    #    """Encrypt data"""
    #    key = Fernet.generate_key()
    #    fernet = Fernet(key)
    #    return fernet.encrypt(data)

    def serialize_dictionary (self, data_format, dictionary):
        """Serialize the dictionary before sending it depending on its format"""
        if data_format == "binary":
            return pickle.dumps(dictionary)
        elif data_format == "json":
            return json.dumps(dictionary)
        elif data_format == "xml":
            # Helper function to convert dictionary to XML
            def dict_to_xml(tag, d):
                elem = ET.Element(tag)
                for key, value in d.items():
                    child = ET.Element(key)
                    child.text = str(value)
                    elem.append(child)
                return elem

            xml_data = dict_to_xml("data", dictionary)
            xml_str = ET.tostring(xml_data, encoding="unicode")
            return xml_str


if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 12345

    client = Client(HOST, PORT, print_screen=True, save_file=True)
    file_path = "C:/Users/82102/PycharmProjects/CSCK541-GroupB/example.txt"
    client.send_textfile (file_path, False)

#    dictionary_data = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}
#    client.send_dictionary("xml", dictionary_data)