from datetime import datetime
import pytz
from pytz import timezone as timezone
import discord
import asyncio
import random

tzs = []
banned_tzs = ['CET','CST6DT','EET','EST','EST5EDT','GMT','Greenwhich','UTC','Zulu','Universal','GB','HST','MET','MST','MST7MDT','NZ','PRC','PST8PDT','ROC','ROK','UCT','WET','W-SU']

async def where(message, client):
    while True:
        await client.send_typing(message.channel)
        for tz in pytz.all_timezones:
            h_tz = datetime.now(timezone(tz)).hour
            if h_tz == 12:
                tzs.append(tz)

        if not tzs:
            await client.send_message(message.channel, "It isn't Hign Noon anywhere somehow?!")
            break
        else:
            for tmzn in tzs:
                if any(tmz in tmzn for tmz in banned_tzs):
                    tzs.remove(tmzn)

            if not tzs:
                await client.send_message(message.channel, "It's High Noon somewhere... we just can't really describe where...")
                break

            tmp1 = random.choice(tzs)
            loc = 0
            if '/' in tmp1:
                tmp1 = tmp1.split("/")
                tmp2 = tmp1[1].split("_")
                loc = " ".join(tmp2)
            else:
                loc = tmp1

            msg = "It's High Noon in %s" % loc
            await client.send_message(message.channel, msg)
            break
