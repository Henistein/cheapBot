import discord
import re
import os
import datetime
from jsonrpcclient import request

TOKEN = os.getenv('TOKEN')

client = discord.Client()

# insert the allowed channels
allowed_channels = ['test']
cooldown_list = []

def allow_message(word, cooldow_list):
  for i in cooldown_list:
    if word in i:
      if datetime.datetime.now() > i[1]:
        cooldown_list.remove(i)
        return True
      else:
        return False
  return True

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content:
    if message.channel.name in allowed_channels:
      message_words = message.content.split()
      for word in message_words:
        if re.search("^0x([A-Fa-f0-9]{40})$", word):

          # Using JSON-RPC to retrieve balance info from https://cheapeth.org/rpc
          blockNum = request("https://node.cheapeth.org/rpc", "eth_blockNumber").data.result
          bal = request("https://node.cheapeth.org/rpc", "eth_getBalance", word, blockNum).data.result
          count = request("https://node.cheapeth.org/rpc", "eth_getTransactionCount", word, blockNum).data.result
          bal = str(round(float.fromhex(bal)/(1e+18), 10))
          count = str(int(count, 16))
          print(bal)
          s = ('**'+message.author.name+'**' + ': ' + '<https://explore.cheapswap.io/account/' 
              + word + '>' + '\n**Balance:** ' + bal + ' cTH' + '\n**Transactions**: ' + count) 


          cooldown = (datetime.datetime.now() + datetime.timedelta(seconds=60))
          if allow_message(word, cooldown_list):
            cooldown_list.append((word, cooldown))
            await message.channel.send(s)

client.run(TOKEN)
