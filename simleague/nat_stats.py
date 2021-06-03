import discord
from redbot.core import checks, commands
from redbot.core.utils.menus import DEFAULT_CONTROLS, menu
from scipy.stats import binom

from .abc import MixinMeta
from .utils import mergeDict, getformbonus, getformbonuspercent
from math import ceil


class NatStatsMixin(MixinMeta):
    """Nat Stats Settings"""

    @checks.admin_or_permissions(manage_guild=True)
    @commands.command()
    async def nat_clearstats(self, ctx, user: discord.Member = None):
        """Clear statistics for a user."""
        if user is None:
            return await ctx.send_help()
        userid = str(user.id)
        async with self.config.guild(ctx.guild).nstats() as stats:
            stats["goals"].pop(userid, None)
            stats["owngoals"].pop(userid, None)
            stats["shots"].pop(userid, None)
            stats["fouls"].pop(userid, None)
            stats["assists"].pop(userid, None)
            stats["yellows"].pop(userid, None)
            stats["reds"].pop(userid, None)
            stats["motm"].pop(userid, None)
            stats["penalties"].pop(userid, None)
        await ctx.tick()

    # @checks.admin_or_permissions(manage_guild=True)
    # @commands.command()
    # async def nat_addnotes(self, ctx, user: discord.Member, *value):
    #     """Add notes for a player."""
    #     userid = str(user.id)
    #     async with self.config.guild(ctx.guild).notes() as notes:
    #         if userid not in notes:
    #             notes[userid] = value
    #         else:
    #             for v in value:
    #                 notes[userid].append(v)
    #         await ctx.tick()

    # @checks.admin_or_permissions(manage_guild=True)
    # @commands.command()
    # async def nat_removenote(self, ctx, user: discord.Member, index):
    #     """Remove note for a player (at index)."""
    #     userid = str(user.id)
    #     async with self.config.guild(ctx.guild).notes() as notes:
    #         del notes[userid][int(index)]
    #         await ctx.tick()

    # @checks.admin_or_permissions(manage_guild=True)
    # @commands.command()
    # async def nat_clearnotes(self, ctx, user: discord.Member):
    #     """Clear notes for a player."""
    #     userid = str(user.id)
    #     async with self.config.guild(ctx.guild).notes() as notes:
    #         notes.pop(userid, None)

    # @commands.command()
    # async def nat_viewnotes(self, ctx, user: discord.Member):
    #     """View notes for a player."""
    #     notes = await self.config.guild(ctx.guild).notes()
    #     userid = str(user.id)
    #     if userid not in notes:
    #         return await ctx.send("No note for {}.".format(user.display_name))
    #     else:
    #         return await ctx.send("Notes: {}".format(" / ".join(str(x) for x in notes[userid])))

    # @commands.command(name="pstats")
    # async def nat_vs_stats(self, ctx, user1: discord.Member, user2: discord.Member):
    #     stats = await self.config.guild(ctx.guild).stats()
    #     notes = await self.config.guild(ctx.guild).notes()
    #     user1id = str(user1.id)
    #     user2id = str(user2.id)
    #     user1_team = await self.get_user_with_team(ctx, user1id)
    #     user2_team = await self.get_user_with_team(ctx, user2id)
    #     embed = discord.Embed(
    #         title="Players Comparison",
    #         description="------------- {} vs {} -------------\n\n".format(user1.name, user2.name),
    #         colour=ctx.author.colour,
    #     )
    #     for userid in [user1id, user2id]:
    #         note = notes[userid] if userid in notes else None
    #         if note is not None:
    #             note = round(sum(float(n) for n in note) / len(note), 2)
    #         note = note or "N/A"
    #         pens = stats["penalties"].get(userid)
    #         goals = stats["goals"].get(userid) or 0
    #         owngoals = stats["owngoals"].get(userid) or 0
    #         assists = stats["assists"].get(userid) or 0
    #         yellows = stats["yellows"].get(userid) or 0
    #         reds = stats["reds"].get(userid) or 0
    #         motms = stats["motm"].get(userid) or 0
    #         shots = stats["shots"].get(userid) or 0
    #         fouls = stats["fouls"].get(userid) or 0
    #         penmissed = pens.get("missed") if pens else 0
    #         penscored = pens.get("scored") if pens else 0
    #         title = f"{user1_team[0].name} ({user1_team[1]})"
    #         if userid == user2id:
    #             title = f"{user2_team[0].name} ({user2_team[1]})"
    #         embed.add_field(
    #             name=title,
    #             value="Note: {}\nMotMs: {}\n\nGoals: {}\nAssists: {}\nShots: {}\nPen Scored: {}\nPen Missed: {}\n\nYellows: {}\nReds: {}\nFouls: {}\nOwn Goals: {}".format(
    #                 note,
    #                 motms,
    #                 goals,
    #                 assists,
    #                 shots,
    #                 penscored,
    #                 penmissed,
    #                 yellows,
    #                 reds,
    #                 fouls,
    #                 owngoals,
    #             ),
    #         )
    #     await ctx.send(embed=embed)

    @checks.admin_or_permissions(manage_guild=True)
    @commands.command()
    async def nat_addteamstats(self, ctx, team: str, stat: str, value: int):
        """Add statistics for a team."""
        validstats = [
            "played",
            "wins",
            "losses",
            "points",
            "gd",
            "gf",
            "ga",
            "draws",
            "reds",
            "yellows",
            "fouls",
            "chances",
        ]
        teams = await self.config.guild(ctx.guild).nteams()
        if team not in teams:
            return await ctx.send("Team does not exist.")
        if stat not in validstats:
            return await ctx.send("Invalid stat. Must be one of {}".format(", ".join(validstats)))
        async with self.config.guild(ctx.guild).nstandings() as standings:
            standings[team][stat] += value
        await ctx.tick()

    @checks.admin_or_permissions(manage_guild=True)
    @commands.command()
    async def nat_addstats(self, ctx, user: discord.Member, stat: str, value: int):
        """Add statistics for a user."""
        validstats = [
            "goals",
            "owngoals",
            "shots",
            "fouls",
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
        async with self.config.guild(ctx.guild).nstats() as stats:
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
    async def nat_teamstats(self, ctx, team):
        """Sim League Team Statistics."""
        teams = await self.config.guild(ctx.guild).nteams()
        if team not in teams:
            return await ctx.send("This team does not exist.")
        stats = {}
        title = "League"
        stats = await self.config.guild(ctx.guild).nstats()
        standings = await self.config.guild(ctx.guild).nstandings()
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
        ]
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
                stats["owngoals"].get(userid),
                stats["assists"].get(userid),
                stats["yellows"].get(userid),
                stats["reds"].get(userid),
                stats["motm"].get(userid),
                pens.get("missed") if pens else None,
                pens.get("scored") if pens else None,
            ]
            headers = [
                "goals",
                "owngoals",
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
    async def nat_leaguestats(self, ctx, user: discord.Member = None):
        """Sim League Statistics."""
        if user is not None:
            stats = await self.config.guild(ctx.guild).nstats()
            notes = await self.config.guild(ctx.guild).notes()
            userid = str(user.id)
            note = notes[userid] if userid in notes else None
            if note is not None:
                note = round(sum(float(n) for n in note) / len(note), 2)
            pens = stats["penalties"].get(userid)
            statistics = [
                note,
                stats["goals"].get(userid),
                stats["owngoals"].get(userid),
                stats["assists"].get(userid),
                stats["yellows"].get(userid),
                stats["reds"].get(userid),
                stats["motm"].get(userid),
                stats["shots"].get(userid),
                stats["fouls"].get(userid),
                pens.get("missed") if pens else None,
                pens.get("scored") if pens else None,
            ]
            headers = [
                "note",
                "goals",
                "owngoals",
                "assists",
                "yellows",
                "reds",
                "motms",
                "shots",
                "fouls",
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
            owngoalscorer = sorted(stats["owngoals"], key=stats["owngoals"].get, reverse=True)
            assists = sorted(stats["assists"], key=stats["assists"].get, reverse=True)
            yellows = sorted(stats["yellows"], key=stats["yellows"].get, reverse=True)
            reds = sorted(stats["reds"], key=stats["reds"].get, reverse=True)
            motms = sorted(stats["motm"], key=stats["motm"].get, reverse=True)
            shots = sorted(stats["shots"], key=stats["shots"].get, reverse=True)
            fouls = sorted(stats["fouls"], key=stats["fouls"].get, reverse=True)
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
            msg += "**Most Shots**: {} - {}\n".format(
                await self.statsmention(ctx, shots),
                stats["shots"][shots[0]] if len(shots) else "",
            )
            msg += "**Most Own Goals**: {} - {}\n".format(
                await self.statsmention(ctx, owngoalscorer),
                stats["owngoals"][owngoalscorer[0]] if len(owngoalscorer) else "",
            )
            msg += "**Most Assists**: {} - {}\n".format(
                await self.statsmention(ctx, assists),
                stats["assists"][assists[0]] if len(assists) else "",
            )
            msg += "**Most Fouls**: {} - {}\n".format(
                await self.statsmention(ctx, fouls),
                stats["fouls"][fouls[0]] if len(fouls) else "",
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
            await ctx.maybe_send_embed(msg)

    async def nat_statsmention(self, ctx, stats):
        if stats:
            user = self.bot.get_user(int(stats[0]))
            if not user:
                user = await self.bot.fetch_user(int(stats[0]))
                if not user:
                    return "Invalid User {}".format(stats[0])
            return f"_{user.name}_"
        else:
            return "None"

    async def nat_get_user_with_team(self, ctx, userid):
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

    @nat_leaguestats.command(name="notes")
    async def nat__notes(self, ctx):
        """Players with the best average note."""
        notes = await self.config.guild(ctx.guild).notes()
        if not notes:
            return await ctx.send("No stats available.")
        else:
            for n in notes:
                note = round(sum(float(pn) for pn in notes[n]) / len(notes[n]), 2)
                notes[n] = note
            embeds = []
            pages = ceil(len(notes) / 10)
            for page in range(pages):
                page = page + 1
                p1 = (page - 1) * 10 if page > 1 else page - 1
                p2 = page * 10
                a = []
                for i, k in enumerate(sorted(notes, key=notes.get, reverse=True)[p1:p2]):
                    user_team = await self.get_user_with_team(ctx, k)
                    a.append(f"{i + p1 +1}. {user_team[0].name} ({user_team[1]}) - {notes[k]}")
                embed = discord.Embed(
                    title="Best players _({}/{})_".format(page, pages),
                    description="\n".join(a),
                    colour=0xFF0000,
                )
                embeds.append(embed)
        await menu(ctx, embeds, DEFAULT_CONTROLS)

    @nat_leaguestats.command(name="ga", alias=["ga", "contributions"])
    async def nat__goals_assists(self, ctx):
        """Players with the most combined goals and assists."""
        stats = await self.config.guild(ctx.guild).nstats()
        goals = stats["goals"]
        assists = stats["assists"]
        contributions = mergeDict(self, goals, assists)
        stats = contributions
        if not contributions:
            return await ctx.send("No stats available.")
        else:
            embeds = []
            pages = ceil(len(contributions) / 10)
            for page in range(pages):
                page = page + 1
                p1 = (page - 1) * 10 if page > 1 else page - 1
                p2 = page * 10
                a = []
                for i, k in enumerate(sorted(stats, key=stats.get, reverse=True)[p1:p2]):
                    user_team = await self.get_user_with_team(ctx, k)
                    a.append(f"{i + p1 + 1}. {user_team[0].name} ({user_team[1]}) - {stats[k]}")
                embed = discord.Embed(
                    title="Top goal involvements (goals + assists) _({}/{})_".format(page, pages),
                    description="\n".join(a),
                    colour=0xFF0000,
                )
                embeds.append(embed)
        await menu(ctx, embeds, DEFAULT_CONTROLS)

    @nat_leaguestats.command(name="goals", alias=["topscorer", "topscorers"])
    async def nat__goals(self, ctx):
        """Players with the most goals."""
        stats = await self.config.guild(ctx.guild).nstats()
        stats = stats["goals"]
        if not stats:
            return await ctx.send("No stats available.")
        else:
            embeds = []
            pages = ceil(len(stats) / 10)
            for page in range(pages):
                page = page + 1
                p1 = (page - 1) * 10 if page > 1 else page - 1
                p2 = page * 10
                a = []
                for i, k in enumerate(sorted(stats, key=stats.get, reverse=True)[p1:p2]):
                    user_team = await self.get_user_with_team(ctx, k)
                    a.append(f"{i + p1 + 1}. {user_team[0].name} ({user_team[1]}) - {stats[k]}")
                embed = discord.Embed(
                    title="Top Scorers _({}/{})_".format(page, pages),
                    description="\n".join(a),
                    colour=0xFF0000,
                )
                embeds.append(embed)
        await menu(ctx, embeds, DEFAULT_CONTROLS)

    @nat_leaguestats.command(name="owngoals")
    async def nat__owngoals(self, ctx):
        """Players with the most own goals."""
        stats = await self.config.guild(ctx.guild).nstats()
        stats = stats["owngoals"]
        if not stats:
            return await ctx.send("No stats available.")
        else:
            embeds = []
            pages = ceil(len(stats) / 10)
            for page in range(pages):
                page = page + 1
                p1 = (page - 1) * 10 if page > 1 else page - 1
                p2 = page * 10
                a = []
                for i, k in enumerate(sorted(stats, key=stats.get, reverse=True)[p1:p2]):
                    user_team = await self.get_user_with_team(ctx, k)
                    a.append(f"{i+p1+1}. {user_team[0].name} ({user_team[1]}) - {stats[k]}")
                embed = discord.Embed(
                    title="Most Own Goals _({}/{})_".format(page, pages),
                    description="\n".join(a),
                    colour=0xFF0000,
                )
                embeds.append(embed)
        await menu(ctx, embeds, DEFAULT_CONTROLS)

    @nat_leaguestats.command(aliases=["yellowcards"])
    async def nat_yellows(self, ctx):
        """Players with the most yellow cards."""
        stats = await self.config.guild(ctx.guild).nstats()
        stats = stats["yellows"]
        if not stats:
            return await ctx.send("No stats available.")
        else:
            embeds = []
            pages = ceil(len(stats) / 10)
            for page in range(pages):
                page = page + 1
                p1 = (page - 1) * 10 if page > 1 else page - 1
                p2 = page * 10
                a = []
                for i, k in enumerate(sorted(stats, key=stats.get, reverse=True)[p1:p2]):
                    user_team = await self.get_user_with_team(ctx, k)
                    a.append(f"{i+p1+1}. {user_team[0].name} ({user_team[1]}) - {stats[k]}")
                embed = discord.Embed(
                    title="Most Yellow Cards _({}/{})_".format(page, pages),
                    description="\n".join(a),
                    colour=0xFF0000,
                )
                embeds.append(embed)
        await menu(ctx, embeds, DEFAULT_CONTROLS)

    @nat_leaguestats.command(alies=["redcards"])
    async def nat_reds(self, ctx):
        """Players with the most red cards."""
        stats = await self.config.guild(ctx.guild).nstats()
        stats = stats["reds"]
        if not stats:
            return await ctx.send("No stats available.")
        else:
            embeds = []
            pages = ceil(len(stats) / 10)
            for page in range(pages):
                page = page + 1
                p1 = (page - 1) * 10 if page > 1 else page - 1
                p2 = page * 10
                a = []
                for i, k in enumerate(sorted(stats, key=stats.get, reverse=True)[p1:p2]):
                    user_team = await self.get_user_with_team(ctx, k)
                    a.append(f"{i+p1+1}. {user_team[0].name} ({user_team[1]}) - {stats[k]}")
                embed = discord.Embed(
                    title="Most Red Cards _({}/{})_".format(page, pages),
                    description="\n".join(a),
                    colour=0xFF0000,
                )
                embeds.append(embed)
        await menu(ctx, embeds, DEFAULT_CONTROLS)

    @nat_leaguestats.command(alias=["motms"])
    async def nat_motm(self, ctx):
        """Players with the most MOTMs."""
        stats = await self.config.guild(ctx.guild).nstats()
        stats = stats["motm"]
        if not stats:
            return await ctx.send("No stats available.")
        else:
            embeds = []
            pages = ceil(len(stats) / 10)
            for page in range(pages):
                page = page + 1
                p1 = (page - 1) * 10 if page > 1 else page - 1
                p2 = page * 10
                a = []
                for i, k in enumerate(sorted(stats, key=stats.get, reverse=True)[p1:p2]):
                    user_team = await self.get_user_with_team(ctx, k)
                    a.append(f"{i+p1+1}. {user_team[0].name} ({user_team[1]}) - {stats[k]}")
                embed = discord.Embed(
                    title="Most MOTMs _({}/{})_".format(page, pages),
                    description="\n".join(a),
                    colour=0xFF0000,
                )
                embeds.append(embed)
        await menu(ctx, embeds, DEFAULT_CONTROLS)

    @nat_leaguestats.command(name="fouls", alias=["fouls"])
    async def nat_ls_fouls(self, ctx):
        """Players with the most fouls."""
        stats = await self.config.guild(ctx.guild).nstats()
        stats = stats["fouls"]
        if not stats:
            return await ctx.send("No stats available.")
        else:
            embeds = []
            pages = ceil(len(stats) / 10)
            for page in range(pages):
                page = page + 1
                p1 = (page - 1) * 10 if page > 1 else page - 1
                p2 = page * 10
                a = []
                for i, k in enumerate(sorted(stats, key=stats.get, reverse=True)[p1:p2]):
                    user_team = await self.get_user_with_team(ctx, k)
                    a.append(f"{i+p1+1}. {user_team[0].name} ({user_team[1]}) - {stats[k]}")
                embed = discord.Embed(
                    title="Most Fouls _({}/{})_".format(page, pages),
                    description="\n".join(a),
                    colour=0xFF0000,
                )
                embeds.append(embed)
        await menu(ctx, embeds, DEFAULT_CONTROLS)

    @nat_leaguestats.command(name="shots", alias=["shots"])
    async def nat_ls_shots(self, ctx):
        """Players with the most shots."""
        stats = await self.config.guild(ctx.guild).nstats()
        stats = stats["shots"]
        if not stats:
            return await ctx.send("No stats available.")
        else:
            embeds = []
            pages = ceil(len(stats) / 10)
            for page in range(pages):
                page = page + 1
                p1 = (page - 1) * 10 if page > 1 else page - 1
                p2 = page * 10
                a = []
                for i, k in enumerate(sorted(stats, key=stats.get, reverse=True)[p1:p2]):
                    user_team = await self.get_user_with_team(ctx, k)
                    a.append(f"{i+p1+1}. {user_team[0].name} ({user_team[1]}) - {stats[k]}")
                embed = discord.Embed(
                    title="Most Shots _({}/{})_".format(page, pages),
                    description="\n".join(a),
                    colour=0xFF0000,
                )
                embeds.append(embed)
        await menu(ctx, embeds, DEFAULT_CONTROLS)

    @nat_leaguestats.command()
    async def nat_penalties(self, ctx):
        """Penalties scored and missed statistics."""
        stats = await self.config.guild(ctx.guild).nstats()
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

    @nat_leaguestats.command()
    async def nat_assists(self, ctx):
        """Players with the most assists."""
        stats = await self.config.guild(ctx.guild).nstats()
        stats = stats["assists"]
        if not stats:
            return await ctx.send("No stats available.")
        else:
            embeds = []
            pages = ceil(len(stats) / 10)
            for page in range(pages):
                page = page + 1
                p1 = (page - 1) * 10 if page > 1 else page - 1
                p2 = page * 10
                a = []
                for i, k in enumerate(sorted(stats, key=stats.get, reverse=True)[p1:p2]):
                    user_team = await self.get_user_with_team(ctx, k)
                    a.append(f"{i+p1+1}. {user_team[0].name} ({user_team[1]}) - {stats[k]}")
                embed = discord.Embed(
                    title="Most Assists _({}/{})_".format(page, pages),
                    description="\n".join(a),
                    colour=0xFF0000,
                )
                embeds.append(embed)
        await menu(ctx, embeds, DEFAULT_CONTROLS)
