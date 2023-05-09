#include <math.h>
#include <stdlib.h>
#include <string.h>
#include "esp_system.h"
#include "esp_mac.h"
#include "esp_log.h"
#include <time.h>

#define PI 3.14159265358979323846

/*

Aqui generamos los 5 tipos de protocolos con sus datos.
Las timestamps en realidad siempre mandamos 0, y por comodidad 
guardamos la timestampo del tiempo de llegada en el servidor de la raspberry.


En general los "mensajes" los creamos copiando a la mala (con memcpy) la memoria de los datos en un char*.
No es muy elegante pero funciona.

Al final lo único que se usa fuera de este archivo es:

message: dado un protocolo, crea un mensaje (con header y datos) codificado en un array de bytes (char*).
messageLength: dado un protocolo, entrega el largo del mensaje correspondiente

*/

float randf(float min, float max){
    return min + (float)rand()/(float)(RAND_MAX/(max-min));
}
int randi(int min, int max){
    return (rand() % (max-min+1))+min;
}

float** accelerometer_sensor(){
    float arr_x[2000];
    float arr_y[2000];
    float arr_z[2000];

    for (int i = 0; i < 2000; i++){
        arr_x[i] = 2*sin(2*PI*0.001*randf(-8000, 8000));
        arr_y[i] = 3*cos(2*PI*0.001*randf(-8000, 8000));
        arr_z[i] = 10*sin(2*PI*0.001*randf(-8000, 8000));
    }
    float** result = malloc(3*2000*sizeof(float));
    result[0] = arr_x;
    result[1] = arr_y;
    result[2] = arr_z;
    return result;
}

char* THPC_sensor(){
    char *result = malloc(10*sizeof(char));         //10 bytes

    char temp = (rand() % 25) + 5;                  //1 byte
    unsigned int press = (rand() % 200) + 1000;     //4 bytes
    char hum = randi(30, 80);                       //1 byte
    float co2 = randf(30, 200);                     //4 bytes

    result[0] = temp;
    memcpy((void*) &(result[1]), (void*) &press, 4);
    result[5] = hum;
    memcpy((void*) &(result[6]), (void*) &co2, 4);
    return result;
}

// Entrega el valor de la batería (entre 1 y 100)
char batt_sensor(){
    return (rand() % 100) + 1;
}

//  
float* accelerometer_kpi(){
    float amp_x = randf(0.0059, 0.12);
    float amp_y = randf(0.0041, 31.0);
    float amp_z = randf(0.008, 0.15);
    
    float frec_x = randf(29.0, 31.0);
    float frec_y = randf(59.0, 61.0);
    float frec_z = randf(89.0, 91.0);

    float rms = sqrt(pow(amp_x, 2) + pow(amp_y, 2) + pow(amp_z, 2));

    float* result = malloc(7*sizeof(float));
    result[0] = rms;
    result[1] = amp_x;
    result[2] = frec_x;
    result[3] = amp_y;
    result[4] = frec_y;
    result[5] = amp_z;
    result[6] = frec_z;

    return result;

}

int get_time() {
    time_t s;  // Seconds
    struct timespec spec;
    clock_gettime(CLOCK_REALTIME, &spec);
    s  = spec.tv_sec;
    return (int) s;
}
