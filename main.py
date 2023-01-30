import config
import discord
import googletrans
from googletrans import Translator


langs = googletrans.LANGUAGES.keys()
BotID = config.secret['cl_id']
prefix = config.secret['prefix']
client = discord.Client(intents=discord.Intents().all())
tr = Translator()


class IDError(Exception):
    def __init__(self):
        super(IDError, self).__init__()


@client.event
async def on_ready():
    print('Авторизован как: ' + str(client.user) +'.\nЧтобы пригласить бота на сервер используйте ссылку: \nhttps://discordapp.com/oauth2/authorize?&client_id=' + config.secret['cl_id'] + '&scope=bot&permissions=' + str(config.secret['perms']))


@client.event
async def on_message(message: discord.Message):
    msg_text: str = message.content

    try:
        if message.author.id == 1031558752173826168:
            raise IDError
        else:
            if msg_text.startswith('.tr_mode'):
                command = msg_text.split(' ')
                try:
                    lang = command[1]
                    if lang in langs:
                        await message.channel.send(f'Переводчик включён для языка: {lang}')
                    else:
                        await message.channel.send(f'Язык {lang} недоступен для перевода!')
                except IndexError:
                    await message.channel.send('Переводчик отключен!')
            else:
                if lang:
                    translated = tr.translate(msg_text, dest=lang)
                    if translated.src != lang:
                        await message.channel.send(translated.text)

    except IDError as ex:
        await message.channel.send(ex)


client.run(config.secret['token'])
