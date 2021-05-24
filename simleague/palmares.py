import discord
from redbot.core import checks, commands
from .abc import MixinMeta
from .utils import mergeDict, checkReacts
import asyncio


class PalmaresMixin(MixinMeta):
    """Palmares Settings"""

    @checks.admin_or_permissions(manage_guild=True)
    @commands.command()
    async def genseasonpalmares(self, ctx, season: str):
        """Generate palmares for a season."""
        teams = await self.config.guild(ctx.guild).teams()
        stats = await self.config.guild(ctx.guild).stats()
        notes = await self.config.guild(ctx.guild).notes()
        maxplayers = await self.config.guild(ctx.guild).maxplayers()
        standings = await self.config.guild(ctx.guild).standings()
        cupgames = await self.config.guild(ctx.guild).cupgames()
        tots = await self.config.guild(ctx.guild).tots()
        async with self.config.guild(ctx.guild).palmares() as palmares:
            seasonstats = ["goals", "assists", "reds", "yellows", "motm", "owngoals"]
            for s in seasonstats:
                stat = stats[s]
                for i, userid in list(enumerate(sorted(stat, key=stat.get, reverse=True)))[:10]:
                    if userid in palmares:
                        if season in palmares[userid]:
                            if s in palmares[userid][season]:
                                pass
                            else:
                                palmares[userid][season][s] = (stat[userid], i + 1)
                        else:
                            palmares[userid][season] = {}
                            palmares[userid][season][s] = (stat[userid], i + 1)
                    else:
                        palmares[userid] = {}
                        palmares[userid][season] = {}
                        palmares[userid][season][s] = (stat[userid], i + 1)
            contributions = mergeDict(self, stats["goals"], stats["assists"])
            for i, userid in list(
                enumerate(sorted(contributions, key=contributions.get, reverse=True))
            )[:10]:
                if userid in palmares:
                    if season in palmares[userid]:
                        if "ga" in palmares[userid][season]:
                            pass
                        else:
                            palmares[userid][season]["ga"] = (contributions[userid], i + 1)
                    else:
                        palmares[userid][season] = {}
                        palmares[userid][season]["ga"] = (contributions[userid], i + 1)
                else:
                    palmares[userid] = {}
                    palmares[userid][season] = {}
                    palmares[userid][season]["ga"] = (contributions[userid], i + 1)
            for n in notes:
                note = round(sum(float(pn) for pn in notes[n]) / len(notes[n]), 2)
                notes[n] = note
            for i, userid in list(enumerate(sorted(notes, key=notes.get, reverse=True)))[:15]:
                if userid in palmares:
                    if season in palmares[userid]:
                        if "note" in palmares[userid][season]:
                            pass
                        else:
                            palmares[userid][season]["note"] = (notes[userid], i + 1)
                    else:
                        palmares[userid][season] = {}
                        palmares[userid][season]["note"] = (notes[userid], i + 1)
                else:
                    palmares[userid] = {}
                    palmares[userid][season] = {}
                    palmares[userid][season]["note"] = (notes[userid], i + 1)
            for i, t in enumerate(
                sorted(
                    standings,
                    key=lambda x: (standings[x]["points"], standings[x]["gd"], standings[x]["gf"]),
                    reverse=True,
                )
            ):
                team = teams[t]
                for userid in team["members"]:
                    if userid in palmares:
                        if season in palmares[userid]:
                            if "finish" in palmares[userid][season]:
                                pass
                            else:
                                palmares[userid][season]["finish"] = (t, i + 1)
                        else:
                            palmares[userid][season] = {}
                            palmares[userid][season]["finish"] = (t, i + 1)
                    else:
                        palmares[userid] = {}
                        palmares[userid][season] = {}
                        palmares[userid][season]["finish"] = (t, i + 1)
            if len(cupgames):
                final = cupgames["2"][0]
                semifinals = cupgames["4"]
                winner = (
                    final["team1"]
                    if (final["score1"] + final["penscore1"])
                    > (final["score2"] + final["penscore2"])
                    else final["team2"]
                )
                second = final["team2"] if winner == final["team1"] else final["team1"]
                third = (
                    semifinals[0]["team1"]
                    if (semifinals[0]["score1"] + semifinals[0]["penscore1"])
                    < (semifinals[0]["score2"] + semifinals[0]["penscore2"])
                    else semifinals[0]["team2"]
                )
                fourth = (
                    semifinals[1]["team1"]
                    if (semifinals[1]["score1"] + semifinals[1]["penscore1"])
                    < (semifinals[0]["score2"] + semifinals[1]["penscore2"])
                    else semifinals[1]["team2"]
                )
                cupteams = {
                    "winner": {"team": winner, "finish": 1},
                    "second": {"team": second, "finish": 2},
                    "third": {"team": third, "finish": 3},
                    "fourth": {"team": fourth, "finish": 3},
                }
                for t in enumerate(cupteams):
                    team = cupteams[t[1]]["team"]
                    if team != "BYE":
                        for userid in teams[team]["members"]:
                            if userid in palmares:
                                if season in palmares[userid]:
                                    if "cupfinish" in palmares[userid][season]:
                                        pass
                                    else:
                                        palmares[userid][season]["cupfinish"] = (
                                            team,
                                            cupteams[t[1]]["finish"],
                                        )
                                else:
                                    palmares[userid][season] = {}
                                    palmares[userid][season]["cupfinish"] = (
                                        team,
                                        cupteams[t[1]]["finish"],
                                    )
                            else:
                                palmares[userid] = {}
                                palmares[userid][season] = {}
                                palmares[userid][season]["cupfinish"] = (
                                    team,
                                    cupteams[t[1]]["finish"],
                                )
            tots = tots["players"]
            for i, userid in enumerate(list(tots)[:maxplayers]):
                if userid in palmares:
                    if season in palmares[userid]:
                        if "tots" in palmares[userid][season]:
                            pass
                        else:
                            palmares[userid][season]["tots"] = (i + 1, 1)
                    else:
                        palmares[userid][season] = {}
                        palmares[userid][season]["tots"] = (i + 1, 1)
                else:
                    palmares[userid] = {}
                    palmares[userid][season] = {}
                    palmares[userid][season]["tots"] = (i + 1, 1)
            userid = list(tots)[0]
            if userid in palmares:
                if season in palmares[userid]:
                    if "pots" in palmares[userid][season]:
                        pass
                    else:
                        palmares[userid][season]["pots"] = (i + 1, 1)
                else:
                    palmares[userid][season] = {}
                    palmares[userid][season]["pots"] = (i + 1, 1)
            else:
                palmares[userid] = {}
                palmares[userid][season] = {}
                palmares[userid][season]["pots"] = (i + 1, 1)
        await ctx.tick()

    @checks.admin_or_permissions(manage_guild=True)
    @commands.command()
    async def addpalmares(self, ctx, user: discord.Member, season, stat, value, rank):
        """Add palmares entry for a member."""
        validstats = [
            "goals",
            "owngoals",
            "assists",
            "ga",
            "reds",
            "yellows",
            "motms",
            "finish",
            "cupfinish",
            "communityshield",
        ]
        if stat not in validstats:
            return await ctx.send("Invalid stat. Must be one of {}".format(", ".join(validstats)))
        async with self.config.guild(ctx.guild).palmares() as palmares:
            userid = str(user.id)
            if userid in palmares:
                if season in palmares[userid]:
                    palmares[userid][season][stat] = (value, rank)
                else:
                    palmares[userid][season] = {}
                    palmares[userid][season][stat] = (value, rank)
            else:
                palmares[userid] = {}
                palmares[userid][season] = {}
                palmares[userid][season][stat] = (value, rank)
            await ctx.tick()

    @checks.admin_or_permissions(manage_guild=True)
    @commands.command(name="transferpalmares")
    async def transfer_palmares(self, ctx, u1id: str, u2id: str):
        """Transfer palmares from a member to another."""
        async with self.config.guild(ctx.guild).palmares() as palmares:
            if u1id in palmares:
                if u2id in palmares:
                    for season in palmares[u1id]:
                        palmares[u2id][season] = palmares[u1id][season]
                else:
                    palmares[u2id] = {}
                    for season in palmares[u1id]:
                        palmares[u2id][season] = palmares[u1id][season]
            await ctx.tick()

    @checks.admin_or_permissions(manage_guild=True)
    @commands.command()
    async def updatepalmaresseason(
        self, ctx, season1: str, season2: str, user: discord.Member = None
    ):
        """Update palmares season for all members."""
        async with self.config.guild(ctx.guild).palmares() as palmares:
            if user is None:
                for uid in palmares:
                    player = await self.bot.fetch_user(uid)
                    if season1 in palmares[uid]:
                        await self.checkReacts(
                            ctx,
                            "This will replace palmares for season {} for {}".format(
                                season1, player.name
                            ),
                        )
                        if season2 in palmares[uid]:
                            confirm = await self.checkReacts(
                                ctx,
                                "{} already has a palmares for {}. Are you sure you want to override it ?".format(
                                    player.name, season2
                                ),
                            )
                            if confirm:
                                palmares[uid][season2] = palmares[uid][season1]
                                del palmares[uid][season1]
                            else:
                                pass
                        else:
                            palmares[uid][season2] = {}
                            palmares[uid][season2] = palmares[uid][season1]
                            del palmares[uid][season1]
                    else:
                        await ctx.send("Season {} not found for {}".format(season1, player.name))
            else:
                uid = str(user.id)
                if uid in palmares:
                    if season1 in palmares[uid]:
                        confirm = await self.checkReacts(
                            ctx,
                            "Palmares season {} will be changed to season {} for {}. Are you sure ?".format(
                                season1, season2, user.name
                            ),
                        )
                        if confirm:
                            palmares[uid][season2] = {}
                            palmares[uid][season2] = palmares[uid][season1]
                            del palmares[uid][season1]
                            return await ctx.send("Done.")
                        else:
                            return await ctx.send("Season override cancelled.")
                    else:
                        await ctx.send("Season {} not found for {}".format(season1, user.name))
            await ctx.tick()

    @checks.admin_or_permissions(manage_guild=True)
    @commands.command()
    async def updateteampalmaresseason(self, ctx, team, season1: str, season2: str, stat: str):
        """Update palmares season for a team's members."""
        teams = await self.config.guild(ctx.guild).teams()
        if team not in teams:
            return await ctx.send("Team does not exist.")
        validstats = [
            "goals",
            "assists",
            "ga",
            "reds",
            "yellows",
            "motms",
            "finish",
            "cupfinish",
            "communityshield",
        ]
        if stat not in validstats:
            return await ctx.send("Invalid stat. Must be one of {}".format(", ".join(validstats)))
        async with self.config.guild(ctx.guild).palmares() as palmares:
            for uid in teams[team]["members"]:
                player = await self.bot.fetch_user(uid)
                if uid in palmares:
                    if season1 in palmares[uid]:
                        if stat not in palmares[uid][season1]:
                            await ctx.send(
                                "{} not found in season {} for {}.".format(
                                    stat, season1, player.name
                                )
                            )
                            pass
                        else:
                            confirm = await self.checkReacts(
                                ctx,
                                "Palmares stat {} will be moved from season {} to season {} for {}. Are you sure ?".format(
                                    stat, season1, season2, player.name
                                ),
                            )
                            if confirm:
                                if season2 not in palmares[uid]:
                                    palmares[uid][season2] = {}
                                    palmares[uid][season2][stat] = palmares[uid][season1][stat]
                                    del palmares[uid][season1][stat]
                                else:
                                    palmares[uid][season2][stat] = palmares[uid][season1][stat]
                    else:
                        await ctx.send("Season {} not found for {}".format(season1, player.name))
        await ctx.tick()

    @commands.command(name="palmares")
    async def viewpalmares(self, ctx, user: discord.Member):
        """View palmares for a member."""
        palmares = await self.config.guild(ctx.guild).palmares()
        if str(user.id) not in palmares:
            return await ctx.send("No palmares for {}.".format(user.display_name))
        palmares = palmares[str(user.id)]
        embed = discord.Embed(
            color=ctx.author.color,
            title="Palmares for {}".format(user.display_name),
            description="------------- List of individual player honours -------------",
        )
        a = []
        for season in sorted(palmares):
            seasontitle = "Season {}".format(season) if int(season) != 0 else "Preseason"
            a.append(f"\n**{seasontitle}**")
            finish = palmares[season]["finish"] if "finish" in palmares[season].keys() else None
            cupfinish = (
                palmares[season]["cupfinish"] if "cupfinish" in palmares[season].keys() else None
            )
            goals = palmares[season]["goals"] if "goals" in palmares[season].keys() else None
            owngoals = palmares[season]["owngoals"] if "owngoals" in palmares[season].keys() else None
            note = palmares[season]["note"] if "note" in palmares[season].keys() else None
            assists = palmares[season]["assists"] if "assists" in palmares[season].keys() else None
            ga = palmares[season]["ga"] if "ga" in palmares[season].keys() else None
            motms = palmares[season]["motms"] if "motms" in palmares[season].keys() else None
            yellows = palmares[season]["yellows"] if "yellows" in palmares[season].keys() else None
            reds = palmares[season]["reds"] if "reds" in palmares[season].keys() else None
            tots = palmares[season]["tots"] if "tots" in palmares[season].keys() else None
            pots = palmares[season]["pots"] if "pots" in palmares[season].keys() else None
            communityshield = (
                palmares[season]["communityshield"]
                if "communityshield" in palmares[season].keys()
                else None
            )
            newP = {
                "pots": pots,
                "tots": tots,
                "finish": finish,
                "cupfinish": cupfinish,
                "communityshield": communityshield,
                "note": note,
                "goals": goals,
                "assists": assists,
                "ga": ga,
                "motms": motms,
                "owngoals": owngoals,
                "yellows": yellows,
                "reds": reds,
            }
            for p in newP:
                if p in palmares[season]:
                    res = palmares[season][p]
                    if int(res[1]) == 1:
                        n = "1st"
                    elif int(res[1]) == 2:
                        n = "2nd"
                    elif int(res[1]) == 3:
                        n = "3rd"
                    else:
                        n = "{}th".format(res[1])
                    medal = ""
                    if n == "1st":
                        medal = ":first_place:"
                        if p in ["finish", "cupfinish", "communityshield"]:
                            medal = ":trophy:"
                        if p == "tots":
                            medal = ":medal:"
                        if p == "pots":
                            medal = ":military_medal:"
                    if n == "2nd":
                        medal = ":second_place:"
                    if n == "3rd":
                        medal = ":third_place:"
                    parsedp = self.parsestat(p, res[0], int(res[1]) - 1, n)
                    parsedp = "{} {}".format(parsedp, medal)
                    a.append(parsedp)
        embed.add_field(name="List of honours", value="\n".join(a))
        await ctx.send(embed=embed)

    def parsestat(self, stat, value, n, nth):
        if stat == "communityshield":
            return "Won the Community Shield with {}.".format(value)
        if stat == "finish":
            return "Finished {} in the league with {}.".format(nth, value)
        if stat == "cupfinish":
            if n == 0:
                return "Cup winner with {}.".format(value)
            if n == 1:
                return "Cup finalist with {}.".format(value)
            if n == 2:
                return "Cup semi-finalist with {}.".format(value)
        if stat == "pots":
            return "Won player of the season."
        if stat == "tots":
            return "Voted in the team of the season."
        if stat in ["goals", "assists", "ga", "note"]:
            if n == 0:
                prefix = "Top"
            else:
                prefix = "{} best".format(nth)
            if stat == "goals":
                s = ["goal scorer", "goals"]
            elif stat == "assists":
                s = ["assister", "assists"]
            elif stat == "ga":
                s = ["goal contributor", "goals + assists"]
            else:
                s = ["average note", ""]
            return "{} {} with {} {}.".format(prefix, s[0], value, s[1])
        if stat in ["yellows", "reds", "motms"]:
            if n == 0:
                prefix = "Most"
            else:
                prefix = "{} most".format(nth)
            if stat == "yellows":
                s = "yellow cards"
            elif stat == "reds":
                s = "reds cards"
            else:
                s = "MOTMs"
            return "{} {} received with {} {}.".format(prefix, s, value, s)
