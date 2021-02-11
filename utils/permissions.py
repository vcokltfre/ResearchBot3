from discord import Member
from discord.ext import commands, check, Context

def permission_level(bot: commands.Bot, member: Member) -> int:
    config = bot.cfg.get("permissions")

    users = config.get("users", {})
    roles = config.get("roles", {})

    top = 0

    if member.id in users:
        top = users[member.id]

    for role in member.roles:
        if role.id in roles:
            if roles[role.id] > top:
                top = roles[role.id]

    return top

def level(l: int):
    def predicate(ctx: Context):
        pl = permission_level(ctx.bot, ctx.author)

        if pl >= l:
            return True

        return False

    return check(predicate)
