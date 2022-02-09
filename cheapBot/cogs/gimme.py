import datetime
import re
import os
from typing import Dict, List

import discord
import requests
from discord.ext import commands
from web3 import Web3

from .. import config


class Gimme(commands.Cog):
  bot: commands.Bot
  allowed_channels: List[str]
  cooldowns: Dict[str, datetime.datetime]
  faucet_url: str

  def __init__(self, bot: commands.Bot):
    super().__init__()
    self.bot = bot
    self.allowed_channels = config.allowed_gimme_channels
    self.cooldowns = {}
    self.faucet_url = config.faucet_url
    self.w3 = Web3(Web3.HTTPProvider('https://node.cheapeth.org/rpc'))

  def not_on_cooldown(self, addr: str) -> bool:
    if addr in self.cooldowns:
      if datetime.datetime.now() > self.cooldowns[addr]:
        self.cooldowns.pop(addr)
        return True
      else:
        return False

    return True

  # IMPORTANT: this was the on_message event, has been renamed to run to comply with repo's
  # program flow
  @commands.command()
  async def gimme(self, ctx: commands.Context, addr: str):

    if ctx.author.bot:
      return

    # Check if the address is on message
    if not ctx.message.content:
      return

    if ctx.channel.name in self.allowed_channels:
      message: discord.Message = ctx.message

      if re.search('^0x([A-Fa-f0-9]{40})$', addr):
          url = f'{os.getenv("FAUCET_IP")}?address={addr}'
          print(url)
          r = requests.get(url)

          grantedCth = r.status_code == 200
          print(r.status_code)

          # Using Web3 to retrieve balance info from https://cheapeth.org/rpc
          bal = self.w3.eth.get_balance(addr)
          bal = str(round(bal / 1e+18, 10))
          count = self.w3.eth.getTransactionCount(addr)

          s = f'**{message.author.name}**: <https://explore.cheapswap.io/account/{addr}>'
          s += f'\n**Balance**: {bal} cTH'
          s += f'\n**Transactions**: {count}'

          if grantedCth:
            s += f'\n**Faucet will grant you 0.05 cTH**'
          else:
            s += f'\n**You have not been given any cTH. Try again later.**'

          cooldown = datetime.datetime.now() + datetime.timedelta(seconds=60)

          if self.not_on_cooldown(addr):
            self.cooldowns[addr] = cooldown
            await message.channel.send(s)
