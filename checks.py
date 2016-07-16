import discord

def has_msg(message):
    for role in message.author.roles:
        if role.permissions.manage_messages:
            return True
            break

def has_move(message):
    for role in message.author.roles:
        if role.permissions.move_members:
            return True
            break

def has_admin(message):
    for role in message.author.roles:
        if role.permissions.administrator:
            return True
            break
