#!/media/pi/data/SM/smarthome/env/bin/python3

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

import __main__ as main_lib
import os, sys, time

basepath = os.path.dirname(os.path.abspath(main_lib.__file__))

sys.path.append(basepath+'/lib')

import config
import opencagedata
import weatherbit
import openweathermap
import weather_db
import weather_local

odata = None
wbit = None
oweather = None
wlocal = None
cfg = None
db = None

def callback_wbit():
	if wbit.valid and False:
		for e in wbit.data["current"]:
			print(e+"\t\t"+str(wbit.data["current"][e]))
#	print('new_data_wbit')

def callback_weather():
	if oweather.valid and False:
		for e in oweather.data["current"]:
			print(e+"\t\t"+str(oweather.data["current"][e]))
#	print('new_data_openweather')

def callback_geo():
	global odata, cfg

	if odata.valid:
		cfg.data['geo'] = odata.data['geometry']
		cfg.save()
		print("got geo")
	print("restart")
	sys.exit(1)

def main():
	global cfg
	cfg = config.c_config()
	cfg.load(basepath+"/cfg/"+os.path.splitext(os.path.basename(main_lib.__file__))[0]+".json")
	if not ('geo' in cfg.data):
		if "opencagedata" in cfg.data and "address" in cfg.data:
			global odata
			odata = opencagedata.c_opencagedata()
			odata.callback = callback_geo
			odata.key = cfg.data["opencagedata"]
			odata.forward(cfg.data["address"])
			return
		else:
			print("miss geo")
	global wbit
	if "weatherbit" in cfg.data:
		wbit = weatherbit.c_weatherbit()
		wbit.callback_newdata = callback_wbit
		wbit.key = cfg.data["weatherbit"]
		wbit.lat = cfg.data['geo']['lat']
		wbit.long = cfg.data['geo']['lng']
		wbit.start()
	global oweather
	if "openweathermap" in cfg.data:
		oweather = openweathermap.c_openweathermap()
		oweather.callback_newdata = callback_weather
		oweather.key = cfg.data["openweathermap"]
		oweather.lat = cfg.data['geo']['lat']
		oweather.long = cfg.data['geo']['lng']
		oweather.start()

	global wlocal
	if "local" in cfg.data:
		wlocal = weather_local.weather_local()
		wlocal.cfg = cfg.data["local"]
		wlocal.start()

	global db
	db = weather_db.c_weather_db(basepath+'/db', wbit, oweather, wlocal)
	db.start()

	while True:
		time.sleep(1)
	if not oweather == None:
		oweather.stop()
	if not wbit == None:
		wbit.stop()
	if not wlocal == None:
		wlocal.stop()
	if not db == None:
		db.stop()

if __name__ == '__main__':
	main()

