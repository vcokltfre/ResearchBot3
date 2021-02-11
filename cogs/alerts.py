from discord import Member
from discord.ext import commands
from time import time

WEEK = 24 * 3600 * 7


def age(snowflake: int) -> int:
    timestamp = (snowflake >> 22) + 1420070400000

    return round(time() - (timestamp // 1000))


class Alerts(commands.Cog):
    """A cog for alerting when new users join, and welcoming them."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: Member):
        if member.bot:
            return

        acc_age = age(member.id)

        if acc_age >= WEEK:
            return

        channel = self.bot.get_channel(self.bot.cfg.module("alerts")["channel"])

        s = acc_age % 60
        m = (acc_age // 60) % 60
        h = (acc_age // 3600) % 24
        d = (acc_age // 86400) % 7
        await channel.send(
            f"NEW USER: {member.mention} ({member.id}) was created in the last week! ({d}d {h}h {m}m {s}s ago)"
        )

        ## Welcome channel message

        config = self.bot.get_channel(self.bot.cfg.module("welcome"))
        channel = self.bot.get_channel(config["channel"])
        content = config["message"].format(member=str(member))

        await channel.send(content)


def setup(bot: commands.Bot):
    bot.add_cog(Alerts(bot))
