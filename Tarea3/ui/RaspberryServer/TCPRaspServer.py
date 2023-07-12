from .funs import *

def connect(worker,conf):

    # "192.168.5.177"  # Standard loopback interface address (localhost)
    #HOST = "192.168.4.1"
    #HOST = "192.168.1.154"
    HOST = conf["HostIp"]
    #PORT = 5000  # Port to listen on (non-privileged ports are > 1023)
    PORT = int(conf["TCPPort"])
    connection(HOST, PORT,worker,conf)
