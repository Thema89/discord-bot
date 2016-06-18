import discord
import asyncio
import gc

class Command:
    def __init__(self, cdesc, cname, args, adv):
        self.desc = cdesc
        self.name = cname
        self.args = args
        self.adv = adv

cchannel = Command(
    cdesc='Creates a channel with the given `name`. If `current` is passed in as the name, it will fetch the current game you are playing. `type` can be an intiger which will indicate the client limit in the channel. Can also be either `owlobby` or `cslobby` for 6 and 5 player limits respectively.',
    cname='cchannel',
    args='name;type',
    adv = 'To use spaces in the channel name, simply use quotations, so you would type "Name". The text inside the quotations is literally interpreted, whilst inputting the channel name without quotations will turn it from `this` to `This`. Meanwhile, typing `"This"` would return `This`'
)
dchannel = Command(
    cdesc='Deletes the channel with the *exact* name (if you have the permission that is.)',
    cname='dchannel',
    args='name',
    adv = 'null'
)
echannel = Command(
    cdesc='Edits a channel.',
    cname='echannel',
    args='name',
    adv='The valid edit commands are the following:\n `#name <name>` - Replaces the current name with the <name>\n `#limit <limit>` - Replaces the user limit with <limit>'
)
highnoon = Command(
    cdesc="It's High Noon somewhere in the world. This command tells you where.",
    cname='highnoon',
    args='null',
    adv='null'
)

cmds = []

for obj in gc.get_objects():
    if isinstance(obj, Command):
        cmds.append(obj)

def get_args(cmd):
    args = cmd.args.split(';')
    args_str = ''
    for arg in args:
        args_str += '<{}> '.format(arg)

    return args_str

def get_cmd(cmnd):
    for cmd in cmds:
        if cmd.name == cmnd:
            return cmd

async def print_all(message, client):
    msg = "**The following commands are available**:\n"
    for cmd in cmds:
        args = get_args(cmd)

        msg += '\n`${0} {1}` - {2}'.format(cmd.name, args, cmd.desc)

    await client.send_message(message.channel, msg)

async def print_spec(message, client, cmd):
    if cmd.args != 'null':
        args = get_args(cmd)
    else:
        args = ''

    msg = "**{0}**\n*Syntax*: `${0} {1}`\n*Description*: {2}".format(cmd.name, args, cmd.desc)

    if cmd.adv != 'null':
        msg += '\n*More*:\n {}'.format(cmd.adv)

    await client.send_message(message.channel, msg)

async def print_help(message, client):
    while True:
        await client.send_typing(message.channel)
        parse = message.content.split()
        try:
            spec = parse[1]
        except IndexError:
            await print_all(message, client)
            break

        if any(spec == o.name for o in cmds):
            cmd = get_cmd(spec)
        else:
            await client.send_message(message.channel, 'Command not found.')
            break

        await print_spec(message, client, cmd)
        break
