import discord
from redbot.core import checks, commands

from .abc import MixinMeta
from .utils import mergeDict


class StatsMixin(MixinMeta):
    """Stats Settings"""

    @checks.admin_or_permissions(manage_guild=True)
    @commands.command()
    async def clearstats(self, ctx, user: discord.Member = None):
        """Clear statistics for a user."""
        if user is not None:
            userid = str(user.id)
            async with self.config.guild(ctx.guild).stats() as stats:
                stats["goals"].pop(userid, None)
                stats["assists"].pop(userid, None)
                stats["yellows"].pop(userid, None)
                stats["reds"].pop(userid, None)
                stats["motm"].pop(userid, None)
                stats["penalties"].pop(userid, None)
        await ctx.tick()

    @checks.admin_or_permissions(manage_guild=True)
    @commands.command()
    async def addnotes(self, ctx, user: discord.Member, *value):
        """Add notes for a player."""
        userid = str(user.id)
        async with self.config.guild(ctx.guild).notes() as notes:
            if userid not in notes:
                notes[userid] = value
            else:
                for v in value:
                    notes[userid].append(v)
            await ctx.tick()

    @checks.admin_or_permissions(manage_guild=True)
    @commands.command()
    async def clearnotes(self, ctx, user: discord.Member):
        """Clear notes for a player."""
        userid = str(user.id)
        async with self.config.guild(ctx.guild).notes() as notes:
            notes.pop(userid, None)

    @commands.command()
    async def viewnotes(self, ctx, user: discord.Member):
        """View notes for a player."""
        notes = await self.config.guild(ctx.guild).notes()
        userid = str(user.id)
        if userid not in notes:
            return await ctx.send("No note for {}.".format(user.display_name))
        else:
            return await ctx.send("Notes: {}".format(" / ".join(str(x) for x in notes[userid])))

    @checks.admin_or_permissions(manage_guild=True)
    @commands.command()
    async def addstats(self, ctx, user: discord.Member, stat: str, value: int):
        """Add statistics for a user."""
        validstats = [
            "goals",
            "assists",
            "ga",
            "yellows",
            "reds",
            "motm",
            "penscored",
            "penmissed",
        ]
        if stat not in validstats:
            return await ctx.send("Invalid stat. Must be one of {}".format(", ".join(validstats)))
        userid = str(user.id)
        async with self.config.guild(ctx.guild).stats() as stats:
            if stat in ["penscored", "penmissed"]:
                if userid in stats["penalties"]:
                    if stat == "penscored":
                        if "scored" in stats["penalties"][userid]:
                            stats["penalties"][userid]["scored"] += value
                        else:
                            stats["penalties"][userid]["scored"] = value
                    if stat == "penmissed":
                        if "missed" in stats["penalties"][userid]:
                            stats["penalties"][userid]["missed"] += value
                        else:
                            stats["penalties"][userid]["missed"] = value
                else:
                    stats["penalties"][userid] = {
                        "scored": value if stat == "penscored" else 0,
                        "missed": value if stat == "penmissed" else 0,
                    }
            else:
                if userid in stats[stat]:
                    stats[stat][userid] += value
                    if stats[stat][userid] == 0:
                        stats[stat].pop(userid, None)
                else:
                    stats[stat][userid] = value
        await ctx.tick()

    @commands.command()
    async def teamstats(self, ctx, team, comptype="league"):
        """Sim League Team Statistics."""
        teams = await self.config.guild(ctx.guild).teams()
        if team not in teams:
            return await ctx.send("This team does not exist.")
        stats = {}
        title = "League"
        if comptype not in ["league", "cup", "all"]:
            return await ctx.send("Incorrect type. Must be one of: league, cup, all.")
        if comptype == "league":
            stats = await self.config.guild(ctx.guild).stats()
            standings = await self.config.guild(ctx.guild).standings()
        elif comptype == "cup":
            title = "Cup"
            stats = await self.config.guild(ctx.guild).cupstats()
            standings = await self.config.guild(ctx.guild).cupstandings()
        else:
            title = "All comps"
            stats = await self.config.guild(ctx.guild).stats()
            cupstats = await self.config.guild(ctx.guild).cupstats()

            standings = await self.config.guild(ctx.guild).standings()
            cupstandings = await self.config.guild(ctx.guild).cupstandings()
            for s in stats:
                stats[s] = mergeDict(self, stats[s], cupstats[s])
            for s in standings:
                standings[s] = mergeDict(self, standings[s], cupstandings[s])
        members = teams[team]["members"]
        embed = discord.Embed(
            color=ctx.author.color,
            title="Team Statistics for {} - ({})".format(team, title.upper()),
            description="-----------------------------------------------------------------",
        )
        ts = ""
        teamstats = standings[team]
        res_headers = [
            "played",
            "wins",
            "draws",
            "losses",
            "PPG",
        ]
        try:
            ppg = round(
                (int(teamstats["wins"]) * 3 + int(teamstats["draws"])) / int(teamstats["played"]),
                2,
            )
        except ZeroDivisionError:
            ppg = 0.0
        res_stats = [
            teamstats["played"],
            teamstats["wins"],
            teamstats["draws"],
            teamstats["losses"],
            ppg,
        ]
        for i, t in enumerate(res_headers):
            ts += f"{t.title()}: {res_stats[i]}\n"
        embed.add_field(name="Results", value=ts)

        ts = ""
        goals_headers = [
            "shots",
            "goals scored",
            "goal conversion",
            "goals conceded",
            "cleansheets",
        ]
        cs = stats["cleansheets"]
        cs = cs[team] if team in cs else 0
        try:
            goal_conversion = int(teamstats["gf"]) / int(teamstats["chances"])
            goal_conversion = round(goal_conversion * 100, 2)
        except ZeroDivisionError:
            goal_conversion = 0.0
        goals_stats = [
            teamstats["chances"],
            teamstats["gf"],
            f"{goal_conversion}%",
            teamstats["ga"],
            cs,
        ]
        for i, t in enumerate(goals_headers):
            ts += f"{t.title()}: {goals_stats[i]}\n"
        embed.add_field(name="Shots & Goals", value=ts)

        ts = ""
        fairplay_headers = [
            "fouls",
            "yellow cards",
            "red cards",
        ]
        fairplay_stats = [
            teamstats["fouls"],
            teamstats["yellows"],
            teamstats["reds"],
        ]
        for i, t in enumerate(fairplay_headers):
            ts += f"{t.title()}: {fairplay_stats[i]}\n"
        embed.add_field(name="Fair Play", value=ts)
        await ctx.send(embed=embed)

        embed = discord.Embed(
            color=ctx.author.color,
            title="Players Statistics for {} - ({})".format(team, title.upper()),
            description="-----------------------------------------------------------------",
        )
        for m in members:
            userid = str(m)
            pens = stats["penalties"].get(userid)
            statistics = [
                stats["goals"].get(userid),
                stats["assists"].get(userid),
                stats["yellows"].get(userid),
                stats["reds"].get(userid),
                stats["motm"].get(userid),
                pens.get("missed") if pens else None,
                pens.get("scored") if pens else None,
            ]
            headers = [
                "goals",
                "assists",
                "yellows",
                "reds",
                "motms",
                "pen. missed",
                "pen. scored",
            ]
            stat = ""
            for i, h in enumerate(headers):
                statistic = statistics[i] if statistics[i] is not None else 0
                stat += f"{h.title()}: {statistic}\n"
            member = await self.statsmention(ctx, [m])
            embed.add_field(name=member, value=stat)
        await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True)
    async def leaguestats(self, ctx, user: discord.Member = None):
        """Sim League Statistics."""
        if user is not None:
            stats = await self.config.guild(ctx.guild).stats()
            notes = await self.config.guild(ctx.guild).notes()
            userid = str(user.id)
            note = notes[userid] if userid in notes else None
            if note is not None:
                note = round(sum(float(n) for n in note) / len(note), 2)
            pens = stats["penalties"].get(userid)
            statistics = [
                note,
                stats["goals"].get(userid),
                stats["assists"].get(userid),
                stats["yellows"].get(userid),
                stats["reds"].get(userid),
                stats["motm"].get(userid),
                pens.get("missed") if pens else None,
                pens.get("scored") if pens else None,
            ]
            headers = [
                "note",
                "goals",
                "assists",
                "yellows",
                "reds",
                "motms",
                "penalties missed",
                "penalties scored",
            ]
            embed = discord.Embed(
                color=ctx.author.color, title="Statistics for {}".format(user.display_name)
            )
            for i, stat in enumerate(statistics):
                if stat is not None:
                    embed.add_field(name=headers[i].title(), value=stat)
                else:
                    embed.add_field(name=headers[i].title(), value="0")
            await ctx.send(embed=embed)

        else:
            await ctx.send_help()
            stats = await self.config.guild(ctx.guild).stats()
            goalscorer = sorted(stats["goals"], key=stats["goals"].get, reverse=True)
            assists = sorted(stats["assists"], key=stats["assists"].get, reverse=True)
            yellows = sorted(stats["yellows"], key=stats["yellows"].get, reverse=True)
            reds = sorted(stats["reds"], key=stats["reds"].get, reverse=True)
            motms = sorted(stats["motm"], key=stats["motm"].get, reverse=True)
            cleansheets = sorted(stats["cleansheets"], key=stats["cleansheets"].get, reverse=True)
            penscored = sorted(
                stats["penalties"], key=lambda x: stats["penalties"][x]["scored"], reverse=True
            )
            penmissed = sorted(
                stats["penalties"], key=lambda x: stats["penalties"][x]["missed"], reverse=True
            )
            msg = ""
            msg += "**Top Goalscorer**: {} - {}\n".format(
                await self.statsmention(ctx, goalscorer),
                stats["goals"][goalscorer[0]] if len(goalscorer) else "",
            )
            msg += "**Most Assists**: {} - {}\n".format(
                await self.statsmention(ctx, assists),
                stats["assists"][assists[0]] if len(assists) else "",
            )
            msg += "**Most Yellow Cards**: {} - {}\n".format(
                await self.statsmention(ctx, yellows),
                stats["yellows"][yellows[0]] if len(yellows) else "",
            )
            msg += "**Most Red Cards**: {} - {}\n".format(
                await self.statsmention(ctx, reds), stats["reds"][reds[0]] if len(reds) else ""
            )
            msg += "**Penalties Scored**: {} - {}\n".format(
                await self.statsmention(ctx, penscored),
                stats["penalties"][penscored[0]]["scored"] if len(penscored) else "",
            )
            msg += "**Penalties Missed**: {} - {}\n".format(
                await self.statsmention(ctx, penmissed),
                stats["penalties"][penmissed[0]]["missed"] if len(penmissed) else "",
            )
            msg += "**MOTMs**: {} - {}\n".format(
                await self.statsmention(ctx, motms), stats["motm"][motms[0]] if len(motms) else ""
            )
            if cleansheets:
                msg += "**Cleansheets**: _{}_ - {}\n".format(
                    cleansheets[0], stats["cleansheets"][cleansheets[0]]
                )
            else:
                msg += "**Cleansheets**: {}\n".format(await self.statsmention(ctx, cleansheets))
            await ctx.maybe_send_embed(msg)

    async def statsmention(self, ctx, stats):
        if stats:
            user = self.bot.get_user(int(stats[0]))
            if not user:
                user = await self.bot.fetch_user(int(stats[0]))
                if not user:
                    return "Invalid User {}".format(stats[0])
            return f"_{user.name}_"
        else:
            return "None"

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

    @leaguestats.command(name="notes")
    async def _notes(self, ctx):
        """Players with the best average note."""
        notes = await self.config.guild(ctx.guild).notes()
        if notes:
            for n in notes:
                note = round(sum(float(pn) for pn in notes[n]) / len(notes[n]), 2)
                notes[n] = note
            a = []
            for i, k in enumerate(sorted(notes, key=notes.get, reverse=True)):
                user_team = await self.get_user_with_team(ctx, k)
                a.append(f"{i+1}. {user_team[0].name} ({user_team[1]}) - {notes[k]}")
            embed = discord.Embed(
                title="Best players", description="\n".join(a[:10]), colour=0xFF0000
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("No stats available.")

    @leaguestats.command(name="ga", alias=["ga", "contributions"])
    async def _goals_assists(self, ctx):
        """Players with the most combined goals and assists."""
        stats = await self.config.guild(ctx.guild).stats()
        goals = stats["goals"]
        assists = stats["assists"]
        contributions = mergeDict(self, goals, assists)
        stats = contributions
        if contributions:
            a = []
            for i, k in enumerate(sorted(stats, key=stats.get, reverse=True)):
                user_team = await self.get_user_with_team(ctx, k)
                a.append(f"{i+1}. {user_team[0].name} ({user_team[1]}) - {stats[k]}")
            embed = discord.Embed(
                title="Top goal involvements (goals + assists)",
                description="\n".join(a[:10]),
                colour=0xFF0000,
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("No stats available.")

    @leaguestats.command(name="goals", alias=["topscorer", "topscorers"])
    async def _goals(self, ctx):
        """Players with the most goals."""
        stats = await self.config.guild(ctx.guild).stats()
        stats = stats["goals"]
        if stats:
            a = []
            for i, k in enumerate(sorted(stats, key=stats.get, reverse=True)):
                user_team = await self.get_user_with_team(ctx, k)
                a.append(f"{i+1}. {user_team[0].name} ({user_team[1]}) - {stats[k]}")
            embed = discord.Embed(
                title="Top Scorers", description="\n".join(a[:10]), colour=0xFF0000
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("No stats available.")

    @leaguestats.command(aliases=["yellowcards"])
    async def yellows(self, ctx):
        """Players with the most yellow cards."""
        stats = await self.config.guild(ctx.guild).stats()
        stats = stats["yellows"]
        if stats:
            a = []
            for i, k in enumerate(sorted(stats, key=stats.get, reverse=True)):
                user_team = await self.get_user_with_team(ctx, k)
                a.append(f"{i+1}. {user_team[0].name} ({user_team[1]}) - {stats[k]}")
            embed = discord.Embed(
                title="Most Yellow Cards", description="\n".join(a[:10]), colour=0xFF0000
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("No stats available.")

    @leaguestats.command(alies=["redcards"])
    async def reds(self, ctx):
        """Players with the most red cards."""
        stats = await self.config.guild(ctx.guild).stats()
        stats = stats["reds"]
        if stats:
            a = []
            for i, k in enumerate(sorted(stats, key=stats.get, reverse=True)):
                user_team = await self.get_user_with_team(ctx, k)
                a.append(f"{i+1}. {user_team[0].name} ({user_team[1]}) - {stats[k]}")
            embed = discord.Embed(
                title="Most Red Cards", description="\n".join(a[:10]), colour=0xFF0000
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("No stats available.")

    @leaguestats.command(alies=["motms"])
    async def motm(self, ctx):
        """Players with the most MOTMs."""
        stats = await self.config.guild(ctx.guild).stats()
        stats = stats["motm"]
        if stats:
            a = []
            for i, k in enumerate(sorted(stats, key=stats.get, reverse=True)):
                user_team = await self.get_user_with_team(ctx, k)
                a.append(f"{i+1}. {user_team[0].name} ({user_team[1]}) - {stats[k]}")
            embed = discord.Embed(
                title="Most MOTMs", description="\n".join(a[:10]), colour=0xFF0000
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("No stats available.")

    @leaguestats.command(name="cleansheets")
    async def _cleansheets(self, ctx):
        """Teams with the most cleansheets."""
        stats = await self.config.guild(ctx.guild).stats()
        stats = stats["cleansheets"]
        if stats:
            a = []
            for i, k in enumerate(sorted(stats, key=stats.get, reverse=True)[:10]):
                a.append(f"{i+1}. {k} - {stats[k]}")
            embed = discord.Embed(
                title="Most Cleansheets", description="\n".join(a), colour=0xFF0000
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("No stats available.")

    @leaguestats.command()
    async def penalties(self, ctx):
        """Penalties scored and missed statistics."""
        stats = await self.config.guild(ctx.guild).stats()
        stats = stats["penalties"]
        if stats:
            a = []
            b = []
            for i, k in enumerate(
                sorted(stats, key=lambda x: stats[x]["scored"], reverse=True)[:10]
            ):
                user_team = await self.get_user_with_team(ctx, k)
                a.append(f"{i+1}. {user_team[0].name} ({user_team[1]}) - {stats[k]['scored']}")
            for i, k in enumerate(
                sorted(stats, key=lambda x: stats[x]["missed"], reverse=True)[:10]
            ):
                user_team = await self.get_user_with_team(ctx, k)
                b.append(f"{i+1}. {user_team[0].name} ({user_team[1]}) - {stats[k]['missed']}")
            embed = discord.Embed(
                title="Penalty Statistics",
                colour=0xFF0000,
                description="=== Scored and Missed penalties statistics ===",
            )
            embed.add_field(name="Penalties Scored", value="\n".join(a))
            embed.add_field(name="Penalties Missed", value="\n".join(b))
            await ctx.send(embed=embed)
        else:
            await ctx.send("No stats available.")

    @leaguestats.command()
    async def assists(self, ctx):
        """Players with the most assists."""
        stats = await self.config.guild(ctx.guild).stats()
        stats = stats["assists"]
        if stats:
            a = []
            for i, k in enumerate(sorted(stats, key=stats.get, reverse=True)[:10]):
                user_team = await self.get_user_with_team(ctx, k)
                a.append(f"{i+1}. {user_team[0].name} ({user_team[1]}) - {stats[k]}")
            embed = discord.Embed(
                title="Assist Statistics", description="\n".join(a), colour=0xFF0000
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("No stats available.")
