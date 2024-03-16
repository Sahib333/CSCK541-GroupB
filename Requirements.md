# Requirements

## Server Class
- Create a connection
  - Initialise a connection on a given Host and Port
  - Listen to incoming connections from the client

 - Recieve Data in two types
   - Dictionary in 3 formats (JSON, binary, XML)
   - Text files that may be encrypted
  
  - Process Data
    - If the data is a dictionary desrialise from the given format
    - If the text file is encrypted decrypt

  - Display Data
    - If specified display the data on the screen
   
  - Save Data
    - If specified save the data
   
  ## Client Class
  - Connect to server
    - Connect to the specified Host and Port

  - Send Data
    - Dependant on the information provided by the user through clientapp process the data
    - If the file is a dictionary serialise in the specified format (binary, JSON, XML)
    - If the file is a text file then encrypt if the option is selected
   
  ## ClientApp
  - User Input
    - Interact with the client so they can specify their requirements
    - Use the client class to appropriately select the relevant requirements
      - If they select dictionary then select serialisation
      - If they select text, specify filepath and if encryption is required

## Dependencies
1. Python: Version 3.6 or higher
2. Libraries
   - socket: pip install sockets
   - os: Part of standard library
   - pickle: Part of standard library
   - json: pip install jsonlib
   - xml.etree.ElementTree: pip install elementpath
   - cryptography.fernet: pip install cryptography
   - unittest: pip install unittest
  
