from discord.ext import commands
from pyourls3 import Yourls

from utils.permissions import level


class Links(commands.Cog):
    """A cog for link shortening and statistics."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        config = bot.cfg.module("links")
        self.api = Yourls(addr=config["url"], user="bot", passwd=config["password"])

    @commands.command(name="shorturl")
    @level(40)
    async def shorturl(self, ctx: commands.Context, url: str, short: str = None):
        """Creates a new short URL for a given address."""

        if "mcatho.me" in url:
            return await ctx.reply("You can't shorten already shortened URLs.")

        try:
            short_url = self.api.shorten(url, short)
        except:
            return await ctx.reply("Shortening the URL failed. Perhaps it is a dumplicate?")

        await ctx.reply(f"Shortened URL: <{short_url['shorturl']}>")

    @commands.command(name="urlstats")
    @level(40)
    async def urlstats(self, ctx: commands.Context, url: str = "all"):
        """Gets click statistics for the given URL."""

        if url == "all":
            stats = self.api.stats()
            return await ctx.reply(f"**__All Link Stats:__**\nTotal Links: {stats['total_links']}\nTotal Clicks: {stats['total_clicks']}")

        try:
            stats = self.api.url_stats(url)
            return await ctx.reply(f"**__Link Stats for <{stats['shorturl']}>:__**\nTotal Clicks: {stats['clicks']}")
        except Exception as e:
            await ctx.reply("That link couldn't be found.")


def setup(bot: commands.Bot):
    bot.add_cog(Links(bot))
