import discord
from discord.ext import commands
from tinydb import TinyDB, Query
from .. import config
from web3 import Web3
from typing import Dict, List


w3 = Web3(Web3.HTTPProvider('https://node.cheapeth.org/rpc'))
# ADDRESS OF cheapGames contract, handles fees and payouts - 5% ?
# bank = 

class Games(commands.Cog):
  bot: commands.Bot
  allowed_channels: List[str]

  def __init__(self, bot: commands.Bot):
    super().__init__()
    self.bot = bot
    self.allowed_channels = config.allowed_game_channels

  async def dice(self, ctx: commands.Context, amount: str, opp: str):

