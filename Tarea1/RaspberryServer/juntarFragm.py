end_of_packet = "~end~".encode()

def TCP_frag_recv(conn):
    doc = b""
    while True:
        try:
            conn.settimeout(5)
            doc += conn.recv(1024)
            idx = doc.find(end_of_packet)
            print(len(doc), doc, idx)
            if idx != -1:
                doc = doc[:idx]
                break
        except TimeoutError:
            conn.send(b'\0')
            raise
        except Exception:
            conn.send(b'\0')
            raise
        conn.send(b'\1')

    # Replacing the '\n' that we put on the ESP-32 for '\0'
    res = doc.replace(b'\n', b'\0')
    print("doooc", res)
    return res

def UDP_frag_recv(s):
    doc = b""
    addr = None
    while True:
        try:

            data, addr = s.recvfrom(1024)
            if data == b'\0':
                break
            else:
                doc += data
        except TimeoutError:
            raise
        except Exception:
            raise
        # s.sendto(b'\1', addr)
    return (doc, addr)