"""Unit Tests"""
import unittest
import threading
import time
import pickle
from serverclass import Server
from clientclass import Client

class TestServerClientCommunication(unittest.TestCase):
    """Class to test server client communication"""
    def setUp(self):
        self.host = "127.0.0.1"
        self.port = 12345
        self.buffer_size = 4096
        self.server = Server(self.host, self.port)
        self.server_thread = threading.Thread(target=self.server.connect)
        self.server_thread.start()

    def tearDown(self):
        self.server.server_socket.close()

    def test_server_client_communication(self):
        """Function to test a simple dictionary to send from client to server"""
        # start the server in a separate thread
        server_thread = threading.Thread(target=self.start_server)
        server_thread.start()
        # ensure that the server is running
        server_ready = False
        while not server_ready:
            try:
                client = Client(self.host, self.port)
                server_ready = True
            except ConnectionRefusedError:
                pass
        # test sending dictionary
        dictionary_data = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}
        client.send_dictionary("json", dictionary_data)
        # test sending text file
        file_path = r"C:\Users\16hee\OneDrive\Documents\Sahib\MSc Data Science and " \
                    r"AI\CSCK541\Code\Exercises\Text100\ad.txt "
        client.send_textfile(file_path, False)

    def start_server(self):
        """Function that connects to server"""
        server = Server(self.host, self.port)
        server.connect()

class TestEncryptionDecryption(unittest.TestCase):
    """Class to test security of information transfer"""
    def setUp(self):
        self.host = "127.0.0.1"
        self.port = 12346
        self.key = b'gQqwOp0z6kRLcV80QQQlhvI3gsaUEpHH8KubS6cMdZ0='
        self.server = Server(self.host, self.port, self.key)
        self.server_thread = threading.Thread(target=self.server.connect)
        self.server_thread.start()
        self.client = Client(self.host, self.port)

    def tearDown(self):
        self.server.server_socket.close()

    def test_encrypt_decrypt(self):
        """Function that tests encryption and decryption"""
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
    """Class to test serialization of Client class"""
    def setUp(self):
        self.host = "127.0.0.1"
        self.port = 12347
        self.server = Server(self.host, self.port)
        self.client = Client(self.host, self.port)
    def tearDown(self):
        self.server.server_socket.close()

    def test_json_serialization(self):
        """Function to test JSON serialization"""
        # test data
        test_dictionary = {'key1': 'value1', 'key2': 2, 'key3': [1, 2, 3]}
        # serialize data to JSON
        serialized_dictionary = self.client.serialize_dictionary('json', test_dictionary)
        # ensure serialized data does not match the original data
        self.assertNotEqual(serialized_dictionary, test_dictionary)

    def test_xml_serialization(self):
        """Function to test XML serialization"""
        # test data
        test_dictionary = {'key1': 'value1', 'key2': 2, 'key3': [1, 2, 3]}
        # serialize data to XML
        serialized_dictionary = self.client.serialize_dictionary('xml', test_dictionary)
        # ensure serialized data does not match the original data
        self.assertNotEqual(serialized_dictionary , test_dictionary)

    def test_binary_serialization(self):
        """Function to test Binary serialization"""
        # test data
        test_dictionary = {'key1': 'value1', 'key2': 2, 'key3': [1, 2, 3]}
        # serialize data to binary
        serialized_dictionary = self.client.serialize_dictionary('binary', test_dictionary)
        # ensure serialized data does not match the original data
        self.assertNotEqual(serialized_dictionary , test_dictionary)

class TestDeserialization(unittest.TestCase):
    """Class to test deserialization of the Server class"""
    def setUp(self):
        self.host = "127.0.0.1"
        self.port = 12347
        self.key = b'gQqwOp0z6kRLcV80QQQlhvI3gsaUEpHH8KubS6cMdZ0='
        self.server = Server(self.host, self.port, self.key)
        self.server_thread = threading.Thread(target=self.server.connect)
        self.server_thread.start()
        self.client = Client(self.host, self.port)
    def tearDown(self):
        self.server.server_socket.close()

    def test_deserialize_data_json(self):
        """Function to test JSON deserialization"""
        # Test JSON deserialization
        json_data = '{"key": "value"}'
        deserialized_data = self.server.deserialize_dictionary(json_data, 'json')
        self.assertEqual(deserialized_data, {'key': 'value'})

    def test_deserialize_data_binary(self):
        """Function to test binary deserialization"""
        # Test binary deserialization
        binary_data = pickle.dumps({"key":  "value"})
        self.assertEqual(
            self.server.deserialize_dictionary(binary_data, 'binary'),
            {'key': 'value'},
            'Binary deserialization is incorrect'
        )
    def test_deserialize_data_xml(self):
        """Function to test XML deserialization"""
        # Test XML deserialization
        xml_data = '<data><key1>value1</key1><key2>value2</key2></data>'
        deserialized_data = self.server.deserialize_dictionary(xml_data, 'xml')
        self.assertEqual(deserialized_data, {'key1': 'value1', 'key2': 'value2'})

class TestClientPerformance(unittest.TestCase):
    """Class to test Client class performance"""
    def setUp(self):
        self.host = "127.0.0.1"
        self.port = 12345
        self.client = Client(self.host, self.port)
        self.server = Server(self.host, self.port)

    def tearDown(self):
        self.server.server_socket.close()

    def test_client_performance(self):
        """Function to test Client performance"""
        # Test sending a large amount of data from client to server
        data = "a" * 1000000  # 1 MB of data
        start_time = time.time()
        self.client.send_textfile(data, encrypted=False)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Client execution time: {execution_time} seconds")

class DummySocket:
    """Class to initialize placeholder socket object"""
    def __init__(self, data):
        self.data = data
    def recv(self, buffer_size):
        """Function to receive data from socket"""
        return self.data

class TestServerPerformance(unittest.TestCase):
    """Class to test Server class performance"""
    buffer_size = 4096  # Define the buffer size
    def setUp(self):
        self.server = Server("127.0.0.1", 12345)

    def tearDown(self):
        self.server.server_socket.close()

    def test_server_performance(self):
        """Function to test Server performance"""
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
    """Class to test the no data edge case"""
    def setUp(self):
        self.host = "127.0.0.1"
        self.port = 12345
        self.server = Server(self.host, self.port)
        self.client = Client(self.host, self.port)

    def tearDown(self):
        self.server.server_socket.close()

    def test_no_data(self):
        """Function to test when no data such as an empty dictionary is sent to the server"""
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
    """Class to test the unexpected data edge case"""
    def setUp(self):
        self.host = "127.0.0.1"
        self.port = 12345
        self.server = Server(self.host, self.port)
        self.client = Client(self.host, self.port)

    def tearDown(self):
        self.server.server_socket.close()

    def test_unexpected_data(self):
        """Function to test when unexpected data is received by the server"""
        # Start server
        server_thread = threading.Thread(target=self.server.connect)
        server_thread.start()
        # Send unexpected data from client
        time.sleep(1)  # Wait for server to start
        unexpected_data = b"unexpected data"
        self.client.client_socket.send(unexpected_data)
        # Wait for server to finish handling client
        time.sleep(1)
        # Assert that server raises a Value Error when unexpected data is received
        with self.assertRaises(ValueError):
            self.server.handle_client(self.client.client_socket)

class TestEdgeCaseLargeData(unittest.TestCase):
    """Class to test large data edge case"""
    def setUp(self):
        self.host = "127.0.0.1"
        self.port = 12345
        self.server = Server(self.host, self.port)
        self.client = Client(self.host, self.port)

    def tearDown(self):
        self.server.server_socket.close()

    def test_large_data(self):
        """Function to test large data sent to the server"""
        # Start server
        server_thread = threading.Thread(target=self.server.connect)
        server_thread.start()
        # Send large data from client
        time.sleep(1)  # Wait for server to start
        large_data = b"a" * (10 * 1024 * 1024)  # 10 MB of data
        self.client.client_socket.send(large_data)
        # Wait for server to finish handling client
        time.sleep(5)  # Adjust sleep time as needed
        # Assert that server did not receive data and rejects connection to client
        self.assertIsNone(self.server.received_data, "File is too large for server")
        self.assertFalse(
            self.server.client_connected,
            "Server should reject connection for large data"
        )


if __name__ == '__main__':
    unittest.main()
