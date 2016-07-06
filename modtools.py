import discord
import asyncio

def is_admin(message):
    for role in message.author.roles:
        if role.permissions.manage_messages:
            return True
            break

async def purge(message, client):
    while True:
        await client.send_typing(message.channel)

        if not is_admin(message):
            await client.send_message(message.channel, 'You need the "Manage Messages" permission to call this command.')
            break

        parse = message.content.split()
        try:
            name = parse[1]
        except IndexError:
            await client.send_message(message.channel, 'No name specified')
            break

        user = discord.utils.find(lambda o: o.display_name.lower() == name, message.channel.server.members)

        def is_usr(message):
            return message.author == user

        try:
            param = int(parse[2])
        except IndexError:
            param = 100

        deleted = await client.purge_from(message.channel, limit=param, check=is_usr)

        await client.send_message(message.channel, 'Done deleting {0} messages by {1}.'.format(len(deleted),user.display_name))
        break
