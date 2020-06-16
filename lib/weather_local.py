"""
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Version 1.0
"""

import paho.mqtt.client as mqtt
import time
import json

class weather_local:
	def __init__(self):
		self.cfg = None
		self.valid = False
		self.client = None
		self.temp = None
		self.humidity = None
		self.lux = None

	def on_connect(self, client, userdata, flags, rc):
		if rc == 0:
			if "temp" in self.cfg:
				self.client.subscribe(self.cfg["temp"])
			if "humidity" in self.cfg:
				self.client.subscribe(self.cfg["humidity"])
			if "lux" in self.cfg:
				self.client.subscribe(self.cfg["lux"])
		else:
			time.sleep(30)
			self.client.reconnect()

	def on_message(self, client, userdata, msg):
		if "temp" in self.cfg:
			if msg.topic == self.cfg["temp"]:
				self.temp = json.loads(msg.payload.decode())["val"]
				self.valid = True
		if "humidity" in self.cfg:
			if msg.topic == self.cfg["humidity"]:
				self.humidity = json.loads(msg.payload.decode())["val"]
				self.valid = True
		if "lux" in self.cfg:
			if msg.topic == self.cfg["lux"]:
				self.lux = json.loads(msg.payload.decode())["val"]
				self.valid = True

	def on_disconnect(client, userdata, rc):
		if rc != 0:
			self.client.reconnect()

	def start(self):
		if "host" in self.cfg and ("temp" in self.cfg or "humidity" in self.cfg or "lux" in self.cfg):
			self.client = mqtt.Client()
			self.client.on_connect = self.on_connect
			self.client.on_message = self.on_message
			self.client.connect(self.cfg["host"])
			self.client.loop_start()

	def stop(self):
		if not self.client == None:
			self.client.loop_stop()
