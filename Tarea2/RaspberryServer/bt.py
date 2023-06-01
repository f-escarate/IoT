#!/usr/bin/env python3
"""PyBluez example read_name.py

Copyright (C) 2014, Oscar Acena <oscaracena@gmail.com>
This software is under the terms of GPLv3 or later.
"""

import sys
import subprocess
import keyboard

from gattlib import GATTRequester
from Desempaquetamiento import parseData, response, end_response
from DatabaseWork import getConfig
from bt_funs import select_options


class GattConnector:
    def __init__(self, address):
        self.requester = GATTRequester(address, False)
        self.connect()

    def connect(self):
        print("Connecting...", end=" ")
        sys.stdout.flush()

        self.requester.connect(True)
        print("OK.")

    def request_data(self):
        data = self.requester.read_by_handle(0x2a)[0]
        #data = self.requester.read_by_uuid("0000ff01-0000-1000-8000-00805f9b34fb")[0]
        return parseData(data)
    
    def write_data(self, data):
        self.requester.write_by_handle(0x2a, data)
		
if __name__ == "__main__":
	# Apaga el wlan porque comparte la antena con bt
	select_options()
	subprocess.run(["sudo", "ip", "link", "set", "wlan0", "down"])
	
	obj = GattConnector('3c:61:05:15:a4:02')
    
	data = obj.request_data()
	
	change = True
	if data["protocol"] == 5:
		protocol, transport_layer = getConfig()
		resp = response(change=change, status=transport_layer, protocol=protocol)
		obj.write_data(resp)
		while(True):
			if keyboard.is_pressed("c"):
				# Is true when the user selects "close connection"
				if select_options():
					break
				protocol, transport_layer = getConfig()
				change = True
			else:
				change = False

			data = obj.request_data()   # First message
			resp = response(change=change, status=transport_layer, protocol=protocol)
			obj.write_data(resp)

		print("Done.")
	
	# Se vuelve a encender el WLAN
	subprocess.run(["sudo", "ip", "link", "set", "wlan0", "up"])
