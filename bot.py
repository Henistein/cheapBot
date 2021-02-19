import os
import discord
from scripts import *


# bot stuff after here
PREFIX = '$cheap'
client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):

    msg = message.content.split(' ')
    if msg[0].lower() == PREFIX:
        if len(msg) < 2:
            return
        cmd = msg[1].lower()
        try:
            # Checks if script is present in scripts
            if cmd in list(set([file.split('.')[0] for file in os.listdir('scripts/')][3:])):
                func = eval(f"{cmd}.run")
                await func(client=client, message=message)
        except ValueError as v:
            raise v


client.run(os.getenv('TOKEN'))
