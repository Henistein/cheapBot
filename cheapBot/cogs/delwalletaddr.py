import discord
from discord.ext import commands
from typing import List
from .. import config
import re


def check_addr(message):
  if re.search('0x[a-zA-Z0-9]{40}',message):
    return True
  else:
    return False

class DelWalletAddr(commands.Cog):
  bot: commands.Bot
  allowed_channels: List[str]

  def __init__(self, bot):
    self.bot = bot
    self.allowed_channels = config.allowed_del_wallet_addr_channels

  @commands.Cog.listener()
  async def on_message(self, message):
    if message.author.bot:
      return

    if not message.content:
      return

    if message.channel.name in self.allowed_channels:
      if check_addr(message.content):
        await message.delete()
        await message.author.send("Please note that you are not allowed to enter wallet addresses in #%s channel in the CHEAPETH server" %message.channel)