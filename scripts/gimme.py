import discord
import pickle
import re
import os
import datetime
import json
from jsonrpcclient import request
import requests

'''
moved bot.py from henistein's repo to scripts/faucet.py  
TODO: Refactor this script to comply with flow of imgs/diagram.png
'''

# insert the allowed channels
allowed_channels = ['test']

cooldown_list = []

def allow_message(word, cooldown_list):
  for i in cooldown_list:
    if word in i:
      if datetime.datetime.now() > i[1]:
        cooldown_list.remove(i)
        return True
      else:
        return False
  return True

# IMPORTANT: this was the on_message event, has been renamed to run to comply with repo's program flow
async def run(client, message):
  if message.author == client.user:
    return

  # Check if the address is on message
  if message.content:
    if message.channel.name in allowed_channels:
      message_words = message.content.split()
      for word in message_words:
        if re.search("^0x([A-Fa-f0-9]{40})$", word):
          url = 'https://cethswap.com/faucet/?user=' + str(message.author.id) + '&address=' + message.content
          r = requests.get(url)

          grantedCth = r.status_code == 200
          print(r.status_code)

          # Using JSON-RPC to retrieve balance info from https://cheapeth.org/rpc
          blockNum = request("https://node.cheapeth.org/rpc", "eth_blockNumber").data.result
          bal = request("https://node.cheapeth.org/rpc", "eth_getBalance", word, blockNum).data.result
          count = request("https://node.cheapeth.org/rpc", "eth_getTransactionCount", word, blockNum).data.result
          bal = str(round(float.fromhex(bal)/(1e+18), 10))
          count = str(int(count, 16))
          print(bal)
          s = ('**'+message.author.name+'**' + ': ' + '<https://explore.cheapswap.io/account/' 
              + word + '>' + '\n**Balance:** ' + bal + ' cTH' + '\n**Transactions**: ' + count)

          if(grantedCth):
            s += '\n**Faucet grants you 0.1 CTH: :droplet:**\n<https://cethswap.com/?cth_address=' + word + '&type=faucet>'


          cooldown = (datetime.datetime.now() + datetime.timedelta(seconds=60))
          if allow_message(word, cooldown_list):
            cooldown_list.append((word, cooldown))
            await message.channel.send(s)
