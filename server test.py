
import unittest
from serverclass import Server


class TestServer(unittest.TestCase):
    def setUp(self):
        self.HOST = "127.0.0.1"
        self.PORT = 12345
        self.encryption_key = b'Co-BF0ODIcKopN9XnfMXzIaGyb5eyEUVH13NdaEDKS4='
        self.server = Server(self.HOST, self.PORT)

    def tearDown(self):  # Close the socket after each test
        self.server.sock.close()

    def test_decrypt_data_valid(self):
        # Test successful decryption
        encrypted_data = self.server.cipher_suite.encrypt(b'Test data')
        decrypted_data = self.server.decrypt_string(encrypted_data)
        self.assertEqual(decrypted_data, b'Test data')

    def test_decrypt_data_invalid(self):
        # Test invalid decryption (should return None)
        encrypted_data = b'Invalid encrypted data'
        decrypted_data = self.server.decrypt_string(encrypted_data)
        self.assertIsNone(decrypted_data)

    def test_deserialize_data_json(self):
        # Test JSON deserialization
        json_data = '{"key": "value"}'
        deserialized_data = self.server.deserialize_dictionary(json_data, 'json')
        self.assertEqual(deserialized_data, {'key': 'value'})

    def test_deserialize_data_binary(self):
        # Test binary deserialization
        binary_data = b'\x80\x03X\x05\x00\x00\x00helloq\x00.'
        deserialized_data = self.server.deserialize_dictionary(binary_data, 'binary')
        self.assertEqual(deserialized_data, 'hello')

    def test_deserialize_data_xml(self):
        # Test XML deserialization
        xml_data = '<data><content>Hello</content></data>'
        deserialized_data = self.server.deserialize_dictionary(xml_data, 'xml')
        self.assertEqual(deserialized_data, 'Hello')


if __name__ == '__main__':
    unittest.main()
    
