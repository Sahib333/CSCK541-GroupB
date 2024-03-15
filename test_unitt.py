import unittest
import threading
from serverclass import Server
from clientclass import Client
import time
import pickle


class TestServerClientCommunication(unittest.TestCase):

    def setUp(self):
        self.HOST = "127.0.0.1"
        self.PORT = 12345
        self.BUFFER_SIZE = 4096

    def test_server_client_communication(self):
        # start the server in a separate thread
        server_thread = threading.Thread(target=self.start_server)
        server_thread.start()

        # ensure that the server is running
        server_ready = False
        while not server_ready:
            try:
                client = Client(self.HOST, self.PORT)
                server_ready = True
            except ConnectionRefusedError:
                pass

        # test sending dictionary
        dictionary_data = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}
        client.send_dictionary("json", dictionary_data)

        # test sending text file
        file_path = r"C:\Users\16hee\OneDrive\Documents\Sahib\MSc Data Science and AI\CSCK541\Code\Exercises\Text100\ad.txt"
        client.send_textfile(file_path, False)

    def start_server(self):
        server = Server(self.HOST, self.PORT)
        server.connect()


class TestEncryptionDecryption(unittest.TestCase):

    def setUp(self):
        self.HOST = "127.0.0.1"
        self.PORT = 12346
        self.key = b'gQqwOp0z6kRLcV80QQQlhvI3gsaUEpHH8KubS6cMdZ0='
        self.server = Server(self.HOST, self.PORT, self.key)
        self.server_thread = threading.Thread(target=self.server.connect)
        self.server_thread.start()
        self.client = Client(self.HOST, self.PORT)

    def tearDown(self):
        self.server.server_socket.close()

    def test_encrypt_decrypt(self):
        # test data
        original_data = 'utf-8'

        # encrypt data
        encrypted_data = self.client.encrypt_data(original_data, self.key)

        # ensure encryption resulted in different data
        self.assertNotEqual(encrypted_data, original_data)

        # decrypt data using the server's decryption method
        decrypted_data = self.server.decrypt_string(encrypted_data)

        # ensure decrypted data matches the original data
        self.assertEqual(decrypted_data, original_data)


class TestSerialization(unittest.TestCase):

    def setUp(self):
        self.HOST = "127.0.0.1"
        self.PORT = 12347
        self.server = Server(self.HOST, self.PORT)
        self.client = Client(self.HOST, self.PORT)

    def tearDown(self):
        self.server.server_socket.close()

    def test_json_serialization(self):
        # test data
        test_dictionary = {'key1': 'value1', 'key2': 2, 'key3': [1, 2, 3]}

        # serialize data to JSON
        serialized_dictionary = self.client.serialize_dictionary('json', test_dictionary)

        # ensure serialized data does not match the original data
        self.assertNotEqual(serialized_dictionary, test_dictionary)

    def test_xml_serialization(self):
        # test data
        test_dictionary = {'key1': 'value1', 'key2': 2, 'key3': [1, 2, 3]}

        # serialize data to XML
        serialized_dictionary = self.client.serialize_dictionary('xml', test_dictionary)

        # ensure serialized data does not match the original data
        self.assertNotEqual(serialized_dictionary , test_dictionary)

    def test_binary_serialization(self):
        # test data
        test_dictionary = {'key1': 'value1', 'key2': 2, 'key3': [1, 2, 3]}

        # serialize data to binary
        serialized_dictionary = self.client.serialize_dictionary('binary', test_dictionary)

        # ensure serialized data does not match the original data
        self.assertNotEqual(serialized_dictionary , test_dictionary)


class TestDeserialization(unittest.TestCase):
    def setUp(self):
        self.HOST = "127.0.0.1"
        self.PORT = 12347
        self.key = b'gQqwOp0z6kRLcV80QQQlhvI3gsaUEpHH8KubS6cMdZ0='
        self.server = Server(self.HOST, self.PORT, self.key)
        self.server_thread = threading.Thread(target=self.server.connect)
        self.server_thread.start()
        self.client = Client(self.HOST, self.PORT)

    def test_deserialize_data_json(self):
        # Test JSON deserialization
        json_data = '{"key": "value"}'
        deserialized_data = self.server.deserialize_dictionary(json_data, 'json')
        self.assertEqual(deserialized_data, {'key': 'value'})

    def test_deserialize_data_binary(self):
        # Test binary deserialization
        binary_data = pickle.dumps({"key":  "value"})
        self.assertEqual(self.server.deserialize_dictionary(binary_data, 'binary'), {'key': 'value'}, 'Binary deseiralization is incorrect')

    def test_deserialize_data_xml(self):
        # Test XML deserialization
        xml_data = '<data><key1>value1</key1><key2>value2</key2></data>'
        deserialized_data = self.server.deserialize_dictionary(xml_data, 'xml')
        self.assertEqual(deserialized_data, {'key1': 'value1', 'key2': 'value2'})


if __name__ == '__main__':
    unittest.main()

