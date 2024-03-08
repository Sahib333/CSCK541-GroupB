import unittest
import threading
from serverclass import Server
from clientclass import Client

class TestServerClient(unittest.TestCase):

    def setUp(self):
        self.HOST = "127.0.0.1"
        self.PORT = 12345
        self.BUFFER_SIZE = 1024

    def test_server_client_communication(self):
        # Start the server in a separate thread
        server_thread = threading.Thread(target=self.start_server)
        server_thread.start()

        # Ensure that the server is running
        server_ready = False
        while not server_ready:
            try:
                client = Client(self.HOST, self.PORT)
                server_ready = True
            except ConnectionRefusedError:
                pass

        # Test sending dictionary
        dictionary_data = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}
        client.send_dictionary("json", dictionary_data)

        # Test sending text file
        file_path = "test.txt"
        client.send_textfile(file_path, False)

    def start_server(self):
        server = Server(self.HOST, self.PORT)
        server.connect()

if __name__ == '__main__':
    unittest.main()
