#include <math.h>
#include <stdlib.h>
#include <string.h>
#include <protocols.c>
#include "esp_system.h"
#include "esp_mac.h"
#include "esp_log.h"


static const char *TAG2 = "PACKETING";
static const char *end_of_pkg = "~end~";
static const char end_len = 5;


//Genera el header de un mensaje, con la MAC, el protocolo, status, y el largo del mensaje.
char* header(char protocol, char transportLayer){
	char* head = malloc(12);

    unsigned short ID = 2023;
    memcpy(head, &ID, 2);

	uint8_t* MACaddrs = malloc(6);
	esp_efuse_mac_get_default(MACaddrs);	//172,103,178,60,18,148
	memcpy((void*) &(head[2]), (void*) MACaddrs, 6);
	
	char prtl[2] = {protocol, transportLayer};
	memcpy((void*) &(head[8]), (void*) prtl, 2);

	unsigned short dataLen = dataLength(protocol);

	memcpy((void*) &(head[10]), (void*) &dataLen, 2);
	free(MACaddrs);
	ESP_LOGI(TAG2, "head: %u,%u,%u,%u,%u,%u,%u,%u,%u,%u,%u,%u", head[0], head[1], head[2],head[3], head[4], head[5],
	head[6], head[7], head[8],head[9], head[10], head[11]);

	return head;
}

unsigned short messageLength(char protocol){
    return 12+dataLength(protocol)+end_len;
}

char* mensaje (char protocol, char transportLayer){
	unsigned short msg_len = messageLength(protocol);
	char* mnsj = malloc(msg_len);
	char* hdr = header(protocol, transportLayer);
	char* data;
	switch (protocol) {
		case 0:
			data = dataprotocol0();
			break;
		case 1:
			data = dataprotocol1();
			break;
		case 2:
			data = dataprotocol2();
			break;
        case 3:
			data = dataprotocol3();
			break;
        case 4:
			data = dataprotocol4();
			break;
		case 5:
			data = data_request();
			break;
		default:
			data = dataprotocol0();
			break;
	}
	ESP_LOGI(TAG2, "Dataaaaa: %s", data);
	memcpy((void*) mnsj, (void*) hdr, 12);										// Coping header
	ESP_LOGI(TAG2, "Dataaaaa:1 %s", data);
	memcpy((void*) mnsj+12, (void*) data, dataLength(protocol));				// Coping data
	ESP_LOGI(TAG2, "Dataaaaa:2 %s", data);
	memcpy((void*) mnsj+12+dataLength(protocol), (void*) end_of_pkg, end_len);	// Coping end of package
	ESP_LOGI(TAG2, "Dataaaaa:3 %s", data);

	ESP_LOGI(TAG2, "HEADER: %s", hdr);
	ESP_LOGI(TAG2, "Data: %s", data);
	ESP_LOGI(TAG2, "eom: %s", end_of_pkg);
	ESP_LOGI(TAG2, "paquete: %s", mnsj);
	free(hdr);
	free(data);
	return mnsj;
}