import socket
from funs import *

# "192.168.5.177"  # Standard loopback interface address (localhost)
#HOST = "192.168.4.1"
HOST = "192.168.1.154"
PORT = 5001  # Port to listen on (non-privileged ports are > 1023)

s = socket.socket(socket.AF_INET, #internet
                  socket.SOCK_STREAM) #TCP
s.bind((HOST, PORT))
s.listen(5)


print(f"Listening on {HOST}:{PORT}")


protocol, transport_layer = select_options()

req_bytes = bytearray()
req_bytes.append(protocol)
req_bytes.append(transport_layer)

connection(s, req_bytes)
