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

import time
import threading
import sqlite3
from datetime import datetime

class c_weather_db():
	def __init__(self, dbPath, wbit, oweather):
		self.wbit = wbit
		self.oweather = oweather
		self.timer = None
		self.dbPath = dbPath
		self.running = False

	def start(self):
		self.running = True
		timeout = 900 - (int(time.time() % 900))
		self.timer = threading.Timer(timeout, self.loop)
		self.timer.start()

	def stop(self):
		self.running = False
		if not (self.timer == None):
			self.timer.chancel()

	def loop(self):
		file = self.dbPath+'/history-'+datetime.utcnow().strftime('%Y%m')+'.sqlite'
		conn =  None
		try:
			conn = sqlite3.connect(file)
			c = conn.cursor()
			sql = "CREATE TABLE IF NOT EXISTS history (id integer PRIMARY KEY, time int, name text, value text);"
			c.execute(sql)
			conn.commit()
			last = 0
			sql = "select time from history where name='clouds' order by id desc limit 1"
			c.execute(sql)
			record = c.fetchone()
			if record:
				last = record[0]
			if self.wbit.valid:
				sql = '''INSERT INTO history (time, name, value) VALUES(?,?,?) '''
				cur = self.wbit.data["current"]
				if not (str(last) == str(cur["ts"])):
					c.execute(sql, (cur["ts"],"humidity", str(cur["rh"])))
					c.execute(sql, (cur["ts"],"pressure", str(cur["pres"])))
					c.execute(sql, (cur["ts"],"clouds", str(cur["clouds"])))
					c.execute(sql, (cur["ts"],"solar_rad", str(cur["solar_rad"]))) #W/m*m
					c.execute(sql, (cur["ts"],"wind_speed", str(cur["wind_spd"])))
					c.execute(sql, (cur["ts"],"wind_dir", str(cur["wind_dir"])))
					c.execute(sql, (cur["ts"],"wind_dir_str", str(cur["wind_cdir"])))
					c.execute(sql, (cur["ts"],"visibility", str(cur["vis"]))) # km
					c.execute(sql, (cur["ts"],"solar_hour_angle", str(cur["h_angle"])))
					c.execute(sql, (cur["ts"],"sunset", str(cur["sunset"])))
					c.execute(sql, (cur["ts"],"sunrise", str(cur["sunrise"])))
					c.execute(sql, (cur["ts"],"snow", str(cur["snow"])))
					c.execute(sql, (cur["ts"],"rain", str(cur["precip"])))
					c.execute(sql, (cur["ts"],"uv_index", str(cur["uv"])))
					c.execute(sql, (cur["ts"],"air_quality_index", str(cur["aqi"])))
					c.execute(sql, (cur["ts"],"temperature", str(cur["temp"])))
					c.execute(sql, (cur["ts"],"solar_evalation", str(cur["elev_angle"])))
					c.execute(sql, (cur["ts"],"temperature_feel", str(cur["app_temp"])))
					c.execute(sql, (cur["ts"],"description", str(cur["weather"]["description"])))
					c.execute(sql, (cur["ts"],"icon", str(cur["weather"]["icon"])))
					c.execute(sql, (cur["ts"],"code", str(cur["weather"]["code"])))
			elif self.oweather.valid:
				cur = self.oweather.data["current"]
				if not (str(last) == str(cur["dt"])):
					c.execute(sql, (cur["dt"],"sunrise", datetime.utcfromtimestamp(cur["sunrise"]).strftime('%H:%M')))
					c.execute(sql, (cur["dt"],"sunset", datetime.utcfromtimestamp(cur["sunset"]).strftime('%H:%M')))
					c.execute(sql, (cur["dt"],"temperature", str(cur["temp"])))
					c.execute(sql, (cur["dt"],"temperature_feel", str(cur["feels_like"])))
					c.execute(sql, (cur["dt"],"humidity", str(cur["humidity"])))
					c.execute(sql, (cur["dt"],"pressure", str(cur["pressure"])))
					c.execute(sql, (cur["dt"],"uv_index", str(cur["uvi"])))
					c.execute(sql, (cur["dt"],"clouds", str(cur["clouds"])))
					c.execute(sql, (cur["dt"],"visibility", str(cur["visibility"]/1000))) # km
					c.execute(sql, (cur["dt"],"wind_speed", str(cur["wind_speed"])))
					c.execute(sql, (cur["dt"],"wind_dir", str(cur["wind_deg"])))
					c.execute(sql, (cur["dt"],"description", str(cur["weather"]["description"])))
					pre = "t"
					if cur["weather"]["id"] > 199:
						pre = "d"
					elif cur["weather"]["id"] > 299:
						pre = "r"
					elif cur["weather"]["id"] > 499:
						pre = "s"
					elif cur["weather"]["id"] > 599:
						pre = "s"
					elif cur["weather"]["id"] > 699:
						pre = "a"
					elif cur["weather"]["id"] > 799:
						pre = "c"
					elif cur["weather"]["id"] > 899:
						pre = "u"
					c.execute(sql, (cur["dt"],"icon", pre+str(cur["weather"]["icon"])))
					c.execute(sql, (cur["dt"],"code", str(cur["weather"]["id"])))
			conn.commit()
			conn.close()
		except Exception as e:
			print(e)
		if self.running:
			timeout = 900 - (int(time.time() % 900))
			self.timer = threading.Timer(timeout, self.loop)
			self.timer.start()
