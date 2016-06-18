#!python3
import discord
import asyncio
import logging

import mchan
import highnoon
import helpcmd

# Logging to a file
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client = discord.Client()

#with open('bot.png', 'rb') as fp:
#    avatar = fp.read()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    #await client.edit_profile(avatar=avatar)

@client.event
async def on_message(message):
    if message.content.startswith('$help'):
        await helpcmd.print_help(message, client)
    elif message.content.startswith('$cchannel'):
        await mchan.cchannel(message, client)
    elif message.content.startswith('$dchannel'):
        await mchan.dchannel(message, client)
    elif message.content.startswith('$echannel'):
        await mchan.echannel(message, client)
    elif message.content.startswith('$highnoon'):
        await highnoon.where(message, client)
    elif message.content.startswith('$'):
        await client.send_message(message.channel, 'No command found, type `$help` for commands.')

client.run('token here')
