import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="p455w0rd"
)

mycursor = mydb.cursor()

# Se crea la base de datos para la tarea
mycursor.execute("CREATE DATABASE T1_IoT")
#mycursor.execute("DROP DATABASE T1_IoT")
mycursor.execute("SHOW DATABASES")
for x in mycursor:
  print(x)

# Se crean las tablas
CreateDatos = '''CREATE TABLE Datos (
    MessageId INTEGER PRIMARY KEY,
    MAC TEXT NOT NULL,
    Status INTEGER NOT NULL,
    Protocol INTEGER NOT NULL,
    BattLevel INTEGER NOT NULL,
    Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
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
    AccZ JSON,
);'''

CreateLogs = '''CREATE TABLE Logs (
    ID_Device INTEGER PRIMARY KEY,
    TransportLayer INTEGER NOT NULL,
    Protocol INTEGER NOT NULL,
    Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
);'''

CreateConfiguracion = '''CREATE TABLE Configuracion (
    Protocol INTEGER NOT NULL,
    TransportLayer INTEGER NOT NULL
);'''

CreateLoss = '''CREATE TABLE Loss (
    MessageId INTEGER,
    Delay DATETIME DEFAULT CURRENT_TIMESTAMP,
    PacketLoss INTEGER,
    PRIMARY KEY (MessageId)
    FOREIGN KEY (MessageId) REFERENCES Datos(MessageId)
);'''


mycursor.execute(CreateDatos)
mycursor.execute(CreateLogs)
mycursor.execute(CreateConfiguracion)
mycursor.execute(CreateLoss)