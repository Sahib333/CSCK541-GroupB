"""Client class"""

import socket
import pickle
import json
import xml.etree.ElementTree as ET
from cryptography.fernet import Fernet

class Client:
    """Client class"""
    def __init__(self, host, port):
        try:
            self.host = host
            self.port = port
            self.client_socket = socket.socket()
            self.client_socket.connect((host, port))
        except ConnectionRefusedError:
            print("The connection was refused. The server may be offline.")
        except socket.timeout:
            print("Connection timed out")
        except OSError as oserr:
            print("OS Error occurred:")
            print(oserr)

    def send_dictionary (self, data_format, data):
        """Class method to send dictionary"""
        # Serialise dictionary
        try:
            serialized_data = self.serialize_dictionary(data_format, data)
            if data_format == "binary":
                # if the data format is binary we don't need to encode it
                msg = f"dictionary#|{data_format}#|"
                enconded_msg = msg.encode() + serialized_data
            else:
                # Create string with serialized dictionary and data format
                msg = f"dictionary#|{data_format}#|{serialized_data}"
                # Encode the string before sending it
                enconded_msg = msg.encode()
            self.client_socket.send(enconded_msg)

        except ConnectionError as ceerr:
            print(f"An error occured when sending the dictionary: {ceerr}")

        finally:
            # Close the connection
            self.client_socket.close()
            print("Connection closed")

    def send_textfile (self, file_path, encrypted):
        """Send text file"""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = file.read()
            #  Encrypt If needed
            if encrypted:
                key = Fernet.generate_key()
                data = self.encrypt_data(data,key)
                msg = f"textfile#|{data}#|{encrypted}#|{key}"
            else:
                msg = f"textfile#|{data}#|{encrypted}"

            self.client_socket.send(msg.encode())

        except FileNotFoundError:
            print("The file does not exist. Please check the filepath is correct.")
        except TypeError:
            print("The file type is not a text file")
        except Exception as e:
            print(f"There was an error when sending the text file: {e}")

        finally:
            # Close the connection
            self.client_socket.close()
            print("Connection closed")

    def encrypt_data(self, data, key):
        """Encrypt data"""
        try:
            fernet = Fernet(key)
            return fernet.encrypt(data.encode('utf-8'))
        except Fernet.InvalidToken as ferr:
            print("Invalid token for encryption:")
            print(ferr)

    def serialize_dictionary (self, data_format, dictionary):
        """Serialize the dictionary before sending it depending on its format"""
        try:
            if data_format == "binary":
                return pickle.dumps(dictionary)
            if data_format == "json":
                return json.dumps(dictionary)
            if data_format == "xml":
                # Helper function to convert dictionary to XML
                def dict_to_xml(tag, my_dict):
                    elem = ET.Element(tag)
                    for key, value in my_dict.items():
                        child = ET.Element(key)
                        child.text = str(value)
                        elem.append(child)
                    return elem

                xml_data = dict_to_xml("data", dictionary)
                xml_str = ET.tostring(xml_data, encoding="unicode")
                return xml_str

        except pickle.PickleError as perr:
            print("Binary serialization error occurred:")
            print(perr)
        except json.JSONDecodeError as jsonerr:
            print("JSON serialization error occurred:")
            print(jsonerr)
        except ET.ParseError as xmlerr:
            print("XML serialization error occurred:")
            print(xmlerr)
        except ValueError as verr:
            print("Value error occurred:")
            print(verr)
        except TypeError as typerr:
            print("File type error occurred:")
            print(typerr)
