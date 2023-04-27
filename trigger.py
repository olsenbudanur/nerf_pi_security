import socket

HOST = '10.53.134.70'  # The IP address of the machine running the listening program
PORT = 12345  # The same port number that the listening program is listening on

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to the server on the specified port
s.connect((HOST, PORT))

# send some data to the server
s.sendall(b'Intruder!')

# receive some data from the server
data = s.recv(1024)

# print the data that was received
print('Received', repr(data))

# close the connection
s.close()
