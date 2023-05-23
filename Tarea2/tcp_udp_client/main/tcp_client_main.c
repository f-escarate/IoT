/*
 * SPDX-FileCopyrightText: 2022 Espressif Systems (Shanghai) CO LTD
 *
 * SPDX-License-Identifier: Unlicense OR CC0-1.0
 */
#include "nvs_flash.h"
#include "esp_netif.h"
#include "protocol_examples_common.h"
#include "esp_event.h"
#include "esp_log.h"


extern char* tcp_client(char protocol);
extern char* udp_client_task(char protocol);
extern char* mensaje (char protocol, char transportLayer);


static const char *TAG3 = "main";

void app_main(void)
{
    ESP_ERROR_CHECK(nvs_flash_init());
    ESP_ERROR_CHECK(esp_netif_init());
    ESP_ERROR_CHECK(esp_event_loop_create_default());

    /* This helper function configures Wi-Fi or Ethernet, as selected in menuconfig.
     * Read "Establishing Wi-Fi or Ethernet Connection" section in
     * examples/protocols/README.md for more information about this function.
     */
    ESP_ERROR_CHECK(example_connect());

    // The first message to send is a request using tcp (transport_layer = 0)
    char protocol = 5; char transport_layer = 0;

    char* response = NULL; char ok = 1;
    while(ok){
        // Selecting TCP=0 or UDP=1 in order to send the message
        if (transport_layer == 0)
            response = tcp_client(protocol);
        else if (transport_layer == 1) 
            response = udp_client_task(protocol);
        
        ok = response[0];
        transport_layer = response[2];
        protocol = response[3];
        free(response);
        
        ESP_LOGE(TAG3, "%u,%u,%u,%u,protocol %u transportlayer %u:",response[0],response[1],response[2],response[3], protocol, transport_layer);
    }
}
