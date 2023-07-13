#!/usr/bin/env python3
"""PyBluez example read_name.py

Copyright (C) 2014, Oscar Acena <oscaracena@gmail.com>
This software is under the terms of GPLv3 or later.
"""

import time
import subprocess
import keyboard

from .TCPRaspServer import connect
from gattlib import GATTRequester, BTIOException
from .Desempaquetamiento import parseData, response
from .DatabaseWork import getConfig, saveBLELoss
from .bt_funs import select_options

sleeping = False
wifi = False

class Requester(GATTRequester):
	def __init__(self, *args):
		GATTRequester.__init__(self, *args)
		self.sleep_msg = "close".encode()
		self.wifi_msg = "towifi".encode()

	def on_notification(self, handle, data):
		global sleeping
		global wifi
		print("Notification received from handle:", hex(handle))
		if data[3:] == self.sleep_msg and (not sleeping):
			print("ESP32 sleeping")
			sleeping = True
			
		if data[3:] == self.wifi_msg:
			print("ESP32 ->>> to wifi")
			wifi = True
			
	def on_indication(self, handle, data):
		global sleeping
		print("Indication received from handle:",hex(handle))
		if data[3:] == self.sleep_msg and (not sleeping):
			print("ESP32 sleeping")
			sleeping = True

class GattConnector:
	def __init__(self, address):
		self.requester = Requester(address, False)
		self.connect(address)
		

	def connect(self, MAC):
		print(f"Trying to connect to {MAC}")
		connected = False
		num_attempts = 0
		t0 = time.time()
		while not connected:
			num_attempts += 1
			try:
				self.requester.connect(True)
				connected = True
			except BTIOException:
				print("Failed to connect... restarting in 10 seconds")
				time.sleep(10)

		dt = time.time() - t0
		saveBLELoss(dt, num_attempts)

		print("Connection successful.")

	def request_data(self):
		data = self.requester.read_by_handle(0x2a)[0]
		#data = self.requester.read_by_uuid("0000ff01-0000-1000-8000-00805f9b34fb")[0]
		return parseData(data, use_ble = True)
	
	def write_data(self, data):
		self.requester.write_by_handle(0x2a, data)
		

def req_and_write(obj: GattConnector, change, transport_layer, protocol):
	global sleeping
	try:
		data = obj.request_data()
		resp = response(change=change, status=transport_layer, protocol=protocol)
		obj.write_data(resp)
	except Exception as e:
		if not sleeping:
			print(e)


def run():
	global sleeping
	global wifi
	sleeping = False
	wifi = False
	MAC = '3c:61:05:15:a4:02'
	# Connecting to MAC
	obj = GattConnector(MAC)

	data = obj.request_data()
	
	change = True
	if data["protocol"] == 5:
		protocol, transport_layer = getConfig()
		resp = response(change=change, status=transport_layer, protocol=protocol)
		obj.write_data(resp)
		while(not sleeping and not wifi):
			if keyboard.is_pressed("c"):
				# Is true when the user selects "close connection"
				if select_options():
					resp = response(change=True, status=10, protocol=5)
					obj.write_data(resp)
					return False
				protocol, transport_layer = getConfig()
				change = True
			else:
				change = False

			req_and_write(obj, change, transport_layer, protocol)
				
		print("Disconnected.\n\n")
		return True
	

def connect_bt(worker,conf):
	global wifi
	# Apaga el wlan porque comparte la antena con bt
	subprocess.run(["sudo", "ip", "link", "set", "wlan0", "down"])
	select_options()
	while run():
		pass
		
	print("webos")
	# Se vuelve a encender el WLAN
	subprocess.run(["sudo", "ip", "link", "set", "wlan0", "up"])
	if wifi:
		connect(worker,conf)
		
		
