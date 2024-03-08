"""Client class"""

import socket
import pickle
import json
import xml.etree.ElementTree as ET
from cryptography.fernet import Fernet

class Client:
    """Client class"""
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket()
        self.client_socket.connect((host, port))
        self.fernet_key = Fernet.generate_key()
        self.fernet = Fernet(self.fernet_key)

    def send_dictionary (self, data_format, data):
        """Send dictionary"""
        serialized_data = self.serialize_dictionary(data_format, data)
        print(serialized_data)
        print(type(serialized_data))
        msg = f"dictionary,{data_format},{serialized_data}"
        #Encoding the string before sending it
        self.client_socket.send(msg.encode())

    def send_text (self, data, encrypt):
        """Send text"""
        #if encrypt:
        #    data = self.encrypt_data(data)
        if encrypt:
            encrypted_data = self.fernet.encrypt(data.encode())
            msg = f"text,{encrypted_data.decode()},{self.fernet_key.decode()}"
        else:
            msg = f"text,{data},{str(encrypt)}"
        self.client_socket.send(msg.encode())

    def upload_text_file(self, file_path, encrypt=False):
        """Upload a text file"""
        with open(file_path, 'rb') as file:
            file_data = file.read()
            if encrypt:
                encrypted_data = self.fernet.encrypt(file_data)
                msg = f"file,{file_path},{encrypted_data.decode()},{self.fernet_key.decode()}"
            else:
                msg = f"file,{file_path},{file_data.decode()},False"
            self.client_socket.send(msg.encode())


    #def encrypt_data(self, data):
    #    """Encrypt data"""
    #    key = Fernet.generate_key()
    #    fernet = Fernet(key)
    #    return fernet.encrypt(data)

    def serialize_dictionary (self, data_format, dictionary):
        """Serialize the data received by the client depending on its format"""
        if data_format == "binary":
            return pickle.dumps(dictionary)
        elif data_format == "json":
            return json.dumps(dictionary)
        elif data_format == "xml":
            root = ET.Element("root")
            for key, value in dictionary.items():
                ET.SubElement(root,key).text = str(value)
            return ET.tostring(root)


if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 12345

    client = Client(HOST, PORT)
    dictionary_data = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}
    client.send_dictionary("json", dictionary_data)

    #Text File
    TEXT = "hello world!"
    client.send_text(TEXT, encrypt=True)

    file_path = "example.txt"
    client.upload_text_file(file_path, encrypt=True)