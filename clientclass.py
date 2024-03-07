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

    def send_data (self, data_type, data, data_format, encrypt):

        self.client_socket.send(data_type.encode())

        if data_type == "dictionary":
            if format:
                self.client_socket.send(",".join([data_format,str(encrypt)]).encode())
            else:
                raise ValueError

            serialized_data = self.serialize_dictionary (data, data_format)
            self.client_socket.send(serialized_data)

        elif data_type == "text":
            self.client_socket.send(str(encrypt).encode())

            if encrypt:
                encrypted_data = self.encrypt_data(data)

            self.client_socket.send(encrypted_data)

    def serialize_dictionary (self, dictionary, data_format):
        if data_format == "binary":
            return pickle.dumps(dictionary)
        elif data_format == "json":
            return json.dumps(dictionary).encode()
        elif data_format == "xml":
            root = ET.Element("root")
            for key, value in dictionary.items():
                ET.SubElement(root,key).text = str(value)
            return ET.tostring(root)

    def encrypt_data(self, data):
        fernet = Fernet(b"secretpassword")
        return fernet.encrypt(data)

if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 12345

    client = Client(HOST, PORT)
    dictionary_data = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}
    client.send_data ("dictionary", dictionary_data, "json", True)
