from discord import Message
from discord.ext import commands

from utils.permissions import permission_level


class AMP(commands.Cog):
    """A cog for preventing mass pings by members."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.author.bot:
            return

        if permission_level(self.bot, message.author) >= 10:
            return

        mentions = set(message.mentions)

        settings = self.bot.cfg.module("amp")
        max_mentions = settings.get("max_mentions", 6)
        muted_role = settings["muted_role"]

        if len(mentions) < max_mentions:
            return

        role = message.guild.get_role(muted_role)

        await self.bot.logger.info(
            f"[AMP] Muted {message.author} for exceeding max mention limit ({max_mentions})"
        )

        try:
            await message.author.add_roles(role)
            await message.author.send(
                "You have been muted for exceeding the maximum mention limit per message."
            )
        except Exception as e:
            pass  # TODO: Debug logging (requires templatebot fix)

        await message.add_reaction("❌")


def setup(bot: commands.Bot):
    bot.add_cog(AMP(bot))
