import datetime
from typing import Dict, List
import discord
from discord.ext import commands
from .. import config
from secrets import choice
import os

cooldown_time = 30

class Party(commands.Cog):
  bot: commands.Bot
  allowed_channels: List[str]
  cooldowns: Dict[str, datetime.datetime]


  def __init__(self, bot: commands.Bot):
    super().__init__()
    self.bot = bot
    self.allowed_channels = config.allowed_party_channels
    self.cooldowns = {}

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

  # LETS PARTY

  @commands.command()
  async def party(self, ctx: commands.Context):
    get_userid = ctx.message.author
    #print(get_userid)
    if ctx.author.bot:
      return

    # Check if the address is on message
    if not ctx.message.content:
      return

    if ctx.channel.name in self.allowed_channels:
      message: discord.Message = ctx.message

      s = f'**{message.author.name}** is partying!'

      cooldown = datetime.datetime.now() + datetime.timedelta(seconds=cooldown_time)

      if self.not_on_cooldown(get_userid):
        self.cooldowns[get_userid] = cooldown
        
        
        imgs = []
        path_party = "cheapBot/cogs/party_imgs"
        file_name = choice(os.listdir(path_party))
        file_ext = file_name.split(".")[-1]
        with open(f'{path_party}\\{file_name}', 'rb') as f:
          await message.channel.send(file=discord.File(f, 'new_filename.'+file_ext))
          await message.channel.send(s)
      
      else:
        #cooldowned
        await message.channel.send("You have to party harder!")

