import telegram
from telethon import TelegramClient


######## TELEGRAM #######
api_id = 20692913
api_hash = '678f824b2a57342c53810dcbba19dfcb'

client = TelegramClient('new', api_id, api_hash)
bot_token = '6096429155:AAGZ0WZ6A1GWJS704JLQ18n7bZCSt8rlIMg'
###########################


async def connectToTelegram():
    await client.start()

    print('connected to Telegram')


def dissconecttelegram():
    client.disconnect()

    print('disconnected to Telegram')


async def getinputentity():
    users = await client.get_dialogs(limit=2)
    first = users[1]
    entity = await client.get_input_entity(first.entity)
    return entity


async def sendmsgto(entity, msg):
    await client.send_message(entity, msg)