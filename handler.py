import json
import os
import sys
import datetime

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), './vendored'))

import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from sheet import Schedule

TOKEN = os.environ['TELEGRAM_TOKEN']
BASE_URL = 'https://api.telegram.org/bot{}'.format(TOKEN)


def assertKey(obj, key):
    if key not in obj:
        raise ValueError('Object is missing field \'%s\'' % key)

def sendMessage(chatId, text):
    data = {'text': text.encode('utf8'), 'chat_id': chatId}
    url = BASE_URL + '/sendMessage'
    requests.post(url, data)

def handleStart(chatId):
    reply = 'Hi!'
    sendMessage(chatId, reply)

def handleWater(chatId, schedule):
    today = datetime.date.today()
    plants = schedule.getPlantsToWater(today)
    if not plants:
        reply = 'Nothing to water today'
    else:
	    reply = 'Plants to water today:\n'
	    for plant in plants:
	        reply += plant['Plant'] + '\n'
    sendMessage(chatId, reply)

def handleAdd(chatId, message, schedule):
    commandArgs = message.split()
    if len(commandArgs) != 3:
        sendMessage(chatId, 'usage: /add <plant name> <interval in days>')
        return
    name = commandArgs[1]
    interval = int(commandArgs[2])
    schedule.addPlant(name, interval)
    sendMessage(chatId, 'Plant added!')



def handleUpdate(event, context):
    assertKey(event, 'body')
    data = json.loads(event['body'])

    assertKey(data, 'message')
    assertKey(data['message'], 'text')
    assertKey(data['message'], 'chat')
    assertKey(data['message']['chat'], 'id')
    message = str(data['message']['text'])
    chatId = data['message']['chat']['id']

    if message.startswith('/start'):
        handleStart(chatId)
    else:
        try:
            schedule = Schedule()
            if message.startswith('/water'):
                handleWater(chatId, schedule)
            elif message.startswith('/add'):
                handleAdd(chatId, message, schedule)
        except Exception as e:
            print(e)
            sendMessage(chatId, str(e))

    return {'statusCode': 200}


def handleNotify(event, context):
    chatId = 308999249
    schedule = Schedule()
    handleWater(chatId, schedule)

    return {'statusCode': 200}