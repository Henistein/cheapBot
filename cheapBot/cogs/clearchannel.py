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

class ClearChannel(commands.Cog):
  bot: commands.Bot
  allowed_channels: List[str]

  def __init__(self, bot):
    self.bot = bot
    self.allowed_channels = config.allowed_clear_channel_channels

  @commands.command()
  async def clear(self, ctx: commands.Context, n_messages: str = '10'):
    await ctx.channel.send("Message received")
    if ctx.author.bot:
      return
    
    if not ctx.message.content:
      return

    if ctx.channel.name in self.allowed_channels:
      async for message in ctx.channel.history(limit=int(n_messages)+1):
        if(check_addr(message.content)):
          await message.delete()