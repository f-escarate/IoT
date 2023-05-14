import json
import mysql.connector
import time

# Documentación https://docs.python.org/3/library/sqlite3.html

def dataSave(header, data):
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "123",
        database="T1_IoT"
    )
    cur = mydb.cursor()
    
    insertData = {
            "DeviceId": header["ID_device"],
            "MAC": header["MAC"],
            "Status": header["status"] ,
            "Protocol": header["protocol"],
            "Batt_level": None,
            "Timestamp": None,
            "Temp": None,
            "Pres": None,
            "Hum": None,
            "Co": None,
            "RMS": None,
            "AmpX": None,
            "FreqX": None,
            "AmpY": None,
            "FreqY": None,
            "AmpZ": None,
            "FreqZ": None,
            "AccX": None,
            "AccY": None,
            "AccZ": None
            }
    # Replacing the data in the dictionary 
    for key in insertData:
        if key in data:
            insertData[key] = data[key]
    
    # If is the 4th protocol, we transform the lists to json data
    if insertData["Protocol"] == 4:
        insertData["AccX"] = json.dumps(insertData["AccX"])
        insertData["AccY"] = json.dumps(insertData["AccY"])
        insertData["AccZ"] = json.dumps(insertData["AccZ"])
    
    print("Timestamp: ", insertData["Timestamp"])
        
    cur.execute('''INSERT INTO Datos (DeviceId, MAC, Status, Protocol, BattLevel, Timestamp, Temp, Press, Hum, Co, RMS, AmpX, FreqX, AmpY, FreqY, AmpZ, FreqZ, AccX, AccY, AccZ) 
    values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', tuple(insertData.values()))
    
    mydb.commit()
    
def saveLog(header, data):
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "123",
        database="T1_IoT"
    )
    cur = mydb.cursor()

    insertData = {
            "DeviceId": header["ID_device"],
            "Status": header["status"] ,
            "Protocol": header["protocol"],
            "TimeStamp": data["Timestamp"]
            }
    
    cur.execute('''INSERT INTO Logs (ID_Device, TransportLayer, Protocol, Timestamp)  values (%s, %s, %s, %s)''', tuple(insertData.values()))
    mydb.commit()

def saveLoss(data):
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "123",
        database="T1_IoT"
    )
    cur = mydb.cursor()
    cur.execute('''INSERT INTO Loss (MessageID, Delay, PacketLoss)  values (%s, %s, %s)''', data)
    mydb.commit()

def getMessageID():
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "123",
        database="T1_IoT"
    )
    cur = mydb.cursor()
    cur.execute(''' SELECT MessageId from Datos ORDER BY MessageId DESC LIMIT 1''')
    

    message_id = cur.fetchall()[0]
    print("Message_id: " + str(message_id))

    return message_id

def saveConfig(protocol, transport_layer):
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "123",
        database="T1_IoT"
    )
    cur = mydb.cursor()
    cur.execute('''UPDATE Configuracion SET Protocol=%s, TransportLayer=%s''', (protocol, transport_layer))
    mydb.commit()

def getConfig():
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "123",
        database="T1_IoT"
    )
    cur = mydb.cursor()
    cur.execute(''' SELECT Protocol, TransportLayer from Configuracion''')
    protocol, transport_layer = cur.fetchall()[0]
    return protocol, transport_layer

