import random
from math import ceil

import discord
from redbot.core import checks, commands
from redbot.core.utils.menus import DEFAULT_CONTROLS, menu
import validators

from .abc import MixinMeta
from .utils import mergeDict

class TotsMixin(MixinMeta):
    """TOTS Settings"""

    @commands.group(autohelp=True)
    async def tots(self, ctx):
        """TOTS Commands."""

    @checks.admin_or_permissions(manage_guild=True)
    @tots.command(name="kit")
    async def tots_kit(self, ctx, kiturl: str):
        """Set TOTS kit."""
        if not validators.url(kiturl):
            await ctx.send("This doesn't seem to be a valid URL.")
        if not kiturl.lower().endswith(".png"):
            await ctx.send("URL must be a png.")
        async with self.config.guild(ctx.guild).tots() as tots:
            tots["kit"] = kiturl
            await ctx.tick()

    @checks.admin_or_permissions(manage_guild=True)
    @tots.command(name="logo")
    async def tots_logo(self, ctx, logourl: str):
        """Set TOTS logo."""
        if not validators.url(logourl):
            await ctx.send("This doesn't seem to be a valid URL.")
        if not logourl.lower().endswith(".png"):
            await ctx.send("URL must be a png.")
        async with self.config.guild(ctx.guild).tots() as tots:
            tots["logo"] = logourl
            await ctx.tick()

    @checks.admin_or_permissions(manage_guild=True)
    @tots.command(name="getranking")
    async def getplayersranking(self, ctx):
        """Ranks player to select team of the season and player of the season."""
        users = await self.config.guild(ctx.guild).users()
        stats = await self.config.guild(ctx.guild).stats()
        cupstats = await self.config.guild(ctx.guild).cupstats()
        notes = await self.config.guild(ctx.guild).notes()
        ranking = {}
        for u in users:
            userid = u
            note = notes[userid] if userid in notes else None
            if note is not None:
                note = round(sum(float(n) for n in note) / len(note), 2)
            note = float(note) * 10 if note else 0
            goals = stats["goals"].get(userid)
            goals = int(goals) * 5 if goals else 0
            owngoals = stats["owngoals"].get(userid)
            owngoals = int(owngoals) * 5 if owngoals else 0
            shots = stats["shots"].get(userid)
            shots = int(shots) * 0.5 if shots else 0
            assists = stats["assists"].get(userid)
            assists = int(assists) * 3 if assists else 0
            fouls = stats["fouls"].get(userid)
            fouls = int(fouls) * 0.5 if fouls else 0
            yellows = stats["yellows"].get(userid)
            yellows = int(yellows) * 1 if yellows else 0
            reds = stats["reds"].get(userid)
            reds = int(reds) * 3 if reds else 0
            motms = stats["motm"].get(userid)
            motms = int(motms) * 5 if motms else 0
            rank = note + goals + shots + assists + motms - yellows - reds - owngoals - fouls
            if cupstats:
                cupgoals = cupstats["goals"].get(userid)
                cupgoals = int(cupgoals) * 2.5 if cupgoals else 0
                cupowngoals = cupstats["owngoals"].get(userid)
                cupowngoals = int(cupowngoals) * 5 if cupowngoals else 0
                cupshots = cupstats["shots"].get(userid)
                cupshots = int(cupshots) * 0.25 if cupshots else 0
                cupassists = cupstats["assists"].get(userid)
                cupassists = int(cupassists) * 1.5 if cupassists else 0
                cupfouls = cupstats["fouls"].get(userid)
                cupfouls = int(cupfouls) * 0.25 if cupfouls else 0
                cupyellows = cupstats["yellows"].get(userid)
                cupyellows = int(cupyellows) * 0.5 if cupyellows else 0
                cupreds = cupstats["reds"].get(userid)
                cupreds = int(cupreds) * 1.5 if cupreds else 0
                cupmotms = cupstats["motm"].get(userid)
                cupmotms = int(cupmotms) * 2.5 if cupmotms else 0
                rank = (
                    rank
                    + cupgoals
                    + cupshots
                    + cupassists
                    + cupmotms
                    - cupyellows
                    - cupreds
                    - cupowngoals
                    - cupfouls
                )

            ranking[userid] = rank
            ranking = {
                k: v for k, v in sorted(ranking.items(), key=lambda item: item[1], reverse=True)
            }
        tots = list(ranking)
        async with self.config.guild(ctx.guild).tots() as simtots:
            simtots["pots"] = tots[0]
            for t in tots:
                simtots["players"][t] = ranking[t]
            await ctx.tick()

    @tots.command(name="view")
    async def view_tots(self, ctx):
        """View Team of the Season."""
        tots = await self.config.guild(ctx.guild).tots()
        maxplayers = await self.config.guild(ctx.guild).maxplayers()
        if not len(tots["players"]):
            return await ctx.send("No TOTS available.")
        async with ctx.typing():
            embeds = []
            embed = discord.Embed(
                title="{}".format(
                    "TOTS",
                ),
                description="------------ Team of the Season ------------",
                colour=ctx.author.colour,
            )
            players = {}
            for player in list(tots["players"].keys())[:maxplayers]:
                user = self.bot.get_user(player)
                if user is None:
                    user = await self.bot.fetch_user(player)
                players[player] = user.display_name
            embed.add_field(
                name="Members:",
                value="\n".join(list(players.values())),
                inline=True,
            )
            if tots["logo"] is not None:
                embed.set_thumbnail(url=tots["logo"])
            embeds.append(embed)
            if tots["kit"] is not None:
                embed = discord.Embed(title="Kit", colour=ctx.author.colour)
                embed.set_image(url=tots["kit"])
                embeds.append(embed)
        await menu(ctx, embeds, DEFAULT_CONTROLS)

    @checks.admin_or_permissions(manage_guild=True)
    @tots.command(name="champion")
    async def trophy_champion(self, ctx, trophy: str, season: str):
        """Generate Trophy winner image."""
        if trophy not in ["league", "cup"]:
            return await ctx.send(
                "Invalid argument. Must be one of {}".format(", ".join(["league", "cup"]))
            )
        if trophy == "league":
            standings = await self.config.guild(ctx.guild).standings()
        else:
            standings = await self.config.guild(ctx.guild).cupstandings()
        standings = sorted(
            standings,
            key=lambda x: (standings[x]["points"], standings[x]["gd"], standings[x]["gf"]),
            reverse=True,
        )
        champion = standings[0]
        image = await self.championscup(ctx, champion, trophy, season)
        await ctx.send(file=image)

    @checks.admin_or_permissions(manage_guild=True)
    @tots.command(name="walkout")
    async def tots_walkout(self, ctx):
        """Team of the season walkout. Warning: Tailored for 4 teams members"""
        tots = await self.config.guild(ctx.guild).tots()
        maxplayers = await self.config.guild(ctx.guild).maxplayers()
        tots = tots["players"]
        if not len(tots):
            return await ctx.send("No TOTS available.")
        totslist = list(tots.items())[:maxplayers]
        random.shuffle(totslist)
        tots = dict(totslist)
        im = await self.totswalkout(ctx, tots)
        await ctx.send(file=im)

    @checks.admin_or_permissions(manage_guild=True)
    @tots.command(name="teamstats")
    async def tots_teamstats(self, ctx):
        """Team stats recap for the season."""
        standings = await self.config.guild(ctx.guild).standings()
        stats = {}
        t = []
        wins = sorted(standings, key=lambda x: (standings[x]["wins"]), reverse=True)
        for x in wins[:3]:
            t.append([x, standings[x]["wins"]])
        stats["wins"] = t
        t = []
        goals = sorted(standings, key=lambda x: (standings[x]["gf"]), reverse=True)
        for x in goals[:3]:
            t.append([x, standings[x]["gf"]])
        stats["goals"] = t
        t = []
        shots = sorted(standings, key=lambda x: (standings[x]["chances"]), reverse=True)
        for x in shots[:3]:
            t.append([x, standings[x]["chances"]])
        stats["shots"] = t
        t = []
        conversion = sorted(
            standings,
            key=lambda x: (
                int(standings[x]["gf"]) / int(standings[x]["chances"])
                if int(standings[x]["chances"]) > 0
                else 0
            ),
            reverse=True,
        )
        for x in conversion[:3]:
            conv = (
                int(standings[x]["gf"]) / int(standings[x]["chances"])
                if int(standings[x]["chances"]) > 0
                else 0
            )
            conv = f"{int(round(float(conv) * 100, 2))}%"
            t.append([x, conv])
        stats["conversion"] = t
        t = []
        conceded = sorted(standings, key=lambda x: (standings[x]["ga"]))
        for x in conceded[:3]:
            t.append([x, standings[x]["ga"]])
        stats["conceded"] = t
        t = []
        fairplay = sorted(
            standings,
            key=lambda x: (
                standings[x]["reds"],
                standings[x]["yellows"],
            ),
        )
        for x in fairplay[:3]:
            t.append([x, standings[x]["yellows"], standings[x]["reds"]])
        stats["fairplay"] = t
        t = []
        fouls = sorted(standings, key=lambda x: (standings[x]["fouls"]))
        for x in fouls[:3]:
            t.append([x, standings[x]["fouls"]])
        stats["fouls"] = t
        t = []
        image = await self.totsteamstats(ctx, stats)
        await ctx.send(file=image)

    @checks.admin_or_permissions(manage_guild=True)
    @tots.command(name="playerstats")
    async def tots_playerstats(self, ctx):
        """Player stats recap for the season."""
        notes = await self.config.guild(ctx.guild).notes()
        for n in notes:
            note = round(sum(float(pn) for pn in notes[n]) / len(notes[n]), 2)
            notes[n] = note
        stats = await self.config.guild(ctx.guild).stats()
        playerstats = {}
        t = []
        sortednotes = sorted(notes, key=notes.get, reverse=True)
        for x in sortednotes[:3]:
            t.append([x, notes[x]])
        playerstats["notes"] = t
        t = []
        motms = sorted(stats["motm"], key=stats["motm"].get, reverse=True)
        for x in motms[:3]:
            t.append([x, stats["motm"][x]])
        playerstats["motm"] = t
        t = []
        fairplay = mergeDict(self, stats["yellows"], stats["reds"])
        fairplay = sorted(fairplay, key=fairplay.get)
        for x in fairplay[:3]:
            t.append(
                [
                    x,
                    int(stats["yellows"][x] if x in stats["yellows"] else 0)
                    + 3 * int(stats["reds"][x] if x in stats["reds"] else 0),
                ]
            )
        playerstats["fair-play"] = t
        t = []
        goals = sorted(stats["goals"], key=stats["goals"].get, reverse=True)
        for x in goals[:3]:
            t.append([x, stats["goals"][x]])
        playerstats["goals"] = t
        t = []
        assists = sorted(stats["assists"], key=stats["assists"].get, reverse=True)
        for x in assists[:3]:
            t.append([x, stats["assists"][x]])
        playerstats["assists"] = t
        t = []
        ga = mergeDict(self, stats["goals"], stats["assists"])
        ga = sorted(ga, key=ga.get, reverse=True)
        for x in ga[:3]:
            t.append([x, int(stats["goals"][x]) + int(stats["assists"][x])])
        playerstats["goals + assists"] = t
        t = []
        image = await self.totsplayerstats(ctx, playerstats)
        await ctx.send(file=image)

    async def get_user_with_team(self, ctx, userid):
        teams = await self.config.guild(ctx.guild).teams()
        user = self.bot.get_user(int(userid))
        if not user:
            user = await self.bot.fetch_user(int(userid))
        if not user:
            user = "Invalid User {}".format(userid)
        team = ""
        for t in teams:
            if userid in teams[t]["members"]:
                team = t.upper()[:3]
                pass
        return [user, team]

    @tots.command(name="ranking")
    async def tots_ranking(self, ctx, page: int = 1):
        """POTS Ranking."""
        tots = await self.config.guild(ctx.guild).tots()
        tots = tots["players"]
        if tots:
            a = []
            for i, k in enumerate(sorted(tots, key=tots.get, reverse=True)):
                user_team = await self.get_user_with_team(ctx, k)
                a.append(
                    f"{i+1}. {user_team[0].name} ({user_team[1]}) - {round(float(tots[k]), 2)}"
                )
                p1 = (page - 1) * 10 if page > 1 else page - 1
                p2 = page * 10
            if p1 > len(a):
                maxpage = ceil(len(a) / 10)
                return await ctx.send("Page does not exist. Max page is {}.".format(maxpage))
            embed = discord.Embed(
                title="POTS Ranking", description="\n".join(a[p1:p2]), colour=0xFF0000
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("No tots ranking available.")

    @checks.admin_or_permissions(manage_guild=True)
    @tots.command(name="pots")
    async def pots_walkout(self, ctx):
        """Player of the season infographic."""
        tots = await self.config.guild(ctx.guild).tots()
        if "pots" not in tots:
            return await ctx.send("No POTS available.")

        userid = tots["pots"]
        stats = await self.config.guild(ctx.guild).stats()
        cupstats = await self.config.guild(ctx.guild).cupstats()
        notes = await self.config.guild(ctx.guild).notes()
        note = notes[userid] if userid in notes else None
        if note is not None:
            note = round(sum(float(n) for n in note) / len(note), 2)
        goals = stats["goals"].get(userid)
        goals = goals if goals else 0
        assists = stats["assists"].get(userid)
        assists = assists if assists else 0
        yellows = stats["yellows"].get(userid)
        yellows = yellows if yellows else 0
        reds = stats["reds"].get(userid)
        reds = reds if reds else 0
        motms = stats["motm"].get(userid)
        motms = motms if motms else 0
        if cupstats:
            cupgoals = cupstats["goals"].get(userid)
            goals = goals + (cupgoals if cupgoals else 0)
            cupassists = cupstats["assists"].get(userid)
            assists = assists + (cupassists if cupassists else 0)
            cupyellows = cupstats["yellows"].get(userid)
            yellows = yellows + (cupyellows if cupyellows else 0)
            cupreds = cupstats["reds"].get(userid)
            reds = reds + (cupreds if cupreds else 0)
            cupmotms = cupstats["motm"].get(userid)
            motms = motms + (cupmotms if cupmotms else 0)
        statistics = [note, motms, goals, assists, yellows, reds]
        im = await self.potswalkout(ctx, tots["pots"], statistics)
        await ctx.send(file=im)

