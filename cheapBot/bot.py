from discord.ext import commands  # type: ignore

import config
from scripts.gimme import Gimme
from scripts.verify import MemeVerify
from scripts.twitter import Twitter

class CheapBot(commands.Bot):
  prefix: str

  def __init__(self, prefix='$cheap', min_approval=10, allowed_channels=[], cooldown_time=5 * 60):
    super().__init__(command_prefix=prefix)
    self.prefix = prefix

  async def on_ready(self):
    print(f'We have logged in as {self.user}')

  async def on_message(self, message):
    await self.process_commands(message)
    return


if __name__ == '__main__':
  bot = CheapBot(prefix='$cheap ', allowed_channels=['free-cheapeth-sold-out'])
  bot.add_cog(Gimme(bot))
  bot.add_cog(MemeVerify(bot))
  bot.add_cog(Twitter(bot))
  bot.run(config.token)
