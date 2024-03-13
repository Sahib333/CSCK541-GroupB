"""A class that allows the user to use the client class and select what they want to send"""

from clientclass import Client

class ClientApp:
    def __init__(self):
        self.client = Client("127.0.0.1", 12345)

    def execute(self):
        """Allow the user to choose the method they would like to send the data"""
        while True:
            print("File Type:")
            print("1. Send Text File")
            print("2. Send Dictionary")
            print("3. Exit")

            file_type = input("Choose which file type you would like to send (1/2/3): ")

            # Send a Text File
            if file_type == "1":
                try:
                    file_path = input("Please specify the location of the text file: ")
                    encrypted_input = input("Would you like to encrypt the file? (y/n): ")
                    encrypted = encrypted_input.lower() == "y"
                    self.client.send_textfile(file_path, encrypted)
                    break
                except FileNotFoundError:
                    print("Incorrect filepath.")
                except TypeError:
                    print("File is not in txt format")

            # Send a dictionary
            elif file_type == "2":
                try:
                    data_format = input("Choose a serialization format (binary/JSON/XML): ").lower()
                    if data_format not in ["binary","json","xml"]:
                        raise ValueError("Invalid serialization format. Choose from binary, JSON, or XML.")

                    dictionary_data = {}
                    print("Enter key-value pairs to create the dictionary.")
                    print("To finish leave the key empty and press Enter.")
                    while True:
                        key = input("Enter key: ")
                        if not key:
                            break
                        value = input(f"Enter value for {key}: ")
                        dictionary_data[key] = value

                    self.client.send_dictionary(data_format, dictionary_data)
                    break
                except Exception as e:
                    print(f"An error occurred: {e}")

            elif file_type == "3":
                # Exit
                print("Exiting the application")
                break

            else:
                print("Please select a valid option")

if __name__ == "__main__":
    application = ClientApp()
    application.execute()
