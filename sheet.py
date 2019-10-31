import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), './vendored'))

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
