from scripts import * 
import discord
from discord.ext import commands
import os
import sys
modulenames = set(sys.modules) & set(globals())
allmodules = [sys.modules[name] for name in modulenames]
print(allmodules)


# bot stuff after here

PREFIX = '$cheap'
client = discord.Client()

@client.event
async def on_ready():
		print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):

  msg = message.content.split(' ')
  if msg[0] == PREFIX:
    cmd = msg[1]
    try:
      func = eval(f"{msg[1]}.run")
      await func(client=client, message=message)
    except ValueError as v:
      raise v

client.run(os.getenv('TOKEN'))
