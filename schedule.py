import json
import os
import sys
import datetime

from plant import Plant
from sheet import GoogleSheet
        

class Schedule:
    def __init__(self):
        secret = os.environ['GOOGLE_SECRET']
        secret = json.loads(secret)
        self.sheet = GoogleSheet(secret, 'test')
        self.columnNames = self.sheet.getRow(1)
        if not self.columnNames:
            self.initColumns()
        if len(self.columnNames) != 4:
            raise Exception('Database is inconsistent')

    @staticmethod
    def getRowIndexById(id):
        return id + 1


    def addPlant(self, name, interval):
        numbers = self.sheet.getColumn(1)
        if not numbers:
            self.initColumns()
        id = 1
        if len(numbers) > 1:
            id = int(numbers[-1]) + 1
        today = datetime.date.today()
        rowNum = Schedule.getRowIndexById(id)
        self.sheet.insertRow(rowNum, [id, name, today.isoformat(), interval])

    def getAllPlants(self):
        records = self.sheet.getAllRecords()
        plants = [
            Plant(int(record[self.columnNames[0]]), record[self.columnNames[1]], datetime.datetime.strptime(record[self.columnNames[2]], '%Y-%m-%d').date(), int(record[self.columnNames[3]]))
            for record in records
        ]
        return plants

    def getPlantsToWater(self, targetDate):
        result = []
        if not isinstance(targetDate, datetime.date):
            raise TypeError('targetDate must be a datetime.date')
        plants = self.getAllPlants()
        for plant in plants:
            wateringDate = plant.lastEditDate
            while wateringDate < targetDate:
                wateringDate = wateringDate + datetime.timedelta(days=plant.wateringInterval)
            if wateringDate == targetDate:
                result.append(plant)
        return result


    def initColumns(self):
        self.columnNames = ['N', 'Plant', 'Start', 'Interval(days)']
        for i in range(len(self.columnNames)):
            self.sheet.setCell(1, i + 1, self.columnNames[i])

    def removePlantById(self, id):
        self.sheet.deleteRow(Schedule.getRowIndexById(id))
