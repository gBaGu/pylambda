import datetime


class Plant:
	__slots__ = ['id', 'name', 'countdownDate', 'wateringInterval']

	def __init__(self, id, name, date, interval):
		self.id = id
		self.name = name
		self.countdownDate = date
		self.wateringInterval = interval

	def nextWateringDate(self):
		today = datetime.date.today()
		deltaDays = (today - self.countdownDate).days
		daysToWater = self.wateringInterval - deltaDays % self.wateringInterval
		if daysToWater == self.wateringInterval:
			return today
		return today + datetime.timedelta(days=daysToWater)

	def toString(self):
		pattern = '{: <2}: {: <20} - {: <10} - {: <3}'
		wateringDate = self.nextWateringDate()
		wateringDateStr = wateringDate.isoformat()
		deltaDays = (wateringDate - datetime.date.today()).days
		if deltaDays == 0:
			wateringDateStr = 'today'
		elif deltaDays == 1:
			wateringDateStr = 'tomorrow'
		return pattern.format(self.id, self.name, wateringDateStr, self.wateringInterval)
