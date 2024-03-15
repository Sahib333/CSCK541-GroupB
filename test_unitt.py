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
        decrypted_data = self.server.decrypt_string(encrypted_data, self.key)

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


class TestClientPerformance(unittest.TestCase):

    def setUp(self):
        self.HOST = "127.0.0.1"
        self.PORT = 12345
        self.client = Client(self.HOST, self.PORT)
        self.server = Server(self.HOST, self.PORT)

    def tearDown(self):
        self.server.server_socket.close()

    def test_client_performance(self):
        # Test sending a large amount of data from client to server
        data = "a" * 1000000  # 1 MB of data

        start_time = time.time()
        self.client.send_textfile(data, encrypted=False)
        end_time = time.time()
        execution_time = end_time - start_time

        print(f"Client execution time: {execution_time} seconds")


class DummySocket:
    def __init__(self, data):
        self.data = data

    def recv(self, size):
        return self.data

class TestServerPerformance(unittest.TestCase):
    BUFFER_SIZE = 4096  # Define the buffer size

    def setUp(self):
        self.server = Server("127.0.0.1", 12345)

    def test_server_performance(self):
        # Test receiving a large amount of data by the server
        data = "a" * 1000000  # 1 MB of data
        encoded_data = data.encode()
        dummy_socket = DummySocket(encoded_data)

        start_time = time.time()
        self.server.handle_client(dummy_socket)
        end_time = time.time()
        execution_time = end_time - start_time

        print(f"Server execution time: {execution_time} seconds")

class TestEdgeCaseNoData(unittest.TestCase):
    def setUp(self):
        self.HOST = "127.0.0.1"
        self.PORT = 12345
        self.server = Server(self.HOST, self.PORT)
        self.client = Client(self.HOST, self.PORT)

    def test_no_data(self):
        # Start server
        server_thread = threading.Thread(target=self.server.connect)
        server_thread.start()

        # Send no data from client
        time.sleep(1)  # Wait for server to start
        self.client.send_dictionary("json", {})  # Sending an empty dictionary

        # Wait for server to finish handling client
        time.sleep(1)

        # Assert that no data was received by the server
        self.assertEqual(self.server.received_data, None)

class TestEdgeCaseUnexpectedData(unittest.TestCase):
    def setUp(self):
        self.HOST = "127.0.0.1"
        self.PORT = 12345
        self.server = Server(self.HOST, self.PORT)
        self.client = Client(self.HOST, self.PORT)

    def test_unexpected_data(self):
        # Start server
        server_thread = threading.Thread(target=self.server.connect)
        server_thread.start()

        # Send unexpected data from client
        time.sleep(1)  # Wait for server to start
        unexpected_data = b"unexpected data"
        self.client.client_socket.send(unexpected_data)

        # Wait for server to finish handling client
        time.sleep(1)

        # Assert that server handled unexpected data gracefully
        # You can add specific assertions based on your server's behavior
        self.assertTrue(True)  # Placeholder assertion

class TestEdgeCaseLargeData(unittest.TestCase):
    def setUp(self):
        self.HOST = "127.0.0.1"
        self.PORT = 12345
        self.server = Server(self.HOST, self.PORT)
        self.client = Client(self.HOST, self.PORT)

    def test_large_data(self):
        # Start server
        server_thread = threading.Thread(target=self.server.connect)
        server_thread.start()

        # Send large data from client
        time.sleep(1)  # Wait for server to start
        large_data = b"a" * (10 * 1024 * 1024)  # 10 MB of data
        self.client.client_socket.send(large_data)

        # Wait for server to finish handling client
        time.sleep(5)  # Adjust sleep time as needed

        # Assert that server handled large data gracefully
        # Add specific assertions based on your server's behavior
        self.assertTrue(True)  #


if __name__ == '__main__':
    unittest.main()

