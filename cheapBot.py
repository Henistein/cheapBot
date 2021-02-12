import discord
import re
import os

TOKEN = os.getenv('TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content:
        aux = message.content.split()
        for i in aux:
            if re.search("^0x([A-Fa-f0-9]{40})$", i):
              s = 'https://expedition.dev/address/' + i + '?rpcUrl=https%3A%2F%2Fnode.cheapeth.org%2Frpc'
        await message.channel.send(s)

client.run(TOKEN)
