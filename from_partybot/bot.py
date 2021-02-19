from scripts import * 
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
load_dotenv()

# bot stuff after here

PREFIX = '$cheap'
client = discord.Client()

@client.event
async def on_ready():
		print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):

  msg = message.split(' ')
  if msg[0] == PREFIX:
    cmd = msg[1]
    try:
      eval(f"{msg[1]}.run({message})")
    except ValueError as v:
      raise v

client.run(os.getenv('TOKEN'))
