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

import os.path
import json

class c_config():
	def __init__(self):
		self.data = {}
		self.file = 'cfg.json'

	def load(self, file = None):
		if not file == None:
			self.file = file
		if os.path.isfile(self.file):
			with open(self.file) as f:
				try:
					self.data = json.loads(f.read())
				except:
					pass
				f.close()

	def save(self, file = None):
		if not file == None:
			self.file = file
		try:
			f = open(self.file, "w")
			f.write(json.dumps(self.data))
			f.close()
		except:
			pass
