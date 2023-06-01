import pygatt
from time import sleep

# Definir los UUIDs de los servicios y características del dispositivo BLE
DEVICE_ADDRESS = '3c:61:05:15:a4:02'
#DEVICE_ADDRESS = '98:f6:21:67:92:51'
SERVICE_UUID = '0000fff0-0000-1000-8000-00805f9b34fb'
CHARACTERISTIC_UUID = '0000ff01-0000-1000-8000-00805f9b34fb'

#sudo gatttool -i hci0 -b 3c:61:05:15:a4:02 -I -t random
#connection refused 111

#sudo hcitool -i hci0 lescan

#bluetoothctl pair 3C:61:05:15:A4:02

#sudo ip link set wlan0 down

# Definir los estados de la máquina de estado
STATE_DISCONNECTED = 0
STATE_CONNECTING = 1
STATE_CONNECTED = 2

# Inicializar la conexión PyGatt y el estado inicial de la máquina de estado
adapter = pygatt.GATTToolBackend()
state = STATE_CONNECTING

# Función para manejar eventos de conexión
def handle_connection_event(event):
    global state
    if event == 'disconnected':
        print('El dispositivo se desconectó')
        state = STATE_DISCONNECTED
    elif event == 'connected':
        print('El dispositivo se conectó')
        state = STATE_CONNECTED

# Función para conectar al dispositivo BLE
def connect():
    global state
    print("connecting")
    device = adapter.connect(DEVICE_ADDRESS, address_type=pygatt.BLEAddressType.random, timeout=10, auto_reconnect=True)
    print("suscribing")
    device.subscribe(CHARACTERISTIC_UUID, callback=handle_notification)
    print("-- connected")
    state = STATE_CONNECTED
    
# Función para desconectar del dispositivo BLE
def disconnect():
    global state
    state = STATE_DISCONNECTED
    adapter.stop()

# Función para manejar notificaciones de características
def handle_notification(handle, value):
    print('Notificación recibida:', value.hex())

# Bucle principal de la máquina de estado
count = 0
while True:
    if state == STATE_DISCONNECTED:
        # Si el estado actual es desconectado, intentar conectar
        connect()
    elif state == STATE_CONNECTING:
        # Si el estado actual es conectando, esperar hasta que se conecte o se agote el tiempo de espera
        print("starting")
        count += 1
        print("count", count)
        try:
            adapter.start()
            sleep(1)
            connect()
        except pygatt.exceptions.BLEError as e:
            print(e)
            pass
    elif state == STATE_CONNECTED:
        # Si el estado actual es conectado, hacer cualquier operación necesaria en el dispositivo
        print("oooo")
        sleep(1)
