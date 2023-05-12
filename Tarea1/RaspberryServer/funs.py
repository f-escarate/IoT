import keyboard
import socket
from juntarFragm import TCP_frag_recv, UDP_frag_recv
from Desempaquetamiento import parseData, response

def select_options():
    print("Select the protocol (0, 1, 2, 3, 4) ")
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
            print(" -> You selected the protocol 4")
            protocol = 4
            break

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
    return protocol, transport_layer

def connection(host, port):
    s = socket.socket(socket.AF_INET, #internet
                  socket.SOCK_STREAM) #TCP
    s.bind((host, port))
    s.listen(5)
    print(f"Listening on {host}:{port}")
    protocol, transport_layer = select_options()
    
    while True:
        try:
            print("Esperando conexión...")
            conn, addr = s.accept()
        except KeyboardInterrupt:
            conn.close()
            print("\nCerrando la conexión")
            break
        
        print(f'Conectado por alguien ({addr[0]}) desde el puerto {addr[1]}')
        change = False
        while True:
            try:
                data = TCP_frag_recv(conn)
                if data == b'':
                    break
            except KeyboardInterrupt:
                print("\nCerrando la conexión")
                conn.close()
                return
            except ConnectionResetError:
                break
            except:
                conn.close()
                break
            print(f"Recibido {data}")
            parsedData = parseData(data)
            print(parsedData)
        
            # If the client, requested a protocol and transport_layer, we send it
            if parsedData["protocol"] == 5:
                change=True
            elif keyboard.is_pressed("c"):
                protocol, transport_layer = select_options()
                change = True
            else:
                change = False
            
            send_bytes = response(change=change, status=transport_layer, protocol=protocol)
            conn.send(send_bytes)
            
            
            
            # If the next connection is with UDP, we try to connect using UDP socket
            if transport_layer == 1:
                print("-------------TO UDP----------------")
                conn.close()
                protocol, transport_layer = recv_UDP((host, port), protocol)
                try:
                    print("Esperando conexión...")
                    conn, addr = s.accept()
                except KeyboardInterrupt:
                    conn.close()
                    print("\nCerrando la conexión")
                    break
                continue

        conn.close()
        print('Desconectado')

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
                print(f'Se recibe de ({addr[0]}) desde el puerto {addr[1]}')
                if data == b'':
                    break
            except:
                break
            parsedData = parseData(data)
            
            if keyboard.is_pressed("c"):
                protocol, transport_layer = select_options()
                change = True
            else:
                change = False
            
            send_bytes = response(change=change, status=transport_layer, protocol=protocol)
            s.sendto(send_bytes, addr)
            
            # If the UDP connection is closed, we return
            if transport_layer == 0:
                s.close()
                return protocol, transport_layer
                
        print('Desconectado')
    return protocol, transport_layer
