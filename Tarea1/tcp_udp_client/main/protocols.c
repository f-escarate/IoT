#include <sensors.c>
#include <stdlib.h>
#include <string.h>
#include "esp_log.h"

static const char *TAG8 = "PRotocols";

unsigned short lengmsg[6] = {6, 16, 20, 44, 24016, 2};
// Entrega los posibles largos de cada protocolo
unsigned short dataLength(char protocol){
    return lengmsg[ (unsigned int) protocol];
}

// Arma un paquete para el protocolo de inicio, que busca solo respuesta
char* data_request(){
    char* msg = malloc(2);
    msg[0] = 'g';
    msg[1] = 'a';
    return msg;
}

// Arma un paquete para el protocolo 0, con la bateria
char* dataprotocol0(){
    char* msg = malloc(dataLength(0));

    char val = 1;
    float batt = batt_sensor();
    int t = get_time();

    msg[0] = val;
    msg[1] = batt;
    memcpy((void*) &(msg[2]), (void*) &t, 4);
    return msg;
}


char* dataprotocol1(){
    char* msg = malloc(dataLength(1));
    
    char val = 1;               // 1 byte <- hay que ver que es esto
    char batt = batt_sensor();  // 1 byte
    int t = get_time();         // 4 bytes
    char* tphc = TPHC_sensor(); // 10 bytes

    ESP_LOGI(TAG8, "time: %d", t);
    
    msg[0] = val;
    msg[1] = batt;
    memcpy((void*) &(msg[2]), (void*) &t, 4);
    memcpy((void*) &(msg[6]), (void*) tphc, 10);
    return msg;
}

char* dataprotocol2(){
    char* msg = malloc(dataLength(2));
    
    char val = 1;                       // 1 byte <- hay que ver que es esto
    char batt = batt_sensor();          // 1 byte
    int t = get_time();                 // 4 bytes
    char* tphc = TPHC_sensor();         // 10 bytes
    float* akpi = accelerometer_kpi();
    float rms = akpi[0];                // 4 bytes
    free(akpi);
    
    msg[0] = val;
    msg[1] = batt;

    memcpy((void*) &(msg[2]), (void*) &t, 4);
    memcpy((void*) &(msg[6]), (void*) tphc, 10);
    memcpy((void*) &(msg[16]), (void*) &rms, 4);


    return msg;
}

char* dataprotocol3(){
    char* msg = malloc(dataLength(3));
    
    char val = 1;                       // 1 byte <- hay que ver que es esto
    char batt = batt_sensor();          // 1 byte
    int t = get_time();;                // 4 bytes
    char* tphc = TPHC_sensor();         // 10 bytes
    float* akpi = accelerometer_kpi();  // 28 bytes
    
    msg[0] = val;
    msg[1] = batt;

    memcpy((void*) &(msg[2]), (void*) &t, 4);
    memcpy((void*) &(msg[6]), (void*) tphc, 10);
    memcpy((void*) &(msg[16]), (void*) akpi, 28);
    free(tphc);
    free(akpi);

    return msg;
}

char* dataprotocol4(){
    ESP_LOGI("sensors", "..... 0");
    char* msg = malloc(dataLength(4));
    ESP_LOGI("sensors", "..... 1");

    char val = 1;                           // 1 byte <- hay que ver que es esto
    char batt = batt_sensor();              // 1 byte
    int t = get_time();;                    // 4 bytes
    char* tphc = TPHC_sensor();             // 10 bytes
    ESP_LOGI("sensors", "..... 1.5");
    float* acc = accelerometer_sensor();   // 24000 bytes
    ESP_LOGI("sensors", "..... 2");
    
    msg[0] = val;
    msg[1] = batt;
    memcpy((void*) &(msg[2]), (void*) &t, 4);
    memcpy((void*) &(msg[6]), (void*) tphc, 10);
    memcpy((void*) &(msg[16]), (void*) acc, 24000);

    ESP_LOGI("sensors", "..... 3");
    free(tphc);
    free(acc);
    ESP_LOGI("sensors", "..... 4");


    return msg;
}
