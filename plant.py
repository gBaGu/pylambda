
class Plant:
	__slots__ = ['id', 'name', 'lastEditDate', 'wateringInterval']

	def __init__(self, id, name, date, interval):
		self.id = id
		self.name = name
		self.lastEditDate = date
		self.wateringInterval = interval
