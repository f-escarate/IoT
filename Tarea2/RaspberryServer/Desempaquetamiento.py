from struct import unpack, pack
import traceback
from DatabaseWork import * 

# Documentación struct unpack,pack :https://docs.python.org/3/library/struct.html#
'''
Estas funciones se encargan de parsear y guardar los datos recibidos.
Usamos struct para pasar de un array de bytes a una lista de numeros/strings. (https://docs.python.org/3/library/struct.html)
(La ESP32 manda los bytes en formato little-endian, por lo que los format strings deben empezar con <)

-dataSave: Guarda los datos en la BDD
-response: genera un OK para mandar de vuelta cuando se recibe un mensaje, con posibilidad de pedir que se cambie el status/protocol
-protUnpack: desempaca un byte array con los datos de un mensaje (sin el header)
-headerDict: Transforma el byte array de header (los primeros 10 bytes de cada mensaje) en un diccionario con la info del header
-dataDict: Transforma el byta array de datos (los bytes luego de los primeros 10) en un diccionario con los datos edl mensaje

'''

begin_time = 0
esp_time = 0
end_response = pack("<BBBB", 0, 0, 0, 0)
    
def response(change:bool=False, status:int=255, protocol:int=255):
    OK = 1
    CHANGE = 1 if change else 0
    return pack("<BBBB", OK, CHANGE, status, protocol)

def parseData(packet):
    global begin_time
    global esp_time
    
    header = packet[:12]
    data = packet[12:]
    header = headerDict(header)
    dataD = dataDict(header["protocol"], data)
    
    if dataD is not None:
        if header["protocol"] == 5:
            begin_time = round(time.time()*1000)
            esp_time = dataD['Timestamp']
            saveLog(header, dataD)
            #print("primer tiempo ", dataD['Timestamp'])
        else:
            current_time = round(time.time()*1000)
            dataD['Timestamp'] = begin_time+(dataD['Timestamp']-esp_time)
            deltaT = current_time - dataD['Timestamp']
            #print("---Timestamp: ", dataD['Timestamp'])
            #print("....DELTAT ", deltaT)
            dataSave(header, dataD)
            message_id = getMessageID()
            #print("---------aaaaaaaaaa ", message_id)
            loss_data = (message_id[0], deltaT, header['length'] - len(data))

            saveLoss(loss_data)
        
    return None if dataD is None else {**header, **dataD}

# Ver https://docs.python.org/3/library/struct.html para más detalles
def protUnpack(protocol:int, data):
    protocol_unpack = ["<BBi", "<BBiBIBf","<BBiBIBff","<BBiBIBffffffff", "<i"]
    """
    < :     little endian
    B :     unsigned char
    i :     int
    I :     unsigned int
    f :     float
    8000s:  char[8000]
    
    protocolo 0:    "<BBi"
    protocolo 1:    "<BBiBIBf"
    protocolo 2:    "<BBiBIBff"
    protocolo 3:    "<BBiBIBffffffff"
    protocolo_req:  "<BB"
    
    """
    
    res = unpack(protocol_unpack[protocol], data)    
    return res

def headerDict(data):
    ID_device, M1, M2, M3, M4, M5, M6, protocol, status, leng_msg = unpack("<H6B2BH", data)
    MAC = ".".join([hex(x)[2:] for x in [M1, M2, M3, M4, M5, M6]])
    return {"ID_device": ID_device, "MAC":MAC, "protocol":protocol, "status":status, "length":leng_msg}

def dataDict(protocol:int, data):
    if protocol not in [0, 1, 2, 3, 4]:
        print("Error: protocol doesnt exist")
        return None
    def protFunc(protocol, keys):
        def p(data):
            unp = protUnpack(protocol, data)
            return {key:val for (key,val) in zip(keys, unp)}
        return p
    p0 = ["Val", "Batt_level", "Timestamp"]
    p1 = ["Val", "Batt_level", "Timestamp", "Temp", "Pres", "Hum", "Co"]
    p2 = ["Val", "Batt_level", "Timestamp", "Temp", "Pres", "Hum", "Co", "RMS"]
    p3 = ["Val", "Batt_level", "Timestamp", "Temp", "Pres", "Hum", "Co", "RMS", "AmpX", "FreqX", "AmpY", "FreqY", "AmpZ", "FreqZ"]
    p_req = ["Timestamp"]
    p = [p0, p1, p2, p3, p_req]

    try:
        return protFunc(protocol, p[protocol])(data)
    except Exception:
        print("Data unpacking Error:", traceback.format_exc())
        return None
