import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="123",
  database="T1_IoT"
)

mycursor = mydb.cursor()

# Se crea la base de datos para la tarea
#mycursor.execute("CREATE DATABASE T1_IoT")
#mycursor.execute("DROP DATABASE T1_IoT")
mycursor.execute("SHOW TABLES")
for x in mycursor:
  print(x)

# Se crean las tablas
CreateDatos = '''CREATE TABLE Datos (
    MessageId INTEGER PRIMARY KEY AUTO_INCREMENT,
    DeviceId INTEGER, 
    MAC TEXT NOT NULL,
    Status INTEGER NOT NULL,
    Protocol INTEGER NOT NULL,
    BattLevel INTEGER NOT NULL,
    Timestamp BIGINT,
    Temp INTEGER,
    Press FLOAT,
    Hum INTEGER,
    Co FLOAT,
    RMS FLOAT,
    AmpX FLOAT,
    FreqX FLOAT,
    AmpY FLOAT,
    FreqY FLOAT,
    AmpZ FLOAT,
    FreqZ FLOAT,
    AccX JSON,
    AccY JSON,
    AccZ JSON
);'''

CreateLogs = '''CREATE TABLE Logs (
    ID_Device INTEGER,
    TransportLayer INTEGER NOT NULL,
    Protocol INTEGER NOT NULL,
    Timestamp BIGINT
);'''

CreateConfiguracion = '''CREATE TABLE Configuracion (
    TransportLayer INTEGER NOT NULL,
    Protocol INTEGER NOT NULL,
    Asc_sampling INTEGER,
    Asc_sensibility INTEGER,
    Gyro_sensibility INTEGER,
    BME688_sampling INTEGER,
    Discontinous_time INTEGER,
    TCP_PORT INTEGER,
    UDP_PORT INTEGER,
    Host_ip_addr INTEGER,
    SSID VARCHAR(45),
    Pass VARCHAR(45)
);'''

CreateLoss = '''CREATE TABLE Loss (
    MessageId INTEGER,
    Delay INTEGER,
    PacketLoss INTEGER,
    PRIMARY KEY (MessageId),
    FOREIGN KEY (MessageId) REFERENCES Datos(MessageId)
);'''

CreateBLELoss = '''CREATE TABLE BLELoss (
    Delay FLOAT,
    Attempts INTEGER
);'''

mycursor.execute("DROP TABLE Logs")
mycursor.execute("DROP TABLE Loss")
mycursor.execute("DROP TABLE Configuracion")
mycursor.execute("DROP TABLE Datos")
mycursor.execute("DROP TABLE BLELoss")

mycursor.execute(CreateDatos)
mycursor.execute(CreateLogs)
mycursor.execute(CreateConfiguracion)
mycursor.execute(CreateLoss)
mycursor.execute(CreateBLELoss)
mycursor.execute('INSERT INTO Configuracion (Protocol, TransportLayer)  values (0, 0)')
mydb.commit()
