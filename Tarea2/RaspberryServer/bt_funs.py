import keyboard
import socket
import sys, select
import time
from Desempaquetamiento import saveConfig

def select_options():
    print("Select the protocol (0, 1, 2, 3) or 5 for close")
    protocol = 0
    while True:
        if keyboard.is_pressed("0"):
            print(" -> You selected the protocol 0")
            protocol = 0
            break
        elif keyboard.is_pressed("1"):
            print(" -> You selected the protocol 1")
            protocol = 1
            break
        elif keyboard.is_pressed("2"):
            print(" -> You selected the protocol 2")
            protocol = 2
            break
        elif keyboard.is_pressed("3"):
            print(" -> You selected the protocol 3")
            protocol = 3
            break
        elif keyboard.is_pressed("5"):
            return True

    transport_layer = 10 # config = 10, continuous = 30, discontinuous=31
    print("Select the transport layer (continuous = c, discontinuous=d)")
    while True:
        if keyboard.is_pressed("c"):
            print(" -> You selected Continuous")
            transport_layer = 30
            break
        elif keyboard.is_pressed("d"):
            print(" -> You selected Discontinuous")
            transport_layer = 31
            break
    saveConfig(protocol, transport_layer)
    return False
    
def select_timeout():
    print("You have 3 seconds to change the protocol (press enter)")
    t0 = time.time()
    while(time.time() < t0+3):
        if keyboard.is_pressed("enter"):
            return select_options()
    return None
    