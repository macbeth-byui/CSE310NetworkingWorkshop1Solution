"""
CSE310 Networking Workshop - Example 1 - Solution

This example will explore a client/server architecture using
Python sockets.  
"""

import socket

ip_address = input("Enter NBA Server IP Address: ")
request = input("Which stat do you want: ")

# Addresses are a two part tuple including ip/hostname and port
server_address = (ip_address, 5000)

# Everything within the 'with' block will run
# If an error occurs, the socket will automatically close
# The socket uses the Internet Address Family and Datagram (UDP) Protocol
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:

    # Sockets transmit bytes instead of string.  We will use the common UTF-8 encoding.
    # Transmit the stat name
    sock.sendto(bytes(request, "UTF-8"), server_address)

    # Wait for a response.  UDP packets must specify a buffer size.   We have 
    # to convert the bytes received back to a string using the same UTF-8 encoding.
    result = str(sock.recv(1024), "UTF-8")

    # Display the response
    print("Result: "+result)
