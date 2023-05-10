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


extern void tcp_client(char* pkg);
extern char* tcp_client_recv(void);
extern void udp_client_task(void *pvParameters);
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


    // Initial connection
    char* config = tcp_client_recv();
    char ID_protocol = config[1];
    char Transport_Layer = config[2];
    ESP_LOGE(TAG3, "protocol %u transportlayer %u:", ID_protocol, Transport_Layer);


    // Creating the pkg based on the protocol
    char* pkg = mensaje(ID_protocol, Transport_Layer);

    // Selecting TCP=0 or UDP=1 in order to send the message
    if (Transport_Layer == 0) {
        tcp_client(pkg);
    }
    else if (Transport_Layer == 1) {
        xTaskCreate(udp_client_task, "udp_client", 4096, pkg, 5, NULL);
    }

    // 
    
}
