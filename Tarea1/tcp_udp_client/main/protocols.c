#include <sensors.c>
#include <stdlib.h>
#include <string.h>


unsigned short lengmsg[6] = {6, 16, 20, 44, 24016, 2};
// Entrega los posibles largos de cada protocolo
unsigned short dataLength(char protocol){
    return lengmsg[ (unsigned int) protocol]-1;
}

// Arma un paquete para el protocolo de inicio, que busca solo respuesta
char* data_request(){
    char* msg = malloc(2);
    msg[0] = 'g';
    msg[1] = '\0';
    return msg;
}

// Arma un paquete para el protocolo 0, con la bateria
char* dataprotocol0(){
    char* msg = malloc(dataLength(0));

    float batt = batt_sensor();
    long t = 0;

    msg[0] = batt;
    memcpy((void*) &(msg[1]), (void*) &t, 4);
    msg[dataLength(0)-1] = '\0';
    return msg;
}


char* dataprotocol1(){
    char* msg = malloc(dataLength(1));
    
    char val = 1;               // 1 byte <- hay que ver que es esto
    char batt = batt_sensor();  // 1 byte
    int t = 0;                  // 4 bytes
    char* thpc = THPC_sensor(); // 10 bytes
    
    msg[0] = val;
    msg[1] = batt;
    memcpy((void*) &(msg[2]), (void*) &t, 4);
    memcpy((void*) &(msg[6]), (void*) thpc, 10);
    return msg;
}

char* dataprotocol2(){
    char* msg = malloc(dataLength(2));
    return msg;
}

char* dataprotocol3(){
    char* msg = malloc(dataLength(3));
    return msg;
}

char* dataprotocol4(){
    char* msg = malloc(dataLength(4));

    char val = 1;                       // 1 byte <- hay que ver que es esto
    char batt = batt_sensor();          // 1 byte
    int t = 0;                          // 4 bytes
    char* thpc = THPC_sensor();         // 10 bytes
    float** acc = accelerometer_sensor();// 24000 bytes
    
    msg[0] = val;
    msg[1] = batt;
    memcpy((void*) &(msg[2]), (void*) &t, 4);
    memcpy((void*) &(msg[6]), (void*) thpc, 10);
    memcpy((void*) &(msg[16]), (void*) *acc, 24000);


    return msg;
}
