from templatebot import Bot
from discord import Intents

from utils.config import ConfigLoader

config = ConfigLoader()
botconf = config.get("bot", {})

bot = Bot(
    name="ResearchBot",
    command_prefix=botconf.get("prefix", "!"),
    intents=Intents.all(),
    logging_url=botconf.get("webhook"),
    help_command=None,
)

bot.cfg = config

bot.load_initial_cogs(
    "cogs.amp",
)

bot.run(botconf["token"])