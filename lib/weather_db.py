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
	def __init__(self, dbPath, wbit):
		self.wbit = wbit
		self.timer = None
		self.dbPath = dbPath

	def start(self):
		timeout = 300 - (int(time.time() % 300))
		self.timer = threading.Timer(timeout, self.loop)
		self.timer.start()

	def loop(self):
		file = self.dbPath+'/history-'+datetime.utcnow().strftime('%Y%m')+'.sqlite'
		conn =  None
		try:
			conn = sqlite3.connect(file)
			c = conn.cursor()
			sql = "CREATE TABLE IF NOT EXISTS history (id integer PRIMARY KEY, time int, name text, value text);"
			c.execute(sql)
			print(sqlite.version)
			conn.close()
		except:
			pass
		print("loop")
