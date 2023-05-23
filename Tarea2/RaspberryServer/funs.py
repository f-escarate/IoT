import keyboard
import socket
from juntarFragm import TCP_frag_recv, UDP_frag_recv
from Desempaquetamiento import parseData, response, end_response
from DatabaseWork import saveConfig, getConfig
import sys, select
import time


def select_options():
    print("Select the protocol (0, 1, 2, 3) or 4 for close")
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
        elif keyboard.is_pressed("4"):
            return True

    transport_layer = 1 # TCP = 0 and UDP = 1
    if protocol in [0,1,2,3]:
        print("Select the transport layer (TCP = t and UDP = u)")
        while True:
            if keyboard.is_pressed("t"):
                print(" -> You selected TCP")
                transport_layer = 0
                break
            elif keyboard.is_pressed("u"):
                print(" -> You selected UDP")
                transport_layer = 1
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
    
def connection(host, port):
    s = socket.socket(socket.AF_INET, #internet
                  socket.SOCK_STREAM) #TCP
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(5)
    print(f"Listening on {host}:{port}")
    protocol, transport_layer = getConfig()
    while True:
        try:
            select = select_timeout() 
            if select:
                s.close()
                return
            elif select == False:
                protocol, transport_layer = getConfig()
                
            print("Waiting for connection...")
            conn, addr = s.accept()
        except KeyboardInterrupt:
            print("\nClosing")
            break
        
        print(f'Someone has been connected from {addr[0]}:{addr[1]}')
        change = False
        while True:
            try:
                data = TCP_frag_recv(conn)
                if data == b'':
                    break
            except KeyboardInterrupt:
                print("\nClosing connection")
                conn.close()
                s.close()
                return
            except ConnectionResetError:
                break
            except:
                conn.close()
                break
            parsedData = parseData(data)
            print('Data received: ', parsedData)
        
            # If the client, requested a protocol and transport_layer, we send it
            if parsedData["protocol"] == 4:
                change=True
            elif keyboard.is_pressed("c"):
                # Is true when the user selects "close connection"
                if select_options():
                    conn.send(end_response)
                    print("Closing Connection")
                    conn.close()
                    s.close()
                    return
                protocol, transport_layer = getConfig()
                change = True
            else:
                change = False
            
            send_bytes = response(change=change, status=transport_layer, protocol=protocol)
            conn.send(send_bytes)
            
            
            
            # If the next connection is with UDP, we try to connect using UDP socket
            if transport_layer == 1:
                print("-------------TO UDP----------------")
                conn.close()
                # Is true when the user selects "close connection"
                if recv_UDP((host, port), protocol):
                    print("Closing Connection")
                    return
                print("-------------TO TCP----------------")
                protocol, transport_layer = getConfig()
                try:
                    print("Waiting for connection...")
                    conn, addr = s.accept()
                except KeyboardInterrupt:
                    conn.close()
                    print("\nClosing Connection")
                    break
                continue

        conn.close()
        print('Disconnected')

def recv_UDP(address, protocol):
    s = socket.socket(socket.AF_INET, #internet
                  socket.SOCK_DGRAM) #UDP
    s.bind(address)
    
    change = False
    transport_layer = 1
    while True:
        while True:
            try:
                data, addr = UDP_frag_recv(s)
                print(f'Data received from {addr[0]}:{addr[1]}')
                if data == b'':
                    break
            except:
                break
            parsedData = parseData(data)
            
            # Print data
            print('Data received: ', parsedData)
            # Check for protocol/transport_layer change
            if keyboard.is_pressed("c"):
                # Is true when the user selects "close connection"
                if select_options():
                    s.sendto(end_response, addr)
                    return True
                protocol, transport_layer = getConfig()
                change = True
            else:
                change = False
            
            send_bytes = response(change=change, status=transport_layer, protocol=protocol)
            s.sendto(send_bytes, addr)
            
            # If the UDP connection is closed, we return
            if transport_layer == 0:
                s.close()
                return False
                
        print('Disconnected')
    return False
