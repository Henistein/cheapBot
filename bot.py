from scripts import * 
import discord
from discord.ext import commands
import os
import sys

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
      #Checks if script is present in scripts/
      if msg[1] in list(set([file.split('.')[0] for file in os.listdir('scripts/')][3:])):
        func = eval(f"{msg[1]}.run")
        await func(client=client, message=message)
    except ValueError as v:
      raise v

client.run(os.getenv('TOKEN'))
