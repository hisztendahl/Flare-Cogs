import asyncio

def mergeDict(self, dict1, dict2):
    """Merge dictionaries and keep values of common keys in list"""
    dict3 = {**dict1, **dict2}
    for key, value in dict3.items():
        if key in dict1 and key in dict2:
            try:
                dict3[key] = value + dict1[key]
            except TypeError:
                self.log.info(f"Error merging dicts. {value} + {dict1[key]}")
    return dict3


def getformbonus(form):
    streak = form["streak"]
    result = form["result"]
    if result == "D" or result is None:
        return 1
    multiplier = 1
    if streak == 1:
        multiplier = 2.5
    elif streak == 2:
        multiplier = 5
    elif streak == 3:
        multiplier = 7.5
    elif streak == 4:
        multiplier = 12.5
    elif streak == 5:
        multiplier = 20
    elif streak == 6:
        multiplier = 32.5
    else:
        multiplier = 50
    if result == "W":
        multiplier = -multiplier
    multiplier = (100 + multiplier) / 100
    return multiplier


def getformbonuspercent(form):
    streak = form["streak"]
    result = form["result"]
    if result == "D" or result is None:
        return 0
    multiplier = 1
    if streak == 1:
        multiplier = 2.5
    elif streak == 2:
        multiplier = 5
    elif streak == 3:
        multiplier = 7.5
    elif streak == 4:
        multiplier = 12.5
    elif streak == 5:
        multiplier = 20
    elif streak == 6:
        multiplier = 32.5
    else:
        multiplier = 50
    if result == "W":
        multiplier = -multiplier
    if result == "L":
        multiplier = "+{}".format(multiplier)
    return multiplier

async def checkReacts(self, ctx, message):
    msg = await ctx.send(message)
    confirm_emoji = "✅"
    cancel_emoji = "❎"
    await msg.add_reaction(confirm_emoji)
    await msg.add_reaction(cancel_emoji)
    try:
        reaction, user = await asyncio.wait_for(
            ctx.bot.wait_for("reaction_add", check=lambda r, u: u.id == ctx.author.id), 30
        )
    except:
        await msg.clear_reactions()
        return False
    if reaction.emoji == confirm_emoji:
        return True
    elif reaction.emoji == cancel_emoji:
        return False
