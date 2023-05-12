import json
import mysql.connector

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
        
    cur.execute('''INSERT INTO Datos (DeviceID, MAC, Status, Protocol, BattLevel, Timestamp, Temp, Press, Hum, Co, RMS, AmpX, FreqX, AmpY, FreqY, AmpZ, FreqZ, AccX, AccY, AccZ) 
    values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', tuple(insertData.values()))
    
    mydb.commit()
    
    
def saveLog(header, data):
    #mydb = mysql.connector.connect(
    # host = "localhost",
    #  user = "root",
    #   password = "123"
    #)
    #cur = mydb.cursor()
    
    #cur.execute('''INSERT INTO T1_IoT.Logs ()  values ()''', () )
    
    pass


