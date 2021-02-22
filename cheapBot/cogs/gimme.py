import datetime
import re
from typing import Dict, List

import discord
import requests
from discord.ext import commands
from jsonrpcclient import request  # type: ignore

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
          url = f'{self.faucet_url}{message.author.id}&address={addr}'
          r = requests.get(url)

          grantedCth = r.status_code == 200
          print(r.status_code)

          # Using JSON-RPC to retrieve balance info from https://cheapeth.org/rpc
          blockNum = request(config.rpc_url, 'eth_blockNumber').data.result
          bal = request(config.rpc_url, 'eth_getBalance', addr, blockNum).data.result
          count = request(config.rpc_url, 'eth_getTransactionCount', addr,
                          blockNum).data.result
          bal = str(round(float.fromhex(bal) / (1e+18), 10))
          count = str(int(count, 16))
          print(bal)

          s = f'**{message.author.name}**: <https://explore.cheapswap.io/account/{addr}>'
          s += f'\n**Balance**: {bal} cTH'
          s += f'\n**Transactions**: {count}'

          if grantedCth:
            s += f'\n**Faucet grants you 0.1 cTH: :droplet:**'
            s += f'\n<https://cethswap.com/?cth_address={addr}&type=faucet>'
          else:
            s += f'\n**You have not been given any cTH. Try again later.**'

          cooldown = datetime.datetime.now() + datetime.timedelta(seconds=60)

          if self.not_on_cooldown(addr):
            self.cooldowns[addr] = cooldown
            await message.channel.send(s)