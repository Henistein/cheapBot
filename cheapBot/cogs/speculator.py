from discord.ext import commands
from typing import Dict, List
from .. import config
import datetime
from secrets import choice



keywords = ["moon", "eth", "speculate", "cth", "sell", "prices", "price", "ethereum", "value",
            "exchange", "bitcoin", "worth", "cheap", "demand", "how", "much", "buy", "crypto"
            "trade", "cheapeth", "gas", "token"]

speculator_reply = ("Houston we have a Speculator! :rocket: Go to #speculation if you want to trash talk!",
                        "Speculator ALERT!",
                        "There is some s.p.e.c.u.l.a.t.i.o.n.s. here. #speculation",
                        "Goku: solution is ban speculator. #speculation",
                        "Goku: speculator make everything cost 1000x more than it shouild. #speculation",
                        "Goku: we bring middle class to crypto. #speculation",
                        "Goku: i want cheapeth planet. #speculation",
                        "Stay cheap! https://cheapeth.org/staycheap.html #speculation",
                        "Can we stay on :earth_africa:? #speculation",
                        "Goku: if speculator, no crowdsale!",
                        "Goku: speculator ruin world",
                        "Goku: we need to fight speculator!")


words_treshold = 2
cooldown_time = 20



def check(word, list):
  if word in list:
    return True
  else:
    return False

class Speculator(commands.Cog):
  bot: commands.Bot
  allowed_channels: List[str]
  cooldowns: Dict[str, datetime.datetime]

  def __init__(self, bot):
    self.bot = bot
    self.allowed_channels = config.allowed_check_spec_channels
    self.cooldowns = {}


  def not_on_cooldown(self, addr: str) -> bool:
    if addr in self.cooldowns:
      if datetime.datetime.now() > self.cooldowns[addr]:
        self.cooldowns.pop(addr)
        return True
      else:
        return False

    return True


  @commands.Cog.listener()
  async def on_message(self, message):
    #print(message.content)
    get_userid = message.author
    #print(get_userid)
    if message.author.bot:
      return        

    if not message.content:
      return

    if message.channel.name in self.allowed_channels:
      msg_to_list = message.content.split()
      counted_strikes = 0
      for word in keywords:
        if check(word,msg_to_list):
          counted_strikes += 1
          if counted_strikes > words_treshold:
            #await message.reply("Speculator!")
            cooldown = datetime.datetime.now() + datetime.timedelta(seconds=cooldown_time)

            if self.not_on_cooldown(get_userid):
              self.cooldowns[get_userid] = cooldown
              await message.channel.send(choice(speculator_reply))
