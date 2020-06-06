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
