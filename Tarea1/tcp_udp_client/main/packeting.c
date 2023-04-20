#include <math.h>
#include <stdlib.h>
#include <string.h>
#include <protocols.c>
#include "esp_system.h"
#include "esp_mac.h"
#include "esp_log.h"

//Genera el header de un mensaje, con la MAC, el protocolo, status, y el largo del mensaje.
char* header(char protocol, char transportLayer){
	char* head = malloc(12);

    char ID[2] = {'D', '1'};
    memcpy(head, ID, 2);

	uint8_t* MACaddrs = malloc(6);
	esp_efuse_mac_get_default(MACaddrs);
	memcpy((void*) &(head[2]), (void*) MACaddrs, 6);

    head[8]= transportLayer;
	head[9]= protocol;
	unsigned short dataLen = dataLength(protocol);
	memcpy((void*) &(head[10]), (void*) &dataLen, 2);
	free(MACaddrs);
	return head;
}

unsigned short messageLength(char protocol){
    return 1+12+dataLength(protocol);
}

char* mensaje (char protocol, char transportLayer){
	char* mnsj = malloc(messageLength(protocol));
	mnsj[messageLength(protocol)-1]= '\0';
	char* hdr = header(protocol, transportLayer);
	char* data;
	switch (protocol) {
		case 0:
			data = dataprotocol00();
			break;
		case 1:
			data = dataprotocol0();
			break;
		/* 
		case 2:
			data = dataprotocol1();
			break;
		case 3:
			data = dataprotocol2();
			break;
        case 4:
			data = dataprotocol3();
			break;
        case 5:
			data = dataprotocol4();
			break; */
		default:
			data = dataprotocol0();
			break;
	}
	memcpy((void*) mnsj, (void*) hdr, 12);
	memcpy((void*) &(mnsj[12]), (void*) data, dataLength(protocol));
	free(hdr);
	free(data);
	return mnsj;
}