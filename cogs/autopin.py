from discord import Message
from discord.ext import commands

content = """
__**Here you can propose new projects!**__

__**BEFORE YOU MAKE A SUGGESTION:**__
:book: **Check if it hasn't been suggested already.** Use Discord's search function, check <#755121689913983136>, pins or ask in <#738860957685776395> if unsure.
:mag_right: **Google it!** A lot of seeds/world downloads are already publicly known!
:thinking: **Consider if what you're suggesting has any significance** to the community, be it historical or technical.

__**HOW TO MAKE A GOOD SUGGESTION:**__
:white_check_mark: Explain properly what you mean and why should we be interested.
:white_check_mark: Try to include a link or an image (where it makes sense).

:x: ***Blatant duplicates and spam will get deleted without notice!** :wastebasket:
Otherwise you'll get notified in <#738860957685776395> if there are any problems.
Repeatedly making bad suggestions will get your access to this channel removed!*
"""


class AutoPin(commands.Cog):
    """A cog to automatically pin a message at the bottom of a channel."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.started = False

        self.message = None

    @commands.Cog.listener()
    async def on_ready(self):
        channel = self.bot.get_channel(self.bot.cfg.module("autopin")["channel"])

        i = 0
        success = False

        async for message in channel.history(limit=100):
            if message.author == self.bot.user:
                self.message = message
                success = True
                break

            i += 1

        if i and success:
            await self.message.delete()
            self.message = await channel.send(content)
            return

        if not success:
            self.message = await channel.send(content)

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.channel.id != self.bot.cfg.module("autopin")["channel"]:
            return

        if message.author.bot:
            return

        try:
            await self.message.delete()#
        except:
            pass # TODO: Debug logging (requires templatebot fix)

        self.message = await message.channel.send(content)


def setup(bot: commands.Bot):
    bot.add_cog(AutoPin(bot))
