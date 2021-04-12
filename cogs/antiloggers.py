from discord import Message
from discord.ext import commands

from re import compile


LOGGERS = compile(r"\blogg?.rs?")


class Antiloggers(commands.Cog):
    """No loggers."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if LOGGERS.match(message.content):
            await message.delete()


def setup(bot: commands.Bot):
    bot.add_cog(Antiloggers(bot))
