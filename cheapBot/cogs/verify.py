import datetime
import json
import re
from typing import List

import discord  # type: ignore
from discord.ext import commands

from .. import config
from . import client as cb

'''
Verification script, using the power of memes - WIP
'''


class Meme:
  message: discord.Message
  # datetime timestamp
  expiry_time: datetime.datetime
  # cTH address of sender derived from message
  address: str
  # Amount of reactions received
  reaction_count: int

  def __init__(self, message: discord.Message, expiry_time: datetime.datetime, address: str,
               reaction_count: int):
    self.message = message
    self.expiry_time = expiry_time
    self.address = address
    self.reaction_count = reaction_count


class MemeVerify(commands.Cog):
  bot: commands.Bot
  allowed_channels: List[str]

  # Message, datetime received, address, reaction count
  # meme_list: List[Tuple[discord.message, datetime.datetime, str, int]] = []
  meme_list: List[Meme]

  min_approval: int

  def __init__(self, bot: commands.Bot):
    self.bot = bot
    self.meme_list: List[Meme] = []
    self.allowed_channels = config.allowed_meme_channels
    self.min_approval = config.min_meme_reaction_approval

  def approved_users(self):
    for meme in self.meme_list:
      if meme.reaction_count >= self.min_approval:
        info = f'meme.address {meme.reaction_count}'
        cb.sendInfo(info)
        print(info)

  def update_list(self):
    for meme in self.meme_list:
      meme.reaction_count = 0

      for react in meme.message.reactions:
        meme.reaction_count += react.count

      if datetime.datetime.now() > meme.expiry_time:
        self.meme_list.remove(meme)

  def update_json(self):
    temp = []
    with open("approval.json", "w") as outfile:
      for meme in self.meme_list:
        dictionary = {}
        dictionary["uuid"] = meme.address
        dictionary["reactions"] = meme.reaction_count
        if meme.reaction_count >= self.min_approval:
            dictionary["approval"] = True
        else:
            dictionary["approval"] = False
        dictionary["expired_time"] = meme.expiry_time.__str__()

        temp.append(dictionary)

      json.dump(temp, outfile)

  @commands.Cog.listener()
  async def on_reaction_add(self, reaction, user):
      self.update_list()
      self.update_json()
      #approved_users(meme_list)

  @commands.Cog.listener()
  async def on_raw_reaction_remove(self, payload):
      self.update_list()
      self.update_json()
      #approved_users(meme_list)

  @commands.Cog.listener()
  async def on_message(self, message: discord.Message):
    # Check if an attachment is on the message
    if message.content:
      if message.attachments:
        message_words = message.content.split()
        for word in message_words:
          if re.search("^[- a-fA-F0-9]{36}$", word):
            meme_time = (datetime.datetime.now() + datetime.timedelta(minutes=60))
            meme = Meme(message, meme_time, word, 0)
            self.meme_list.append(meme)
