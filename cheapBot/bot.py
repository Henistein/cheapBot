from discord.ext import commands  # type: ignore

from .cogs.gimme import Gimme
from .cogs.verify import MemeVerify
from .cogs.twitter import Twitter
from . import config


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
  bot.run(config.token)

