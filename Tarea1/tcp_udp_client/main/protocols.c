#include <sensors.c>
#include <stdlib.h>
#include <string.h>


unsigned short lengmsg[6] = {2, 6, 16, 20, 44, 12016};
// Entrega los posibles largos de cada protocolo
unsigned short dataLength(char protocol){
    return lengmsg[ (unsigned int) protocol]-1;
}

// Arma un paquete para el protocolo de inicio, que busca solo respuesta
char* dataprotocol00(){
    char* msg = malloc(dataLength(0));
    msg[0] = 1;
    return msg;
}

// Arma un paquete para el protocolo 0, con la bateria
char* dataprotocol0(){
    
    char* msg = malloc(dataLength(1));
    float batt = batt_sensor();
    msg[0] = batt;
    long t = 0;
    memcpy((void*) &(msg[1]), (void*) &t, 4);
    return msg;
}

/* 
char* dataprotocol1(){
    
    char* msg = malloc(dataLength(2));

    float batt = batt_sensor();
    msg[0] = batt;


    int t = 0;
    memcpy((void*) &(msg[1]), (void*) &t, 4);

    char temp = THPC_sensor_temp();
    msg[5] = temp;


    float press = THPC_sensor_pres();
    memcpy((void*) &(msg[6]), (void*) &press, 4);

    char hum = THPC_sensor_hum();
    msg[10] = hum;

    float co = THPC_sensor_co();
    memcpy((void*) &(msg[11]), (void*) &co, 4);

    return msg;
} */
