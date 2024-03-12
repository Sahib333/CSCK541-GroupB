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

        except Exception as e:
            print(f"An error occurred when initialising the connection: {e}")


    def send_dictionary(self, data_format, data):
        """Class method to send dictionary"""
        # Serialise dictionary
        serialized_data = self.serialize_dictionary(data_format, data)
        try:
            if data_format == "binary":
                # if the data format is binary we don't need to encode it
                msg = f"dictionary\n\n\n{data_format}\n\n\n"
                encoded_msg = msg.encode() + serialized_data

            else:
                # Create string with serialized dictionary and data format
                msg = f"dictionary\n\n\n{data_format}\n\n\n{serialized_data}"
                # Encode the string before sending it
                encoded_msg = msg.encode()
            self.client_socket.send(encoded_msg)

        except Exception as e:
            print(f"An error occurred when sending the dictionary: {e}")

        finally:
            # Close the connection
            self.client_socket.close()
            print("Connection closed")

            
    def send_textfile(self, file_path, encrypted):
        """Send text file"""
        try:
            with open(file_path, "r") as file:
                data = file.read()
            #  Encrypt If needed
            if encrypted is True:
                key = Fernet.generate_key()
                data = self.encrypt_data(data, key)
                msg = f"textfile\n\n\n{data}\n\n\n{encrypted}\n\n\n{key}"
            else:
                msg = f"textfile\n\n\n{data}\n\n\n{encrypted}"

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
        except Exception as e:
            print(f"An error occurred when encrypting the data: {e}")


    def serialize_dictionary(self, data_format, dictionary):
        """Serialize the dictionary before sending it depending on its format"""
        try:
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
            else:
                raise ValueError(f"{data_format} is invalid please choose between binary, json or xml.")
        except Exception as e:
            print(f"An error occurred when serialising the dictionary: {e}")

    def user_prompt(self):
        """Allow the user to choose the method they would like to send the data"""
        while True:
            print("\nFile Type:")
            print("\n1. Send Text")
            print("\n2. Send Dictionary")
            print("\n3. Exit")

            prompt1 = input("Choose which file type you would like to send (1/2/3): ")

            if prompt1 == "1":
                # Send a Text File
                file_path = input("Please specify the location of the text file: ")
                encrypted = input("Would you like to encrypt the file? (y/n): ").lower() == "y"
                self.send_textfile(file_path, encrypted)
                break

            if prompt1 == "2":
                # Send a dictionary
                data_format = input("Which serialization format would you like to use? (binary/json/xml): ").lower()
                file_path = input("Please specify the location of the file: ")
                file_format = input("What format is the dictionary saved? (binary/json/xml): ").lower()

                try:
                    if file_format == "binary":
                        with open(file_path, "rb") as data:
                            dictionary_data = pickle.load(data)

                    if file_format == "json":
                        with open(file_path, "rb") as data:
                            dictionary_data = json.load(data)

                    if file_format == "xml":
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
                        with open(file_path, "rb") as data:
                            dictionary_data = xml_to_dict(data)

                    self.send_dictionary(data_format, dictionary_data)
                    break

                except FileNotFoundError:
                    print("/nPlease check the filepath is correct as no such data exists at the specified location.")
                except pickle.UnpicklingError:
                    print("The specified dictionary is not in binary format")
            if prompt1 == "3":
                # Exit
                break
            else:
                print("Please select a valid option")


                xml_data = dict_to_xml("data", dictionary)
                xml_str = ET.tostring(xml_data, encoding="unicode")
                return xml_str
            else:
                raise ValueError(f"{data_format} is invalid please choose between binary, json or xml.")
        except Exception as e:
            print(f"An error ocurred when serialising the dictionary: {e}")

if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 12345
    client = Client(HOST, PORT)
    client.user_prompt()
    # file_path = r"C:\Users\16hee\OneDrive\Documents\Sahib\MSc Data Science and AI\CSCK541\Code\Exercises\Text100\test_dictionary.json"
    # dictionary_data = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}
    # client.send_dictionary("json", dictionary_data)

    # file_path = r"C:\Users\16hee\OneDrive\Documents\Sahib\MSc Data Science and AI\CSCK541\Code\Exercises\Text100\ad.txt"
    # client.send_textfile (file_path, True)

