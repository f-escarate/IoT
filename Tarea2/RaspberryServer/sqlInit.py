import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="123",
  database="T2_IoT"
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
    FreqZ FLOAT
);'''

CreateLogs = '''CREATE TABLE Logs (
    ID_Device INTEGER,
    TransportLayer INTEGER NOT NULL,
    Protocol INTEGER NOT NULL,
    Timestamp BIGINT
);'''

CreateConfiguracion = '''CREATE TABLE Configuracion (
    Protocol INTEGER NOT NULL,
    TransportLayer INTEGER NOT NULL
);'''

CreateLoss = '''CREATE TABLE Loss (
    MessageId INTEGER,
    Delay INTEGER,
    PacketLoss INTEGER,
    PRIMARY KEY (MessageId),
    FOREIGN KEY (MessageId) REFERENCES Datos(MessageId)
);'''

mycursor.execute("DROP TABLE Logs")
mycursor.execute("DROP TABLE Loss")
mycursor.execute("DROP TABLE Configuracion")
mycursor.execute("DROP TABLE Datos")

mycursor.execute(CreateDatos)
mycursor.execute(CreateLogs)
mycursor.execute(CreateConfiguracion)
mycursor.execute(CreateLoss)
