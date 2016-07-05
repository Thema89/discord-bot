import discord
import asyncio
import pickle

perm_channels = ['Discussion: Greek','Discussion: English','Sicrit Club']
admin_ids = ['93043948775305216']

class VoiceChannel:
    def __init__(self):
        self.owner = ""
        self.chanid = 0

    def setOwner(self, user):
        self.owner = user

    def setID(self, cid):
        self.chanid = cid

with open('voice_channels', 'rb') as f:
    try:
        voice_channels = pickle.load(f)
    except EOFError:
        voice_channels = []

def get_voice_channel(cid):
    for channel in voice_channels:
        if channel.chanid == cid:
            return channel

async def cchannel(message, client):
    while True:
        await client.send_typing(message.channel)

        if message.channel.is_private:
            await client.send_message(message.channel, 'Please call this command from a server channel.')
            break

        if '"' in message.content:
            parse = message.content.split('"')
            for i in range(0, len(parse)):
                parse[i] = parse[i].strip()
        else:
            parse = message.content.split()

        try:
            game = parse[1]
        except IndexError:
            await client.send_message(message.channel, 'Please specify a name for the channel (in lowercase.)')
            break

        try:
            lim = parse[2]
        except IndexError:
            lim = 'null'

        if not '"' in message.content:
            game = game.title()

        if game.lower() == 'current' and str(message.author.game) == 'None':
            await client.send_message(message.channel, 'Please launch a game then call the command again. Alternatively, provide a name.')
            break
        elif game.lower() == 'Current'.lower():
            game = str(message.author.game)

        if game == 'Counter-Strike: Global Offensive':
            game = 'CS:GO'
        elif game == 'Grand Theft Auto V':
            game = 'GTA V'

        exist = sum(c.name.startswith(game) for c in message.server.channels)
        num = str(exist + 1)
        #pos = sum(c.type == discord.ChannelType.voice for c in message.server.channels)

        if exist != 0:
            game += ' #%s' % num

        if str(lim).isdigit():
            limit = int(lim)
        else:
            limit = 0

        chanlim = sum(c.owner == message.author for c in voice_channels)

        if chanlim < 4:
            pass
        else:
            await client.send_message(message.channel, 'You can only create up to 4 channels, you can use $dchannel to delete some though.')
            break

        everyone = discord.PermissionOverwrite(connect=False)
        access = discord.PermissionOverwrite(connect=True)

        if str(lim) == 'private' or str(lim) == 'party':
            channel = await client.create_channel(message.server, game, (message.server.default_role, everyone), (message.author, access), type=discord.ChannelType.voice)
            if str(lim) == 'party':
                try:
                    members = parse[3].split(';')
                except IndexError:
                    await client.delete_channel(channel)
                    await client.send_message(message.channel, 'No party members specified.')
                    break

                for member in members:
                    person = discord.utils.find(lambda o: o.display_name.lower() == member.lower(), message.channel.server.members)
                    await client.edit_channel_permissions(channel, person, access)
        elif str(lim) == 'public':
            channel = await client.create_channel(message.server, game, type=discord.ChannelType.voice)
        else:
            channel = await client.create_channel(message.server, game, (message.server.default_role, everyone), type=discord.ChannelType.voice)
            for role in message.server.roles:
                if role != message.server.default_role and not role.permissions.administrator:
                    await client.edit_channel_permissions(channel, role, access)

        listing = VoiceChannel()
        listing.setOwner(message.author)
        listing.setID(channel.id)
        voice_channels.append(listing)

        with open('voice_channels', 'wb') as f:
            pickle.dump(voice_channels, f)

        await client.edit_channel(channel, bitrate=96000, user_limit=limit)
        #await client.move_channel(channel, pos)
        await client.send_message(message.channel, 'Successfully created the voice channel')
        break

async def dchannel(message, client):
    while True:
        await client.send_typing(message.channel)

        if message.channel.is_private:
            await client.send_message(message.channel, 'Please call this command from a server channel.')
            break

        if '"' in message.content:
            parse = message.content.split('"')
        else:
            parse = message.content.split(' ', 1)

        try:
            name = parse[1]
        except IndexError:
            name = 'null'
            await client.send_message(message.channel, 'No channel specified')
            break

        if name in perm_channels:
            await client.send_message(message.channel, "You don't have permission to delete that channel.")
            break

        try:
            chan = discord.utils.get(message.server.channels, name=name, type=discord.ChannelType.voice)
            channel = get_voice_channel(chan.id)

            if message.author == channel.owner or message.author.id in admin_ids:
                await client.delete_channel(chan)
                voice_channels.remove(channel)
                with open('voice_channels', 'wb') as f:
                    f.truncate()
                    pickle.dump(voice_channels, f)

                await client.send_message(message.channel, 'Successfully deleted the voice channel')
                break
            else:
                await client.send_message(message.channel, "You can only delete your channels.")
                break

        except AttributeError:
            await client.send_message(message.channel, 'Channel not found')
            break

async def echannel(message, client):
    while True:
        await client.send_typing(message.channel)

        if message.channel.is_private:
            await client.send_message(message.channel, 'Please call this command from a server channel.')
            break

        parse = message.content.split(' ', 1)
        try:
            name = parse[1]
        except IndexError:
            await client.send_message(message.channel, 'No channel specified')
            break

        if name in perm_channels:
            await client.send_message(message.channel, "You don't have permission to edit that channel.")
            break

        try:
            chan = discord.utils.get(message.server.channels, name=name, type=discord.ChannelType.voice)
            channel = get_voice_channel(chan.id)
            if message.author == channel.owner or message.author.id in admin_ids:
                await client.send_message(message.channel, "Now, enter an edit command... *(use `$help echannel` for more info)*:")
                await client.send_typing(message.channel)
                msg = await client.wait_for_message(author=message.author, channel=message.channel)

                if '"' in msg.content:
                    response = msg.content.split('"')
                    for i in range(0, len(response)):
                        response[i] = response[i].strip()
                else:
                    response = msg.content.split(' ', 1)

                success = 'Successfully edited the {0} to {1}'

                everyone = discord.PermissionOverwrite(connect=False)
                access = discord.PermissionOverwrite(connect=True)

                if response[0] == '#name':
                    try:
                        nname = response[1]
                        await client.edit_channel(chan, name=nname)
                        await client.send_message(message.channel, success.format('name',nname))
                        break
                    except IndexError:
                        await client.send_message(message.channel, 'No new name specified.')
                        break
                elif response[0] == '#limit':
                    try:
                        limit = int(response[1])
                        await client.edit_channel(chan, user_limit=limit)
                        await client.send_message(message.channel, success.format('limit',limit))
                        break
                    except IndexError:
                        await client.send_message(message.channel, 'No limit specified.')
                        break
                elif response[0] == '#setowner':
                    try:
                        owner = response[1].lower()
                        nowner = discord.utils.find(lambda o: o.display_name.lower() == owner, message.channel.server.members)
                        if str(nowner) == 'None':
                            await client.send_message(message.channel, 'No user found')
                            break

                        channel.setOwner(nowner)
                        await client.send_message(message.channel, success.format('owner',nowner))
                        break
                    except IndexError:
                        await client.send_message(message.channel, 'No new owner specified.')
                        break
                    except AttributeError:
                        await client.send_message(message.channel, 'No user found')
                        break
                elif response[0] == '#whitelist':
                    try:
                        arg = response[1].lower()
                        person = discord.utils.find(lambda o: o.display_name.lower() == arg, message.channel.server.members)
                        await client.edit_channel_permissions(chan, person, access)
                        await client.send_message(message.channel, 'Successfully added {} to the whitelist'.format(person))
                        break
                    except IndexError:
                        await client.send_message(message.channel, 'No user to whitelist.')
                elif response[0] == '#lock':
                    await client.edit_channel_permissions(chan, message.server.default_role, everyone)
                    await client.edit_channel_permissions(chan, message.author, access)
                    for role in message.server.roles:
                        if role != message.server.default_role:
                            await client.delete_channel_permissions(chan, role)
                    for user in chan.voice_members:
                        if user != message.author:
                            await client.edit_channel_permissions(chan, user, access)
                    await client.send_message(message.channel, 'Successfully converted channel to private')
                    break
                elif response[0] == '#unlock':
                    await client.delete_channel_permissions(chan, message.author)
                    for role in message.server.roles:
                        if role != message.server.default_role:
                            await client.edit_channel_permissions(chan, role, access)
                    for user in chan.voice_members:
                        if user != message.author:
                            await client.delete_channel_permissions(chan, user)
                    await client.send_message(message.channel, 'Successfully converted channel to semi-public')
                    break
                elif response[0].startswith('#'):
                    await client.send_message(message.channel, 'Invalid edit command.')
                    break
                else:
                    break
            else:
                await client.send_message(message.channel, "You can only edit your channels.")
                break
        except AttributeError:
            await client.send_message(message.channel, 'Channel not found')
            break
