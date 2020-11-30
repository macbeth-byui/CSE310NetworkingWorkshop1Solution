"""
CSE310 Networking Workshop - Example 1 - Solution

This example will explore a client/server architecture using
Python sockets.  
"""

import socketserver
import socket
import pandas  # pip install pandas

# Load up the NBA data so we can respond to client requests

nba_data = pandas.read_csv("basketball_players.csv", low_memory=False)

class NBA_Stat_Server(socketserver.BaseRequestHandler):
    """
    This class provides a handler function for our server.
    """

    def handle(self):
        # Obtain the source ip address and port form the self.client_address.
        # The self.client_address is inherited form socketserver.BaseRequestHandler
        source_ip_address = self.client_address[0]
        source_port = self.client_address[1]

        # Convert the bytes to a string using UTF-8 encoding
        source_msg = str(self.request[0], "UTF-8") 
        print("[{}:{}] => {}".format(source_ip_address, source_port, source_msg))

        # Process the request and provide a value of -1 if there is any
        # error (e.g. invalid stat column provided by client)
        try:
            result = str(nba_data[source_msg].max())
        except:
            result = str(-1)

        # To send a response, we will need the server socket which is available
        # in self.request[1].  We also need the client address which is available
        # in self.client_address
        sock = self.request[1]
        sock.sendto(bytes(result, "UTF-8"), self.client_address)

        print("[{}:{}] <= {}".format(source_ip_address, source_port, result))
        

# Get the ip address of the server
host_name = socket.gethostname()
ip_address = socket.gethostbyname(host_name)
server_address = (ip_address, 5000)
print("Starting Server: [{}:{}]".format(server_address[0], server_address[1]))

# Create the UDP server and run forever
with socketserver.UDPServer(server_address, NBA_Stat_Server) as server:
    server.serve_forever()

