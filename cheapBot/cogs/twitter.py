import datetime
import re
from typing import List

import requests
from discord.ext import commands

from .. import config

"""
Twitter bot

Read discord messages, send request to smart contract
"""


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
  async def twitter(self, ctx: commands.Context):
    """
    Tweet about CheapEth and get rewarded (\"$cheap help twitter\")

    * Tweet and include any of these keywords [\"cheapeth\", \"cheapethereum\", \"#cth\", \"$CTH\"]
    * Type \"$cheap twitter <twitterID> <your cth arrd>\"
    * Get your twitter ID from: https://tweeterid.com/
    * <1000 followers = 1cth
    * 1000-2000 followers = 2cth
    * 2000+ followers = 3cth
    * Check balance before and after as transaction not on explorer
    * 1 reward per user
    * Min account age 30 days, min followers 10
    """
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

        url = 'https://cheapeth-twitterbot.cheaplife.repl.co/send-cth2?user=' + str(user) + '&address=' + address + '&discordID=' + str(ctx.author.id)
        r = requests.get(url)

        success = r.status_code == 200
        if not success:
          await message.channel.send(
              "Invalid input %s. Use: $cheap help twitter" % message.author.mention)
          return

        r_json = r.json()
        if 'result' in r_json:
            if r_json['result'] == 'cooldown':
                await message.channel.send(
                    "Too many attempts %s" % message.author.mention)
                return

        # send money to the account and notify admins
        if 'tx' not in r_json:
          await message.channel.send(
              "Invalid input %s. Use: $cheap twitter <twitterID> <cth address>" % message.author.mention)
          return

        tx_hash = r_json['tx']

        await message.channel.send(
          'Request sent to contract! %s, userID: %s, tx: %s' % (message.author.mention, user, tx_hash))
