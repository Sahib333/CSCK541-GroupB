import unittest
import threading
from serverclass import Server
from clientclass import Client

class TestServerClient(unittest.TestCase):

    def setUp(self):
        self.HOST = "127.0.0.1"
        self.PORT = 12345
        self.BUFFER_SIZE = 1024

    def test_validate_pickling_format_valid(self):
        client = Client()  # instance of the Client class
        valid_formats = ["binary", "json", "xml"]
        for format in valid_formats:
            result = client.validate_pickling_format(format)
            self.assertTrue(result, f"Expected '{format}' to be valid, but it is not.")

    def test_validate_pickling_format_invalid(self):
        client = Client()  # instance of the Client class
        invalid_formats = ["text", "yaml", "csv"]
        for format in invalid_formats:
            result = client.validate_pickling_format(format)
            self.assertFalse(result, f"Expected '{format}' to be invalid, but it is not.")

    def test_validate_encrypt_option_valid(self):
        client = Client()  # instance of the Client class
        valid_options = ["yes", "no"]
        for option in valid_options:
            result = client.validate_encrypt_option(option)
            self.assertTrue(result, f"Expected '{option}' to be valid, but it is not.")

    def test_validate_encrypt_option_invalid(self):
        client = Client()  # instance of the Client class
        invalid_options = ["true", "false", "encrypt", "decrypt"]
        for option in invalid_options:
            result = client.validate_encrypt_option(option)
            self.assertFalse(result, f"Expected '{option}' to be invalid, but it is not.")

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
        file_path = "test.txt"
        client.send_textfile(file_path, False)

    def start_server(self):
        server = Server(self.HOST, self.PORT)
        server.connect()

class TestEncryption(unittest.TestCase):

    def setUp(self):
        self.HOST = "127.0.0.1"
        self.PORT = 12345
        self.client = Client(self.HOST, self.PORT)

    def test_encrypt_decrypt(self):
        # test data
        original_data = "Hello!"

        # encrypt data
        encrypted_data = self.client.encrypt_data(original_data)

        # ensure encryption resulted in different data
        self.assertNotEqual(encrypted_data, original_data)

        # decrypt data
        decrypted_data = self.client.decrypt_data(encrypted_data)

        # ensure decrypted data matches the original data
        self.assertEqual(decrypted_data, original_data)

if __name__ == '__main__':
    unittest.main()