import discord
from discord.ext import commands
from typing import List
from .. import config


def is_input_goood(input):
  for c in input:
    if c not in ["0", "1", " "]:
      return False
  return True


class BinaryOnly(commands.Cog):
  bot: commands.Bot
  allowed_channels: List[str]

  def __init__(self, bot):
    self.bot = bot
    self.allowed_channels = config.allowed_binary_channels

  @commands.Cog.listener()
  async def on_message(self, message):
    if message.author.bot:
      return

    if not message.content:
      return

    if message.channel.name in self.allowed_channels:
      if not is_input_goood(message.content):
        await message.delete()
        await message.channel.send('%s: %s' % (message.author.mention, ' '.join(format(ord(x), 'b') for x in message.content)))