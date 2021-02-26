from discord.ext import commands  # type: ignore

from . import config
from .cogs.gimme import Gimme
from .cogs.twitter import Twitter
from .cogs.verify import MemeVerify
from .cogs.party import Party
from .cogs.speculator import Speculator
from .cogs.delwalletaddr import DelWalletAddr
from .cogs.clearchannel import ClearChannel

class CheapBot(commands.Bot):
  def __init__(self, prefix='$cheap '):
    super().__init__(command_prefix=prefix)

  async def on_ready(self):
    print(f'We have logged in as {self.user}')

  async def on_message(self, message):
    await self.process_commands(message)
    return


if __name__ == '__main__':
  bot = CheapBot()
  bot.add_cog(Gimme(bot))
  bot.add_cog(MemeVerify(bot))
  bot.add_cog(Twitter(bot))
  bot.add_cog(Party(bot))
  bot.add_cog(Speculator(bot))
  bot.add_cog(DelWalletAddr(bot))
  bot.add_cog(ClearChannel(bot))
  bot.run(config.token)