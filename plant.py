
class Plant:
	__slots__ = ['id', 'name', 'lastEditDate', 'wateringInterval']

	def __init__(self, id, name, date, interval):
		self.id = id
		self.name = name
		self.lastEditDate = date
		self.wateringInterval = interval

	def toString(self):
		pattern = '{: <2}: {: <20} - {: <10} - {: <3}'
		return pattern.format(self.id, self.name, self.lastEditDate.isoformat(), self.wateringInterval)
