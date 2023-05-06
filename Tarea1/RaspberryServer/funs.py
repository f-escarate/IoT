import keyboard
from juntarFragm import TCP_frag_recv, UDP_frag_recv
from Desempaquetamiento import parseData

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
            break

    transport_layer = 1 # TCP = 0 and UDP = 1
    if protocol in [0,1,2,3]:
        print("Select the transport layer (TCP = 0 and UDP = 1)")
        while True:
            if keyboard.is_pressed("0"):
                print(" -> You selected TCP")
                transport_layer = 0
                break
            elif keyboard.is_pressed("1"):
                print(" -> You selected UDP")
                transport_layer = 1
                break
    return protocol, transport_layer

def connection(s, req_bytes):
    while True:
        try:
            conn, addr = s.accept()
        except KeyboardInterrupt:
            conn.close()
            print("\nCerrando la conexión")
            break
        
        print(f'Conectado por alguien ({addr[0]}) desde el puerto {addr[1]}')
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
            conn.send(req_bytes)
            conn.send(data)

        conn.close()
        print('Desconectado')