import discord
from redbot.core import checks, commands
from redbot.core.utils.chat_formatting import box

from .abc import MixinMeta
from .scheduler import Schedule
import math
import random
import asyncio
import re
from .functions import WEATHER

from datetime import datetime, timedelta


class SimthemeMixin(MixinMeta):
    """Simulation Theme Settings"""

    @checks.admin_or_permissions(manage_guild=True)
    @commands.group(autohelp=True)
    async def simtheme(self, ctx):
        """Simulation Theme Settings."""
        if ctx.invoked_subcommand is None:
            guild = ctx.guild
            # Display current theme settings
            theme = await self.config.guild(guild).theme()
            keys = list(theme.keys())
            msg = ""
            for key in keys:
                msg += "\n*{}\n".format(key)
                subkeys = list(theme[key].keys())
                for subkey in subkeys:
                    msg += "{}: {}\n".format(subkey, theme[key][subkey])
            await ctx.send(box(msg))

    async def regexcolor(self, ctx, color):
        if not re.search(r"^#(?:[0-9a-fA-F]{3}){1,2}$", color):
            msg = await ctx.send(f"Color {color} invalid. Please use hex colors (ie: #FFFFFF).")
            await msg.add_reaction("\U0000274c")
            return True

    @simtheme.command()
    async def background(self, ctx, color: str):
        """Events background color"""
        if not await self.regexcolor(ctx, color):
            async with self.config.guild(ctx.guild).theme() as theme:
                theme["general"]["bg_color"] = f"{color}"
                await ctx.tick()

    @simtheme.command()
    async def reset(self, ctx):
        """Resets all theme changes."""
        async with self.config.guild(ctx.guild).theme() as theme:
            theme["general"]["bg_color"] = (255, 255, 255, 0)

            theme["matchinfo"]["vs_title"] = (255, 255, 255, 255)
            theme["matchinfo"]["stadium"] = (255, 255, 255, 255)
            theme["matchinfo"]["commentator"] = (255, 255, 255, 255)
            theme["matchinfo"]["home_away_text"] = (255, 255, 255, 255)
            theme["matchinfo"]["odds"] = (255, 255, 255, 255)

            theme["walkout"]["name_text"] = (255, 255, 255, 255)

            theme["chances"]["header_text_bg"] = (230, 230, 230, 230)
            theme["chances"]["header_text_col"] = (110, 110, 110, 255)
            theme["chances"]["header_time_bg"] = "#AAA"
            theme["chances"]["header_time_col"] = (110, 110, 110, 255)
            theme["chances"]["desc_text_col"] = (240, 240, 240, 255)

            theme["goals"]["header_text_bg"] = (230, 230, 230, 230)
            theme["goals"]["header_text_col"] = (110, 110, 110, 255)
            theme["goals"]["header_time_bg"] = "#AAA"
            theme["goals"]["header_time_col"] = (110, 110, 110, 255)
            theme["goals"]["desc_text_col"] = (240, 240, 240, 255)

            theme["fouls"]["header_text_bg"] = (200, 200, 255, 255)
            theme["fouls"]["header_text_col"] = (110, 110, 110, 255)
            theme["fouls"]["header_time_bg"] = "#AAA"
            theme["fouls"]["header_time_col"] = (110, 110, 110, 255)
            theme["fouls"]["desc_text_col"] = (240, 240, 240, 255)
        await ctx.tick()

    @simtheme.group()
    async def chances(self, ctx):
        """Chances theme (commentaries)"""

    @chances.command(name="headerbg")
    async def headerbg(self, ctx, color: str):
        """Chances header background (commentaries)"""
        if not await self.regexcolor(ctx, color):
            async with self.config.guild(ctx.guild).theme() as theme:
                theme["chances"]["header_text_bg"] = f"{color}"
                await ctx.tick()

    @chances.command(name="headertxt")
    async def headertext(self, ctx, color: str):
        """Chances header text (commentaries)"""
        if not await self.regexcolor(ctx, color):
            async with self.config.guild(ctx.guild).theme() as theme:
                theme["chances"]["header_text_col"] = f"{color}"
                await ctx.tick()

    @chances.command(name="timebg")
    async def headertimebg(self, ctx, color: str):
        """Chances header time background (commentaries)"""
        if not await self.regexcolor(ctx, color):
            async with self.config.guild(ctx.guild).theme() as theme:
                theme["chances"]["header_time_bg"] = f"{color}"
                await ctx.tick()

    @chances.command(name="timetxt")
    async def headertimetext(self, ctx, color: str):
        """Chances header time text (commentaries)"""
        if not await self.regexcolor(ctx, color):
            async with self.config.guild(ctx.guild).theme() as theme:
                theme["chances"]["header_time_col"] = f"{color}"
                await ctx.tick()

    @chances.command(name="desc")
    async def cdescriptiontext(self, ctx, color: str):
        """Chances description text"""
        if not await self.regexcolor(ctx, color):
            async with self.config.guild(ctx.guild).theme() as theme:
                theme["chances"]["desc_text_col"] = f"{color}"
                await ctx.tick()

    @simtheme.group(name="goals")
    async def __goals(self, ctx):
        """Goals theme"""

    @__goals.command(name="headerbg")
    async def gheaderbg(self, ctx, color: str):
        """Goals header background color"""
        if not await self.regexcolor(ctx, color):
            async with self.config.guild(ctx.guild).theme() as theme:
                theme["goals"]["header_text_bg"] = f"{color}"
                await ctx.tick()

    @__goals.command(name="headertxt")
    async def gheadertext(self, ctx, color: str):
        """Goals header text color"""
        if not await self.regexcolor(ctx, color):
            async with self.config.guild(ctx.guild).theme() as theme:
                theme["goals"]["header_text_col"] = f"{color}"
                await ctx.tick()

    @__goals.command(name="timebg")
    async def gheadertimebg(self, ctx, color: str):
        """Goals header time background"""
        if not await self.regexcolor(ctx, color):
            async with self.config.guild(ctx.guild).theme() as theme:
                theme["goals"]["header_time_bg"] = f"{color}"
                await ctx.tick()

    @__goals.command(name="timetxt")
    async def gheadertimetext(self, ctx, color: str):
        """Goals header time text"""
        if not await self.regexcolor(ctx, color):
            async with self.config.guild(ctx.guild).theme() as theme:
                theme["goals"]["header_time_col"] = f"{color}"
                await ctx.tick()

    @__goals.command(name="desc")
    async def gdescriptiontext(self, ctx, color: str):
        """Goals description text"""
        if not await self.regexcolor(ctx, color):
            async with self.config.guild(ctx.guild).theme() as theme:
                theme["goals"]["desc_text_col"] = f"{color}"
                await ctx.tick()

    @simtheme.group()
    async def fouls(self, ctx):
        """Fouls theme"""

    @fouls.command(name="headerbg")
    async def fheaderbg(self, ctx, color: str):
        """Fouls header background"""
        if not await self.regexcolor(ctx, color):
            async with self.config.guild(ctx.guild).theme() as theme:
                theme["fouls"]["header_text_bg"] = f"{color}"
                await ctx.tick()

    @fouls.command(name="headertxt")
    async def fheadertext(self, ctx, color: str):
        """Fouls header text"""
        if not await self.regexcolor(ctx, color):
            async with self.config.guild(ctx.guild).theme() as theme:
                theme["fouls"]["header_text_col"] = f"{color}"
                await ctx.tick()

    @fouls.command(name="timebg")
    async def fheadertimebg(self, ctx, color: str):
        """Fouls header time background"""
        if not await self.regexcolor(ctx, color):
            async with self.config.guild(ctx.guild).theme() as theme:
                theme["fouls"]["header_time_bg"] = f"{color}"
                await ctx.tick()

    @fouls.command(name="timetxt")
    async def fheadertimetext(self, ctx, color: str):
        """Fouls header time text"""
        if not await self.regexcolor(ctx, color):
            async with self.config.guild(ctx.guild).theme() as theme:
                theme["fouls"]["header_time_col"] = f"{color}"
                await ctx.tick()

    @fouls.command(name="desc")
    async def fdescriptiontext(self, ctx, color: str):
        """Fouls description text"""
        if not await self.regexcolor(ctx, color):
            async with self.config.guild(ctx.guild).theme() as theme:
                theme["fouls"]["desc_text_col"] = f"{color}"
                await ctx.tick()

    @simtheme.group(name="walkout")
    async def _walkout(self, ctx):
        """Walkout theme"""

    @_walkout.command(name="players")
    async def wplayers(self, ctx, color: str):
        """Walkout player names"""
        if not await self.regexcolor(ctx, color):
            async with self.config.guild(ctx.guild).theme() as theme:
                theme["walkout"]["name_text"] = f"{color}"
                await ctx.tick()

    @simtheme.group(name="matchinfo")
    async def _matchinfo(self, ctx):
        """Match info theme"""

    @_matchinfo.command(name="vstitle")
    async def mvstitle(self, ctx, color: str):
        """Match info Team1 vs Team2."""
        if not await self.regexcolor(ctx, color):
            async with self.config.guild(ctx.guild).theme() as theme:
                theme["matchinfo"]["vs_title"] = f"{color}"
                await ctx.tick()

    @_matchinfo.command(name="stadium")
    async def mstadium(self, ctx, color: str):
        """Match info stadium."""
        if not await self.regexcolor(ctx, color):
            async with self.config.guild(ctx.guild).theme() as theme:
                theme["matchinfo"]["stadium"] = f"{color}"
                await ctx.tick()

    @_matchinfo.command(name="commentator")
    async def mcommentator(self, ctx, color: str):
        """Match info commentator."""
        if not await self.regexcolor(ctx, color):
            async with self.config.guild(ctx.guild).theme() as theme:
                theme["matchinfo"]["commentator"] = f"{color}"
                await ctx.tick()

    @_matchinfo.command(name="ha")
    async def mhomeaway(self, ctx, color: str):
        """Match info home/away text."""
        if not await self.regexcolor(ctx, color):
            async with self.config.guild(ctx.guild).theme() as theme:
                theme["matchinfo"]["home_away_text"] = f"{color}"
                await ctx.tick()

    @_matchinfo.command(name="odds")
    async def modds(self, ctx, color: str):
        """Match odds text."""
        if not await self.regexcolor(ctx, color):
            async with self.config.guild(ctx.guild).theme() as theme:
                theme["matchinfo"]["odds"] = f"{color}"
                await ctx.tick()

    @simtheme.group(name="preview")
    async def preview(self, ctx):
        """Preview theme"""

    @preview.command(name="goal")
    async def pgoal(self, ctx):
        """Preview goal."""
        min = random.randint(1, 90)
        teams = await self.config.guild(ctx.guild).teams()
        team1 = list(teams.keys())[random.randint(0, len(teams) - 1)]
        team2 = list(teams.keys())[random.randint(0, len(teams) - 1)]
        score1 = random.randint(1, 5)
        score2 = random.randint(1, 5)
        user = await self.bot.fetch_user(ctx.author.id)
        image = await self.simpic(
            ctx,
            str(min),
            "goal",
            user,
            team1,
            team2,
            random.choice([team1, team2]),
            score1,
            score2,
            user,
        )
        await ctx.send(file=image)

    @preview.command(name="yellow")
    async def pyellow(self, ctx):
        """Preview yellow card."""
        min = random.randint(1, 90)
        teams = await self.config.guild(ctx.guild).teams()
        team1 = list(teams.keys())[random.randint(0, len(teams) - 1)]
        team2 = list(teams.keys())[random.randint(0, len(teams) - 1)]
        score1 = random.randint(1, 5)
        score2 = random.randint(1, 5)
        user = await self.bot.fetch_user(ctx.author.id)
        image = await self.simpic(
            ctx,
            str(min),
            "yellow",
            user,
            team1,
            team2,
            random.choice([team1, team2]),
            score1,
            score2,
            user,
        )
        await ctx.send(file=image)

    @preview.command(name="2yellow")
    async def p2yellow(self, ctx):
        """Preview second yellow card."""
        min = random.randint(1, 90)
        teams = await self.config.guild(ctx.guild).teams()
        team1 = list(teams.keys())[random.randint(0, len(teams) - 1)]
        team2 = list(teams.keys())[random.randint(0, len(teams) - 1)]
        score1 = random.randint(1, 5)
        score2 = random.randint(1, 5)
        user = await self.bot.fetch_user(ctx.author.id)
        image = await self.simpic(
            ctx,
            str(min),
            "2yellow",
            user,
            team1,
            team2,
            random.choice([team1, team2]),
            score1,
            score2,
            user,
        )
        await ctx.send(file=image)

    @preview.command(name="red")
    async def pred(self, ctx):
        """Preview red card."""
        min = random.randint(1, 90)
        teams = await self.config.guild(ctx.guild).teams()
        team1 = list(teams.keys())[random.randint(0, len(teams) - 1)]
        team2 = list(teams.keys())[random.randint(0, len(teams) - 1)]
        score1 = random.randint(1, 5)
        score2 = random.randint(1, 5)
        user = await self.bot.fetch_user(ctx.author.id)
        image = await self.simpic(
            ctx,
            str(min),
            "red",
            user,
            team1,
            team2,
            random.choice([team1, team2]),
            score1,
            score2,
            user,
            random.randint(1, 3),
        )
        await ctx.send(file=image)

    @preview.command(name="corner")
    async def pcorner(self, ctx, score=False):
        """Preview corner."""
        min = random.randint(1, 90)
        teams = await self.config.guild(ctx.guild).teams()
        team1 = list(teams.keys())[random.randint(0, len(teams) - 1)]
        team2 = list(teams.keys())[random.randint(0, len(teams) - 1)]
        score1 = random.randint(1, 5)
        score2 = random.randint(1, 5)
        user = await self.bot.fetch_user(ctx.author.id)
        event = "cornerscore" if score == True else "cornermiss"
        image = await self.cornerimg(ctx, team1, str(min), user)
        await ctx.send(file=image)
        image = await self.simpic(
            ctx, str(min), event, user, team1, team2, team1, score1, score2, user,
        )
        await ctx.send(file=image)

    @preview.command(name="penalty")
    async def ppenalty(self, ctx, score=False):
        """Preview penalty."""
        min = random.randint(1, 90)
        teams = await self.config.guild(ctx.guild).teams()
        team1 = list(teams.keys())[random.randint(0, len(teams) - 1)]
        team2 = list(teams.keys())[random.randint(0, len(teams) - 1)]
        score1 = random.randint(1, 5)
        score2 = random.randint(1, 5)
        user = await self.bot.fetch_user(ctx.author.id)
        event = "penscore" if score == True else "penmiss"
        image = await self.penaltyimg(ctx, team1, str(min), user)
        await ctx.send(file=image)
        image = await self.simpic(
            ctx, str(min), event, user, team1, team2, team1, score1, score2, user,
        )
        await ctx.send(file=image)

    @preview.command(name="foul")
    async def pfoul(self, ctx):
        """Preview fouls"""
        min = random.randint(1, 90)
        teams = await self.config.guild(ctx.guild).teams()
        team = list(teams.keys())[random.randint(0, len(teams) - 1)]
        user = await self.bot.fetch_user(ctx.author.id)
        image = await self.commentimg(ctx, team, str(min), user, 1)
        await ctx.send(file=image)

    @preview.command(name="chance")
    async def pchance(self, ctx):
        """Preview chance."""
        min = random.randint(1, 90)
        teams = await self.config.guild(ctx.guild).teams()
        team = list(teams.keys())[random.randint(0, len(teams) - 1)]
        user = await self.bot.fetch_user(ctx.author.id)
        image = await self.commentimg(ctx, team, str(min), user, 0)
        await ctx.send(file=image)

    @preview.command(name="motm")
    async def pmotm(self, ctx):
        """Preview MOTM."""
        teams = await self.config.guild(ctx.guild).teams()
        team = list(teams.keys())[random.randint(0, len(teams) - 1)]
        user = await self.bot.fetch_user(ctx.author.id)
        image = await self.motmpic(ctx, user, team, random.randint(0, 3), random.randint(0, 3),)
        await ctx.send(file=image)

    @preview.command(name="walkout")
    async def pwalkout(self, ctx):
        """Preview walkout."""
        teams = await self.config.guild(ctx.guild).teams()
        team = list(teams.keys())[random.randint(0, len(teams) - 1)]
        home_or_away = random.choice(["home", "away"])
        image = await self.walkout(ctx, team, home_or_away,)
        await ctx.send(file=image)

    @preview.command(name="matchinfo")
    async def pmatchinfo(self, ctx):
        """Preview match info."""
        teams = await self.config.guild(ctx.guild).teams()
        team1 = list(teams.keys())[random.randint(0, len(teams) - 1)]
        team2 = list(teams.keys())[random.randint(0, len(teams) - 1)]
        homewin = random.uniform(0.1, 5)
        awaywin = random.uniform(0.1, 5)
        draw = homewin / awaywin
        stadium = teams[team1]["stadium"] if teams[team1]["stadium"] is not None else None
        weather = random.choice(WEATHER)
        image = await self.matchinfo(
            ctx, [team1, team2], weather, stadium, homewin, awaywin, draw,
        )
        await ctx.send(file=image)

    @preview.command(name="matchstats")
    async def pmatchstats(self, ctx):
        """Preview match stats."""
        teams = await self.config.guild(ctx.guild).teams()
        team1 = list(teams.keys())[random.randint(0, len(teams) - 1)]
        team2 = list(teams.keys())[random.randint(0, len(teams) - 1)]
        score = (random.randint(0, 4), random.randint(0, 4))
        yellow = (random.randint(0, 3), random.randint(0, 3))
        red = (random.randint(0, 1), random.randint(0, 1))
        chances = (random.randint(1, 10), random.randint(1, 10))
        fouls = (random.randint(3, 15), random.randint(3, 15))
        image = await self.matchstats(ctx, team1, team2, score, yellow, red, chances, fouls)
        await ctx.send(file=image)
