import json
import os
import sys
import datetime
from botocore.vendored import requests

from schedule import Schedule


TOKEN = os.environ['TELEGRAM_TOKEN']
BASE_URL = 'https://api.telegram.org/bot{}'.format(TOKEN)


def assertKey(obj, key):
    if key not in obj:
        raise ValueError('Object is missing field \'%s\'' % key)

def escapeTgMarkdown(text):
    return text.replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("`", "\\`")

def sendMessage(chatId, text, parseMode=None):
    data = {
        'text': text.encode('utf8'),
        'chat_id': chatId
    }
    if parseMode:
        data['parse_mode'] = parseMode
    url = BASE_URL + '/sendMessage'
    result = requests.post(url, data)
    #TODO: handle result


def start(chatId):
    reply = 'Hi!'
    sendMessage(chatId, reply)

def water(chatId, schedule):
    today = datetime.date.today()
    plants = schedule.getPlantsToWater(today)
    if not plants:
        reply = 'Nothing to water today'
    else:
	    reply = 'Plants to water today:\n'
	    for plant in plants:
	        reply += plant.name + '\n'
    sendMessage(chatId, reply)

def add(chatId, message, schedule):
    commandArgs = message.split()
    if len(commandArgs) != 3:
        sendMessage(chatId, 'usage: /add <plant name> <interval in days>')
        return
    name = commandArgs[1]
    interval = int(commandArgs[2])
    schedule.addPlant(name, interval)
    sendMessage(chatId, 'Plant added!')

def remove(chatId, message, schedule):
    commandArgs = message.split()
    if len(commandArgs) != 2:
        sendMessage(chatId, 'usage: /remove <plant id>')
        return
    id = int(commandArgs[1])
    schedule.removePlantById(id)
    sendMessage(chatId, 'Plant with id={} has been removed!'.format(id))


def listAll(chatId, schedule):
    plants = schedule.getAllPlants()
    if not plants:
        reply = 'No plants'
    else:
        parseMode = 'Markdown'
        reply = escapeTgMarkdown('Plants (id: name - next watering date - interval):\n')
        reply += '```\n'
        for plant in plants:
            reply += escapeTgMarkdown(plant.toString() + '\n')
        reply += '```'
    sendMessage(chatId, reply, parseMode)

def setInterval(chatId, message, schedule):
    commandArgs = message.split()
    if len(commandArgs) != 3:
        sendMessage(chatId, 'usage: /set_interval <plant id> <interval in days>')
        return
    id = int(commandArgs[1])
    interval = int(commandArgs[2])
    try:
        schedule.setInterval(id, interval)
        sendMessage(chatId, 'Interval is set')
    except IndexError as e:
        sendMessage(chatId, str(e))



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
        start(chatId)
    else:
        try:
            schedule = Schedule()
            if message.startswith('/water'):
                water(chatId, schedule)
            elif message.startswith('/add'):
                add(chatId, message, schedule)
            elif message.startswith('/remove'):
                remove(chatId, message, schedule)
            elif message.startswith('/list'):
                listAll(chatId, schedule)
            elif message.startswith('/set_interval'):
                setInterval(chatId, message, schedule)
        except Exception as e:
            print(e)
            sendMessage(chatId, str(e))

    return {'statusCode': 200}


def handleNotify(event, context):
    chatId = 308999249
    schedule = Schedule()
    water(chatId, schedule)

    return {'statusCode': 200}