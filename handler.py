import json
import os
import sys
import datetime

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), './vendored'))

import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials

TOKEN = os.environ['TELEGRAM_TOKEN']
BASE_URL = 'https://api.telegram.org/bot{}'.format(TOKEN)


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
        secret = {
            'type': 'service_account',
            'project_id': 'testspreadsheets',
            'private_key_id': 'e4e0686107152c3bf1b8138c54d2677060ae720d',
            'private_key': '-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC2RMnZkz6b57Rn\nMQOTCbPMd/TtWrfkcnDqamLAa4unkQOvb9/LzblHAnvYpMK9wrarx/eeB2l92j5/\njZigP/ij+2Cfy1EU27WulZQy1WV7dh7y+Hb34uuz0NV5Aik+oPVBIryCEA72YNeE\noldE3p87izaxeFFhlWV6wWzv/0EdwUzcmLS7X2p/rNxhNLBiYBF6wuH1SrD6Eozj\nLB/JvZBn9UtJS3Q8VdbFnaC1ml/5O8mdw+xWlOB7nFQZBGpzm96WtZ2EdpVhQiy/\nJpnUSarBONLyyAgYUM8HucEelt3HmJXdjTmtvBNpVRT9UjEUVx05JOkGnjhFuqDF\n+8ypDOWZAgMBAAECggEAAgT72AxquYs9C1YmkBzfyDyNgwo55p7ye5RrbO6cHOKN\nUAatK/rG6l+fi+hSbIwRXlCgQJjcLTvrbJoe5mqjCH0W5lpYNwMSraEkY9ZLsi0e\nPWqtlcRGwIaoMNeqaZJauUqnXEkNg2MSDDsIvL97M+uQUvHOdAZ12gD14ihZujjG\n4rOJJtwS8O4VmLmMSAtt4Hvpn2j9P6uHH2Y74UOO26hZsvqqR6bQ2p6sha9R49el\nBoxw6Zenim4Pb+gHGaxYCs0UlCPK4s6v5rcyh2XbRhBlJP9+GY6HWcZDVhsRalq1\nQBKUQAw9WhA7cYrj2l3la6V0XKLLe78HUe0kF0sZEQKBgQDoWqQ7w1v8M2gbfjfD\n89vP3dW4SB0X2jdMcnKgKOH8V29hcHLINr5Yo08OD4bYBDGaD92jxE82sZbu0q4D\nIE7OIWQgLsF60bxzRf1UwCkExNV+LbolnochRto0rSOBkmD6q2/osxcCHdQTAwyX\n3mTrqGmW6PEprBronk2JHYkZCQKBgQDI0U7SpKRxbOpE8TcuakzBnx2wl4Ag5AAq\nvV44XmDvFIxPWvGGJH6t+N8othXL2vA7NWtualJO7pt0iNnREMaTg5kDRcy3R+Iy\nbzX2u8OwdVfuhaJGwri+nQEtvWqJ73SmVaaRO1esOYm7Ji4Dl5q/Gg1rYUR7ZLEx\nDbzM+htcEQKBgAnIHxfg/pNceqqFosVeE8fpd+DdMFRbvG48dzTk47ai266HdF2X\naGYE4gQehTe83XW160fEsO0Fhuwg9HBvQMIOx89PCJgqEjvsG2EhAdkQjEhWlnqU\n9O1itTb4fwEqb2i+JOTv/Sz6on32Z+ZQ14DQQzm2LsjpVOysFWmLU8U5AoGBAIhD\nrs60NXlZxGVfoGf4bXj8tTK8uo6W554YvTRWpkPUl5jJRxYU8XivZQ3E8GlReK1U\nhD96GbvBoO6kZdi9H2G9bDiSRmUfe9dpKx7vLcww86fAOer1+lItSz10SDSsrWSo\nvcvSjp0otdKuB48ccj62OODiMYvhOXLltXUJSUNhAoGAN+VABx+nmxBb80x5qx8p\nhS3BDraxyzTYa+l+WHRAQ7eCrLSzg51qoHfO3wT6mZLpfnb324isoK/UvIjvlZB4\nalt4dVTKbl+R9aHrFuVXyJ01Y8tnnT6VALzK7RbrToCEm5ecJ1L63Qe81QNSwNCM\nQMhAzriiJK3Hxq1X0k7B7LQ=\n-----END PRIVATE KEY-----\n',
            'client_email': 'account@testspreadsheets.iam.gserviceaccount.com',
            'client_id': '110698387299297508980',
            'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
            'token_uri': 'https://oauth2.googleapis.com/token',
            'auth_provider_x509_cert_url': 'https://www.googleapis.com/oauth2/v1/certs',
            'client_x509_cert_url': 'https://www.googleapis.com/robot/v1/metadata/x509/account%40testspreadsheets.iam.gserviceaccount.com'
        }
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

def assertKey(obj, key):
    if key not in obj:
        raise ValueError('Object is missing field \'%s\'' % key)

def sendMessage(chatId, text):
    data = {'text': text.encode('utf8'), 'chat_id': chatId}
    url = BASE_URL + '/sendMessage'
    requests.post(url, data)

def handleStart(data):
    reply = 'Hi!'
    chatId = data['message']['chat']['id']
    sendMessage(chatId, reply)

def handleWater(data, schedule):
    chatId = data['message']['chat']['id']
    today = datetime.date.today()
    plants = schedule.getPlantsToWater(today)
    if not plants:
        reply = 'Nothing to water today'
    else:
	    reply = 'Plants to water today:\n'
	    for plant in plants:
	        reply += plant['Plant'] + '\n'
    sendMessage(chatId, reply)

def handleAdd(data, schedule):
    chatId = data['message']['chat']['id']
    message = str(data['message']['text'])
    commandArgs = message.split()
    if len(commandArgs) != 3:
        sendMessage(chatId, 'usage: /add <plant name> <interval in days>')
        return
    name = commandArgs[1]
    interval = int(commandArgs[2])
    schedule.addPlant(name, interval)
    sendMessage(chatId, 'Plant added!')



def handle(event, context):
    assertKey(event, 'body')
    data = json.loads(event['body'])

    assertKey(data, 'message')
    assertKey(data['message'], 'text')
    assertKey(data['message'], 'chat')
    assertKey(data['message']['chat'], 'id')
    message = str(data['message']['text'])
    chatId = data['message']['chat']['id']

    if message.startswith('/start'):
        handleStart(data)
    else:
        try:
            schedule = Schedule()
            if message.startswith('/water'):
                handleWater(data, schedule)
            elif message.startswith('/add'):
                handleAdd(data, schedule)
        except Exception as e:
            print(e)
            sendMessage(chatId, str(e))

    return {'statusCode': 200}