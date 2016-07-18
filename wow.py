import discord
import asyncio
import pickle

import checks

classes = [
    'Mage',
    'Paladin',
    'Monk',
    'Warlock',
    'Death Knight',
    'Warrior',
    'Rogue',
    'Hunter',
    'Demon Hunter',
    'Shaman',
    'Priest'
]

wow_server_ids = [
    '203875404224659456'
]

def get_class(message):
    for role in message.author.roles:
        if role.name in classes:
            return role


async def addwowsv(message, client):
    await client.send_typing(message.channel)
    if checks.has_admin(message):
        if not message.server.id in wow_server_ids:
            wow_server_ids.append(message.server.id)
            await client.send_message(message.channel, 'Successfully added the WoW server! Appropriate groups for the classes will be created!')
        else:
            await client.send_message(message.channel, 'It is already a WoW server, it seems.')
    else:
        await client.send_message(message.channel, 'You must have the "Administrator" permission to classify this server as a WoW server.')

async def setclass(message, client):
    await client.send_typing(message.channel)
    if message.server.id in wow_server_ids:
        ex_class = get_class(message)
        if ex_class != None:
            await client.remove_roles(message.author, ex_class)

        parse = message.content.split(' ', 1)

        await asyncio.sleep(.02)

        try:
            cname = parse[1]
        except IndexError:
            await client.send_message(message.channel, 'Please specify a class.')

        if cname.title() in classes:
            role = discord.utils.get(message.server.roles, name=cname.title())
            if role != None:
                await client.add_roles(message.author, role)
                await client.send_message(message.channel, 'Successfully set you as a {}'.format(role.name))
            else:
                await client.send_message(message.channel, "Doesn't seem to be a Role for this class. Try contacting server admins so they can add it.")
        else:
            await client.send_message(message.channel, "This doesn't seem to be a class... (you have to type in the class name fully, by the way.)")
    else:
        await client.send_message(message.channel, "This isn't classified as a WoW server. Use `$addwowsv` if you are an admin.")
