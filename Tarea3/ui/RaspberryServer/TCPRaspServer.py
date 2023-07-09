from .funs import *

def connect():

    # "192.168.5.177"  # Standard loopback interface address (localhost)
    HOST = "192.168.4.1"
    #HOST = "192.168.1.154"
    PORT = 5000  # Port to listen on (non-privileged ports are > 1023)

    connection(HOST, PORT)
