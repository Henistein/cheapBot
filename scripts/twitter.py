import pickle
import re
import os
import datetime
import json
from jsonrpcclient import request
import requests
from typing import Dict, List, Tuple

import discord
import requests                 
from discord.ext import commands

import config
"""
Twitter bot

Read discord messages, send request to smart contract
"""

# insert the allowed channels

class Twitter(commands.Cog):
  bot: commands.Bot
  allowed_channels: List[str]

  def __init__(self, bot):
    self.bot = bot
    self.allowed_channels = config.allowed_twitter_channels
  
  def allow_message(self, word, cooldown_list):
      for i in cooldown_list:
          if word in i:
              if datetime.datetime.now() > i[1]:
                  cooldown_list.remove(i)
                  return True
              else:
                  return False
      return True


  def extract_address(self, message):
      p = re.compile('(0x[a-fA-F0-9]{40})')
      result = p.search(message)
      if result is None:
          return None
      return result.group(1)

  @commands.command()
  async def twitter(self, ctx):

    if ctx.author.bot:
      return        

    if not ctx.message.content:
      return                 

    # Check if the address is on message
    if ctx.message.content:
        if ctx.channel.name in self.allowed_channels:
            message = ctx.message

            if len(message.content.split(' ')) < 4:
                await message.channel.send(
                    "Wrong format %s. Use: $cheap twitter <twitterID> <cth address>" % message.author.mention)
                return

            # check that 3rd is eth addr
            address = self.extract_address((message.content))

            # not adding a address is a no go
            if address is None:
                await message.channel.send(
                    "Wrong format %s. Use: $cheap twitter <twitterID> <cth address>" % message.author.mention)
                return

            user = message.content.split(' ')[2]

            url = 'http://157.245.4.45:5000/send-cth?user=' + str(user) + '&address=' + address
            r = requests.get(url)

            success = r.status_code == 200
            if not success:
                await message.channel.send(
                    "Invalid input %s. Use: $cheap twitter <twitterID> <cth address>" % message.author.mention)
                return

            # send money to the account and notify admins
            if 'tx' not in r.json():
                await message.channel.send(
                    "Invalid input %s. Use: $cheap twitter <twitterID> <cth address>" % message.author.mention)
                return

            tx_hash = r.json()['tx']

            await message.channel.send(
                'Request sent to contract! %s, userID: %s, tx: %s' % (message.author.mention, user, tx_hash))
     
