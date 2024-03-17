# CSCK541 GroupB Server-Client Project

## Introduction

Creared for the task is a server written in Python that receives data from a client class, which is then processed with the option to print to screen and save to file. The Client can send a dictionary or text file, with the dictionary they can be serialised in binary, JSON or XML when sent and the text file can be encrypted. There is a seperate class which interacts with the user wherevby the user can specify which of the options above they would like selected when the file is sent.

## Repository

The repository can be found at https://github.com/Sahib333/CSCK541-GroupB/ 

## Running the process

- Start by running the serverclass.py to initialise the server
- Once the server is running run clientapp.py
- Follow the prompts provided by the application to send the required information to the server

## Components
### Server Class

The Server class opens up the connection to receive data from the client. Dependant on the received data it will undergo processing and optionally display the data and/or save the data. If it is a dictionary it will derialise depending on if it has been serialised in binary, JSON or XML. If the data is a string it will detect if there is encryption and decrypt so that it can display and/or save the data. 

### Client Class

The client class connects to the server and transmits data dependant on the file supplied. You can send a dictionary or text file to the server. If yoou send a dictionary you can serialise it in binary. JSON, or XML and if you send a text file you can encrypt it.


### Client App
The client app is the interface between the system and the user whereby they can specify the the file they would like to send alongside the relevant parameters. If the user selects a dictionary they can serialise in binary, JSON or XML and if its a text file there is the option to encrypt the data.

## Configuring
Modify the host and port settings in both the Server and Client class to match the server configuration. Firthermore for the server configuration alter the initialisation dependant on if the information should be displayed or the data should be saved.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.

## License
MIT License

Copyright (c) 2024 Sahib333

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

