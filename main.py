import config
import discord
import data_objects
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
    print('Авторизован как: ' +str(client.user) +'.\nЧтобы пригласить бота на сервер используйте ссылку: \nhttps://discordapp.com/oauth2/authorize?&client_id=' +config.secret['cl_id'] +'&scope=bot&permissions=' +str(config.secret['perms']))


@client.event
async def on_message(message: discord.Message):
    msg_text: str = message.content
    try:
        if message.author.id == 1031558752173826168:
            raise IDError
        else:
            writer: data_objects.User = data_objects.User(message.author.id)
            if msg_text.startswith('.tr_mode'):
                command = msg_text.split(' ')
                try:
                    lang = command[1]
                    if lang in langs:
                        await message.channel.send(f'Переводчик включён для языка: {lang}')
                        writer.update({'tr_lang': lang})
                    else:
                        await message.channel.send(f'Язык {lang} недоступен для перевода!')
                except IndexError:
                    await message.channel.send('Переводчик отключен!')
                    writer.update({'tr_lang': ''})
            else:

                w_lang = writer.user['tr_lang']

                if w_lang != '':
                    translated = tr.translate(msg_text, dest=writer.user['tr_lang'])
                    if translated.src != writer.user['tr_lang']:
                        await message.channel.send(translated.text)

    except IDError:
        pass


client.run(config.secret['token'])