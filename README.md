# discord-bot
A bot for [Discord](https://discordapp.com/) written in Python with [discord.py](https://github.com/Rapptz/discord.py)!

## Functionality
As a TeamSpeak user, I can not imagine using something that doesn't let users create temporary Voice Channels. To do that in Discord, I not only have to trust my users, but also give them permissions for stuff they don't need (ie, permissions to edit ALL channels, as well as text channels).
As such, the main features of my bot are:
* Let's users create their own Voice channels and let's them set a client limit, or even make them whitelist-only, so they get to choose who joins their channel.
* Let's users delete only their own channels
* Let's users edit their channel's Name, User limit, or whitelist other users if it's a private channel.
* Saves a database of user-created channels locally, so even if the bot restarts it will still remember the owner of each channel etc.
* Tells you where it's High Noon at. Cool little feature I guess.

### Add to Discord
To add my bot to discord simply use the following [link](https://discordapp.com/oauth2/authorize?client_id=190034775170351104&scope=bot&permissions=0x0000010)
