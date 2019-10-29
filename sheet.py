import json
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), './vendored'))

import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials


class GoogleSheet:
    def __init__(self, secret, sheetName):
        scope = ['https://www.googleapis.com/auth/drive']
        self.creds = ServiceAccountCredentials.from_json_keyfile_dict(secret, scope)
        self.client = gspread.authorize(self.creds)
        self.sheet = self.client.open(sheetName).get_worksheet(0)

    def deleteRow(self, index):
        self.sheet.delete_row(index)

    def getAllRecords(self):
        return self.sheet.get_all_records()

    def getCell(self, x, y):
        return self.sheet.cell(1, 1).value

    def getColumn(self, index):
        return self.sheet.col_values(index)

    def getRow(self, index):
        return self.sheet.row_values(index)

    def insertRow(self, index, values):
        self.sheet.insert_row(values, index)

    def setCell(self, x, y, value):
        return self.sheet.update_cell(x, y, value)
        

class Schedule:
    def __init__(self):
        secret = os.environ['GOOGLE_SECRET']
        secret = json.loads(secret)
        self.sheet = GoogleSheet(secret, 'test')

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
        return self.sheet.getAllRecords()

    def getPlantsToWater(self, targetDate):
        result = []
        if not isinstance(targetDate, datetime.date):
            raise TypeError('targetDate must be a datetime.date')
        plants = self.getAllPlants()
        for plant in plants:
            wateringDate = datetime.datetime.strptime(plant['Start'], '%Y-%m-%d').date()
            interval = int(plant['Interval(days)'])
            while wateringDate < targetDate:
                wateringDate = wateringDate + datetime.timedelta(days=interval)
            if wateringDate == targetDate:
                result.append(plant)
        return result


    def initColumns(self):
        self.sheet.setCell(1, 1, 'N')
        self.sheet.setCell(1, 2, 'Plant')
        self.sheet.setCell(1, 3, 'Start')
        self.sheet.setCell(1, 4, 'Interval(days)')

    def removePlantById(self, id):
        self.sheet.deleteRow(Schedule.getRowIndexById(id))