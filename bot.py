import discord
import re
import os
import datetime
import json
from jsonrpcclient import request
import client as cb
import requests

TOKEN = os.getenv('TOKEN')

client = discord.Client()

# insert the allowed channels
allowed_channels = ['test']

cooldown_list = []
meme_list = []

global min_approval 
min_approval = 10

def allow_message(word, cooldow_list):
  for i in cooldown_list:
    if word in i:
      if datetime.datetime.now() > i[1]:
        cooldown_list.remove(i)
        return True
      else:
        return False
  return True

def update_list(meme_list):
  for i in meme_list:
    i[3] = 0
    for j in i[0].reactions:
      i[3] += j.count
    if datetime.datetime.now() > i[1]:
      meme_list.remove(i)
  return meme_list

def update_json(meme_list):
  temp = []
  with open("approval.json", "w") as outfile:
    for i in meme_list:
      dictionary = {}
      dictionary["uuid"] = i[2]
      dictionary["reactions"] = i[3]
      if i[3] >= min_approval:
        dictionary["approval"] = True
      else:
        dictionary["approval"] = False
      dictionary["expired_time"] = i[1].__str__()

      temp.append(dictionary)
      json_object = json.dumps(temp)
    outfile.write(json_object)

def approved_users(meme_list):
  for i in meme_list:
    if i[3] >= min_approval:
      info = f'{i[2]} {i[3]}'
      cb.sendInfo(info)
      print(info)

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
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

  # Check if an attachment is on the message
  if message.content:
    if message.attachments:
      message_words = message.content.split()
      for word in message_words:
        if re.search("^[- a-fA-F0-9]{36}$", word):
          meme_time = (datetime.datetime.now() + datetime.timedelta(minutes=60))
          meme_list.append([message, meme_time, word, 0])

@client.event
async def on_reaction_add(user, reaction):
  update_list(meme_list)
  update_json(meme_list)
  #approved_users(meme_list)

@client.event
async def on_raw_reaction_remove(payload):
  update_list(meme_list)
  update_json(meme_list)
  #approved_users(meme_list)
    
client.run(TOKEN)
