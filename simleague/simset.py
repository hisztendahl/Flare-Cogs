import discord
from redbot.core import checks, commands
from redbot.core.utils.chat_formatting import box

from .abc import MixinMeta
from .scheduler import Schedule
import math
import random
import asyncio

from datetime import datetime, timedelta


class Name:
    title: str
    parsed: str


class SimsetMixin(MixinMeta):
    """Simulation Settings"""

    @checks.admin_or_permissions(manage_guild=True)
    @commands.group(autohelp=True)
    async def simset(self, ctx):
        """Simulation Settings."""
        if ctx.invoked_subcommand is None:
            guild = ctx.guild
            # Display current settings
            gametime = await self.config.guild(guild).gametime()
            htbreak = await self.config.guild(guild).htbreak()
            results = await self.config.guild(guild).resultchannel()
            bettoggle = await self.config.guild(guild).bettoggle()
            maxplayers = await self.config.guild(guild).maxplayers()
            redcardmodif = await self.config.guild(guild).redcardmodifier()
            transfers = await self.config.guild(guild).transferwindow()
            mentions = await self.config.guild(guild).mentions()
            msg = ""
            msg += "Game Time: 1m for every {}s.\n".format(gametime)
            msg += "Team Limit: {} players.\n".format(maxplayers)
            msg += "HT Break: {}s.\n".format(htbreak)
            msg += "Red Card Modifier: {}% loss per red card.\n".format(redcardmodif)
            msg += "Posting Results: {}.\n".format("Yes" if results else "No")
            msg += "Transfer Window: {}.\n".format("Open" if transfers else "Closed")
            msg += "Accepting Bets: {}.\n".format("Yes" if bettoggle else "No")
            msg += "Mentions on game start: {}.\n".format("Yes" if mentions else "No")

            if bettoggle:
                bettime = await self.config.guild(guild).bettime()
                betmax = await self.config.guild(guild).betmax()
                betmin = await self.config.guild(guild).betmin()
                msg += "Bet Time: {}s.\n".format(bettime)
                msg += "Max Bet: {}.\n".format(betmax)
                msg += "Min Bet: {}.\n".format(betmin)
            await ctx.send(box(msg))

    @checks.admin_or_permissions(manage_guild=True)
    @simset.group(autohelp=True)
    async def bet(self, ctx):
        """Simulation Betting Settings."""

    @checks.admin_or_permissions(manage_guild=True)
    @simset.group(autohelp=True, hidden=True)
    async def probability(self, ctx):
        """Simulation Probability Settings. May break the cog if changed."""
        if ctx.invoked_subcommand is None:
            proba = await self.config.guild(ctx.guild).probability()
            goals = proba["goalchance"]
            owngoals = proba["owngoalchance"]
            yellow = proba["yellowchance"]
            red = proba["redchance"]
            penalty = proba["penaltychance"]
            penaltyblock = proba["penaltyblock"]
            freekick = proba["freekickchance"]
            freekickblock = proba["freekickblock"]
            corner = proba["cornerchance"]
            cornerblock = proba["cornerblock"]
            var = proba["varchance"]
            varsuccess = proba["varsuccess"]
            comment = proba["commentchance"]
            msg = "/!\\ This has the chance to break the game completely, no support is offered. \n\n"
            msg += "Goal Chance: {}.\n".format(goals)
            msg += "Own Goal Chance: {}.\n".format(owngoals)
            msg += "Yellow Card Chance: {}.\n".format(yellow)
            msg += "Red Card Chance: {}.\n".format(red)
            msg += "Penalty Chance: {}.\n".format(penalty)
            msg += "Penalty Block Chance: {}.\n".format(penaltyblock)
            msg += "Free Kick Chance: {}.\n".format(freekick)
            msg += "Free Kick Block Chance: {}.\n".format(freekickblock)
            msg += "Corner Chance: {}.\n".format(corner)
            msg += "Corner Block Chance: {}.\n".format(cornerblock)
            msg += "VAR Chance: {}.\n".format(var)
            msg += "VAR Success Chance: {}.\n".format(varsuccess)
            msg += "Commentary Chance: {}.\n".format(comment)
            await ctx.send(box(msg))

    @probability.command()
    async def goals(self, ctx, amount: int = 96):
        """Goal probability. Default = 96"""
        if amount > 100 or amount < 1:
            return await ctx.send("Amount must be greater than 0 and less than 100.")
        async with self.config.guild(ctx.guild).probability() as probability:
            probability["goalchance"] = amount
        await ctx.tick()

    @probability.command()
    async def owngoals(self, ctx, amount: int = 399):
        """Own Goal probability. Default = 399"""
        if amount > 400 or amount < 1:
            return await ctx.send("Amount must be greater than 0 and less than 400.")
        async with self.config.guild(ctx.guild).probability() as probability:
            probability["owngoalchance"] = amount
        await ctx.tick()

    @probability.command()
    async def yellow(self, ctx, amount: int = 98):
        """Yellow Card probability. Default = 98"""
        if amount > 100 or amount < 1:
            return await ctx.send("Amount must be greater than 0 and less than 100.")
        async with self.config.guild(ctx.guild).probability() as probability:
            probability["yellowchance"] = amount
        await ctx.tick()

    @simset.command()
    async def maxplayers(self, ctx, amount: int):
        """Set the max team players."""
        if amount < 3 or amount > 7:
            return await ctx.send("Amount must be between 3 and 7.")
        await self.config.guild(ctx.guild).maxplayers.set(amount)
        await ctx.tick()

    @simset.command()
    async def redcardmodifier(self, ctx, amount: int):
        """Set the the handicap per red card."""
        if amount < 1 or amount > 30:
            return await ctx.send("Amount must be between 1 and 30.")
        await self.config.guild(ctx.guild).redcardmodifier.set(amount)
        await ctx.tick()

    @simset.command()
    async def addstat(self, ctx, param=None):
        """Add standings stat keys."""
        teams = await self.config.guild(ctx.guild).teams()
        headers = [
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
        if param not in headers:
            return await ctx.send(f"Stat to add must be one of {', '.join(headers)}.")
        for team in teams:
            async with self.config.guild(ctx.guild).standings() as standings:
                stats = standings[team].keys()
                if param not in stats:
                    standings[team][param] = 0
                else:
                    await ctx.send(f"Stat '{param}' already exists (league).")
            async with self.config.guild(ctx.guild).cupstandings() as cupstandings:
                if team not in cupstandings:
                    cupstandings[team] = {
                        "played": 0,
                        "wins": 0,
                        "losses": 0,
                        "points": 0,
                        "gd": 0,
                        "gf": 0,
                        "ga": 0,
                        "draws": 0,
                        "reds": 0,
                        "yellows": 0,
                        "fouls": 0,
                        "chances": 0,
                    }
                else:
                    stats = cupstandings[team].keys()
                    if param not in stats:
                        cupstandings[team][param] = 0
                    else:
                        await ctx.send(f"Stat '{param}' already exists (cup).")
        await ctx.tick()

    @probability.command()
    async def red(self, ctx, amount: int = 398):
        """Red Card probability. Default = 398"""
        if amount > 400 or amount < 1:
            return await ctx.send("Amount must be greater than 0 and less than 400.")
        async with self.config.guild(ctx.guild).probability() as probability:
            probability["redchance"] = amount
        await ctx.tick()

    @probability.command()
    async def penalty(self, ctx, amount: int = 249):
        """Penalty Chance probability. Default = 249"""
        if amount > 250 or amount < 1:
            return await ctx.send("Amount must be greater than 0 and less than 250.")
        async with self.config.guild(ctx.guild).probability() as probability:
            probability["penaltychance"] = amount
        await ctx.tick()

    @probability.command()
    async def penaltyblock(self, ctx, amount: int = 75):
        """Penalty Block probability. Default = 75"""
        if amount > 100 or amount < 0:
            return await ctx.send("Amount must be greater than 0 and less than 100.")
        async with self.config.guild(ctx.guild).probability() as probability:
            probability["penaltyblock"] = amount
        await ctx.tick()

    @probability.command()
    async def corner(self, ctx, amount: int = 98):
        """Corner Chance probability. Default = 98"""
        if amount > 100 or amount < 1:
            return await ctx.send("Amount must be greater than 0 and less than 100.")
        async with self.config.guild(ctx.guild).probability() as probability:
            probability["cornerchance"] = amount
        await ctx.tick()

    @probability.command()
    async def cornerblock(self, ctx, amount: int = 20):
        """Corner Block probability. Default = 20"""
        if amount > 100 or amount < 0:
            return await ctx.send("Amount must be greater than 0 and less than 100.")
        async with self.config.guild(ctx.guild).probability() as probability:
            probability["cornerblock"] = amount
        await ctx.tick()

    @probability.command()
    async def freekick(self, ctx, amount: int = 98):
        """Free Kick Chance probability. Default = 98"""
        if amount > 100 or amount < 1:
            return await ctx.send("Amount must be greater than 0 and less than 100.")
        async with self.config.guild(ctx.guild).probability() as probability:
            probability["freekickchance"] = amount
        await ctx.tick()

    @probability.command()
    async def freekickblock(self, ctx, amount: int = 15):
        """Free Kick Block probability. Default = 15"""
        if amount > 100 or amount < 0:
            return await ctx.send("Amount must be greater than 0 and less than 100.")
        async with self.config.guild(ctx.guild).probability() as probability:
            probability["freekickblock"] = amount
        await ctx.tick()

    @probability.command()
    async def var(self, ctx, amount: int = 50):
        """VAR Chance probability. Default = 50"""
        if amount > 100 or amount < 1:
            return await ctx.send("Amount must be greater than 0 and less than 100.")
        async with self.config.guild(ctx.guild).probability() as probability:
            probability["varchance"] = amount
        await ctx.tick()

    @probability.command()
    async def varsuccess(self, ctx, amount: int = 50):
        """VAR Success Chance probability. Default = 50"""
        if amount > 100 or amount < 1:
            return await ctx.send("Amount must be greater than 0 and less than 100.")
        async with self.config.guild(ctx.guild).probability() as probability:
            probability["varsuccess"] = amount
        await ctx.tick()

    @probability.command()
    async def commentchance(self, ctx, amount: int = 85):
        """Commentary Chance probability. Default = 85"""
        if amount > 100 or amount < 1:
            return await ctx.send("Amount must be greater than 0 and less than 100.")
        async with self.config.guild(ctx.guild).probability() as probability:
            probability["commentchance"] = amount
        await ctx.tick()

    @bet.command()
    async def time(self, ctx, time: int = 180):
        """Set the time allowed for betting - 600 seconds is the max, 180 is default."""
        if time < 0 or time > 600:
            time = 180
        await self.config.guild(ctx.guild).bettime.set(time)
        await ctx.tick()

    @bet.command()
    async def max(self, ctx, amount: int):
        """Set the max amount for betting."""
        if amount < 1:
            return await ctx.send("Amount must be greater than 0.")
        await self.config.guild(ctx.guild).betmax.set(amount)
        await ctx.tick()

    @bet.command()
    async def min(self, ctx, amount: int):
        """Set the min amount for betting."""
        if amount < 1:
            return await ctx.send("Amount must be greater than 0.")
        await self.config.guild(ctx.guild).betmin.set(amount)
        await ctx.tick()

    @bet.command()
    async def toggle(self, ctx, toggle: bool):
        """Set if betting is enabled or not.
        Toggle must be a valid bool."""
        await self.config.guild(ctx.guild).bettoggle.set(toggle)
        await ctx.tick()

    @simset.command()
    async def gametime(self, ctx, time: float = 1):
        """Set the time each minute takes - 5 seconds is the max. 1 is default."""
        if time < 0 or time > 5:
            time = 90
        await self.config.guild(ctx.guild).gametime.set(time)
        await ctx.tick()

    @simset.command()
    async def halftimebreak(self, ctx, time: int = 1):
        """Set the half time break - 20 seconds is the max. 5 is default."""
        if time < 0 or time > 20:
            time = 5
        await self.config.guild(ctx.guild).htbreak.set(time)
        await ctx.tick()

    @simset.command()
    async def resultchannel(self, ctx, channel: discord.TextChannel):
        """Add a channel for automatic result posting."""
        channels = await self.config.guild(ctx.guild).resultchannel()
        for c in channels:
            if c == channel.id:
                await ctx.send("Results are already posted in this channel")
                return

        channels.append(channel.id)
        await self.config.guild(ctx.guild).resultchannel.set(channels)
        await ctx.tick()

    @simset.command()
    async def resultchannels(self, ctx, option: str):
        """Show or clear all result channels."""
        if option == "clear":
            await self.config.guild(ctx.guild).resultchannel.set([])
            await ctx.tick()
        elif option == "show":
            async with self.config.guild(ctx.guild).resultchannel() as result:
                a = []
                for res in result:
                    channel = ctx.guild.get_channel(res).name
                    a.append(channel)
                embed = discord.Embed(
                    title="Result channels", description="\n".join(a), colour=0xFF0000
                )
                await ctx.send(embed=embed)
        else:
            await ctx.send("No parameter for resultchannels, you must choose 'show' or 'clear'")

    @simset.command()
    async def transferchannel(self, ctx, channel: discord.TextChannel):
        """Add a channel for automatic transfer posting."""
        async with self.config.guild(ctx.guild).transferchannel() as channels:
            if channel.id in channels:
                await ctx.send("Transfers are already posted in this channel")
                return

            channels.append(channel.id)
        await ctx.tick()

    @simset.command()
    async def transferchannels(self, ctx, option: str):
        """Show or clear all transfer channels."""
        if option == "clear":
            await self.config.guild(ctx.guild).transferchannel.set([])
            await ctx.tick()
        elif option == "show":
            async with self.config.guild(ctx.guild).transferchannel() as result:
                a = []
                for res in result:
                    channel = ctx.guild.get_channel(res)
                    if channel is not None:
                        a.append(channel.name)
                embed = discord.Embed(
                    title="Transfer channels", description="\n".join(a), colour=0xFF0000
                )
                await ctx.send(embed=embed)
        else:
            await ctx.send("No parameter for transferchannels, you must choose 'show' or 'clear'")

    @simset.command()
    async def window(self, ctx, status: str):
        """Open or close the transfer window."""
        if status.lower() not in ["open", "close"]:
            return await ctx.send("You must specify either 'open' or 'close'.")
        if status == "open":
            standings = await self.config.guild(ctx.guild).standings()
            sortedstandings = sorted(
                standings,
                key=lambda team: (
                    standings[team]["points"],
                    standings[team]["gd"],
                    standings[team]["gf"],
                ),
            )
            firstteam = None
            for i, team in enumerate(sortedstandings):
                async with self.config.guild(ctx.guild).transfers() as transfers:
                    if i == 0:
                        firstteam = team
                    transfers[team] = {
                        "ready": True if i == 0 else False,
                        "locked": None,
                        "swap": {"in": None, "out": None},
                        "sign": {"in": None, "out": None},
                    }
            await self.config.guild(ctx.guild).transferwindow.set(True)
            await ctx.send(
                "Transfer window is now open. Transfers will start with {}".format(firstteam)
            )
        else:
            await self.config.guild(ctx.guild).transferwindow.set(False)
            await ctx.send("Transfer window is now closed.")

    @simset.command()
    async def lockwindow(self, ctx, status: str):
        """Open or close the contract extension window."""
        if status.lower() not in ["open", "close"]:
            return await ctx.send("You must specify either 'open' or 'close'.")
        if status == "open":
            await self.config.guild(ctx.guild).extensionwindow.set(True)
            await ctx.send(
                "Extension window is now open. You can now pick a player to extend for this season."
            )
        else:
            await self.config.guild(ctx.guild).extensionwindow.set(False)
            await ctx.send("Extension window is now closed.")

    @simset.command()
    async def mentions(self, ctx, bool: bool):
        """Toggle mentions on game start."""
        if bool:
            await self.config.guild(ctx.guild).mentions.set(True)
        else:
            await self.config.guild(ctx.guild).mentions.set(False)

    @simset.command(name="updatecache")
    async def levels_updatecache(self, ctx):
        """Update the level cache."""
        async with ctx.typing():
            await self.updatecacheall(ctx.guild)
        await ctx.tick()

    @simset.command()
    @commands.bot_has_permissions(manage_roles=True)
    async def createroles(self, ctx):
        """Create roles for teams and captains."""
        roles = await ctx.guild.fetch_roles()
        cptrole = [r for r in roles if r.name == "Sim Captain"]
        cptrole = await ctx.guild.create_role(name="Sim Captain") if not cptrole else cptrole[0]

        async with self.config.guild(ctx.guild).teams() as teams:
            for team in teams:
                if teams[team]["role"] is None:
                    role = await ctx.guild.create_role(name=team)
                    teams[team]["role"] = role.id

                teamcaptain = teams[team]["captain"]
                captainid = list(teamcaptain.keys())[0]
                member = ctx.guild.get_member(int(captainid))
                if member is not None:
                    await ctx.send(f"Assigning {cptrole.name} to {member.name}")
                    await member.add_roles(cptrole)
        await ctx.tick()

    @simset.command()
    @commands.bot_has_permissions(manage_roles=True)
    async def updateroles(self, ctx):
        """Update roles for teammembers."""
        teams = await self.config.guild(ctx.guild).teams()
        for team in teams:
            if teams[team]["role"] is None:
                self.log.debug(f"Skipping {team}, no role found.")
                continue
            role = ctx.guild.get_role(teams[team]["role"])
            for user in teams[team]["members"]:
                member = ctx.guild.get_member(int(user))
                if member is None:
                    await ctx.send("Could not find user {}.".format(user))
                else:
                    await member.add_roles(role)
        await ctx.tick()

    @simset.command()
    @commands.bot_has_permissions(manage_roles=True)
    async def clearform(self, ctx, team=None):
        """Clear streak form for a team or all teams."""
        cog = self.bot.get_cog("SimLeague")
        async with cog.config.guild(ctx.guild).teams() as teams:
            if team is not None:
                if team not in teams:
                    return await ctx.send("This team does not exist.")
                teams[team]["form"] = {"result": None, "streak": 0}
            else:
                for t in teams:
                    teams[t]["form"] = {"result": None, "streak": 0}
            await ctx.tick()

    @simset.command()
    async def createfixtures(self, ctx):
        """Create the fixtures for the current teams."""
        teams = await self.config.guild(ctx.guild).teams()
        teams = list(teams.keys())
        random.shuffle(teams)
        if len(teams) % 2:
            teams.append("DAY OFF")
        n = len(teams)
        matchs = []
        fixtures = []
        return_matchs = []
        for fixture in range(1, n):
            for i in range(n // 2):
                matchs.append((teams[i], teams[n - 1 - i]))
                return_matchs.append((teams[n - 1 - i], teams[i]))
            teams.insert(1, teams.pop())
            fixtures.insert(len(fixtures) // 2, matchs)
            fixtures.append(return_matchs)
            matchs = []
            return_matchs = []

        a = []
        for k, fixture in enumerate(fixtures, 1):
            a.append(f"Week {k}\n----------")
            for i, game in enumerate(fixture, 1):
                a.append(f"Game {i}: {game[0]} vs {game[1]}")
            a.append("----------")

        await self.config.guild(ctx.guild).fixtures.set(fixtures)
        await ctx.tick()

    @simset.command()
    async def drawcupround(self, ctx, *teambyes):
        """Draws the current round of Sim Cup."""
        teams = await self.config.guild(ctx.guild).teams()
        if len(teambyes):
            for t in list(teambyes):
                if t not in teams:
                    return await ctx.send("{} is not a valid team.".format(t))
        cupgames = await self.config.guild(ctx.guild).cupgames()
        async with ctx.typing():
            if len(cupgames):
                keys = list(cupgames.keys())
                if [keys[len(keys) - 1]][0] == "2":
                    return await ctx.send("There is no more game to draw!")
                lastround = cupgames[keys[len(keys) - 1]]
                unplayedgames = [
                    game
                    for game in lastround
                    if (game["score1"] + game["penscore1"]) == (game["score2"] + game["penscore2"])
                    and game["team2"] != "BYE"
                ]
                isroundover = False if len(unplayedgames) else True
                if not isroundover:
                    return await ctx.send(
                        "You need to finish the current round before drawing the next."
                    )
                winners = [
                    game["team1"]
                    if (game["score1"] + game["penscore1"]) > (game["score2"] + game["penscore2"])
                    or game["team2"] == "BYE"
                    else game["team2"]
                    for game in lastround
                ]
                teams = {k: v for k, v in teams.items() if k in winners}
                if len(teams):
                    roundsize = 2 ** math.ceil(math.log2(len(teams)))
                    drawables = [x for x in teams]

                    n = len(drawables)
                    fixtures = []
                    for i in range(n // 2):
                        draw = []
                        msg = await ctx.send("Game {}:".format(i + 1))
                        rdteam1 = random.choice(drawables)
                        drawables = [x for x in drawables if x is not rdteam1]
                        rdteam1mention = ctx.guild.get_role(teams[rdteam1]["role"]).mention
                        await msg.edit(content="Game {}: {} vs ...".format(i + 1, rdteam1mention))
                        rdteam2 = random.choice(drawables)
                        rdteam2mention = ctx.guild.get_role(teams[rdteam2]["role"]).mention
                        await asyncio.sleep(5)
                        await msg.edit(
                            content="Game {}: {} vs {}!".format(
                                i + 1, rdteam1mention, rdteam2mention
                            )
                        )
                        draw.append(
                            {
                                "team1": rdteam1,
                                "score1": 0,
                                "penscore1": 0,
                                "team2": rdteam2,
                                "score2": 0,
                                "penscore2": 0,
                            }
                        )
                        fixtures.append(
                            {
                                "team1": rdteam1,
                                "score1": 0,
                                "penscore1": 0,
                                "team2": rdteam2,
                                "score2": 0,
                                "penscore2": 0,
                            }
                        )
                        drawables = [x for x in drawables if x is not rdteam2]
                        await asyncio.sleep(5)

                    async with self.config.guild(ctx.guild).cupgames() as cupgames:
                        cupgames[str(roundsize)] = fixtures
            else:
                # Get seeds and start draw
                standings = await self.config.guild(ctx.guild).standings()
                sortedstandings = sorted(
                    standings,
                    key=lambda team: (
                        standings[team]["points"],
                        standings[team]["gd"],
                        standings[team]["gf"],
                    ),
                    reverse=True,
                )
                byes = []
                if len(teambyes):
                    sortedstandings = [x for x in teams if x not in teambyes]
                    byes = list(teambyes)
                if len(teams):
                    roundsize = 2 ** math.ceil(math.log2(len(teams)))
                    drawables = []
                    for idx, team in enumerate(sortedstandings):
                        if idx < (roundsize - len(teams) - len(teambyes)):
                            byes.append(team)
                        else:
                            drawables.append(team)

                    n = len(drawables)
                    fixtures = []
                    byementions = []
                    for bye in byes:
                        fixtures.append(
                            {
                                "team1": bye,
                                "score1": 0,
                                "penscore1": 0,
                                "team2": "BYE",
                                "score2": 0,
                                "penscore2": 0,
                            }
                        )
                        byemention = ctx.guild.get_role(teams[bye]["role"]).mention
                        byementions.append(byemention)

                    if len(byes):
                        await ctx.send(
                            "Teams directly qualified for the next round: {}".format(
                                ", ".join(byementions)
                            )
                        )
                        await asyncio.sleep(5)

                    for i in range(n // 2):
                        draw = []
                        msg = await ctx.send("Game {}:".format(i + 1))
                        rdteam1 = random.choice(drawables)
                        drawables = [x for x in drawables if x is not rdteam1]
                        rdteam1mention = ctx.guild.get_role(teams[rdteam1]["role"]).mention
                        await msg.edit(content="Game {}: {} vs ...".format(i + 1, rdteam1mention))
                        rdteam2 = random.choice(drawables)
                        rdteam2mention = ctx.guild.get_role(teams[rdteam2]["role"]).mention
                        await asyncio.sleep(5)
                        await msg.edit(
                            content="Game {}: {} vs {}!".format(
                                i + 1, rdteam1mention, rdteam2mention
                            )
                        )
                        draw.append(
                            {
                                "team1": rdteam1,
                                "score1": 0,
                                "penscore1": 0,
                                "team2": rdteam2,
                                "score2": 0,
                                "penscore2": 0,
                            }
                        )
                        fixtures.append(
                            {
                                "team1": rdteam1,
                                "score1": 0,
                                "penscore1": 0,
                                "team2": rdteam2,
                                "score2": 0,
                                "penscore2": 0,
                            }
                        )
                        drawables = [x for x in drawables if x is not rdteam2]
                        await asyncio.sleep(5)

                    async with self.config.guild(ctx.guild).cupgames() as cupgames:
                        cupgames[str(roundsize)] = fixtures

            embed = discord.Embed(
                color=0xFF0000,
                description="------------------------- Cup Draw -------------------------",
            )
            a = []
            for fixture in fixtures:
                if fixture["team2"] == "BYE":
                    a.append(f"**{fixture['team1']}** _(qualified directly)_")
                else:
                    a.append(f"{fixture['team1']} vs {fixture['team2']}")
            title = ""
            if roundsize >= 16:
                title = "Round of {}".format(roundsize)
            elif roundsize == 8:
                title = "Quarter Finals"
            elif roundsize == 4:
                title = "Semi Finals"
            else:
                title = "Final"
            embed.add_field(name=title, value="\n".join(a))
        await ctx.send(embed=embed)
        await ctx.tick()

    async def scheduleGame(self, ctx, week, homeTeam, awayTeam, time):
        query = f"sim {homeTeam} {awayTeam} --start-at {time}"
        event_name = Name()
        event_name.parsed = f"{homeTeam}_{awayTeam}_W{week}"
        scheduleCmd = self.bot.get_command("schedule")
        await ctx.invoke(scheduleCmd, event_name=event_name, schedule=Schedule(time, query))

    # @simset.command()
    # async def createscheduledfixtures(self, ctx, day: int = 0, interval: int = 1):
    #     """Create the fixtures for the current teams with scheduler."""
    #     """Day is when to start schedule in days from today. ie 0 start gameweek today, 1 start it tomorrow, etc"""
    #     """Interval is interval between two gameweeks"""
    #     # TODO: Add breaks (ie no game wednesday)
    #     gameInterval = 10
    #     today = datetime.today() + timedelta(days=day)
    #     # TODO: add starting time param 8pm will be default for every gameweek here
    #     startDate = today.replace(hour=20, minute=0, second=0, microsecond=0)

    #     teams = await self.config.guild(ctx.guild).teams()
    #     teams = list(teams.keys())
    #     if len(teams) % 2:
    #         teams.append("DAY OFF")
    #     n = len(teams)
    #     matchs = []
    #     fixtures = []
    #     return_matchs = []
    #     for fixture in range(1, n):
    #         for i in range(n // 2):
    #             matchs.append((teams[i], teams[n - 1 - i]))
    #             return_matchs.append((teams[n - 1 - i], teams[i]))
    #         teams.insert(1, teams.pop())
    #         fixtures.insert(len(fixtures) // 2, matchs)
    #         fixtures.append(return_matchs)
    #         matchs = []
    #         return_matchs = []

    #     newFixtures = []
    #     for k, fixture in enumerate(fixtures, 1):
    #         weekFixtures = []
    #         startDate = startDate + timedelta(days=(interval))
    #         for i, game in enumerate(fixture, 1):
    #             gameTime = startDate + timedelta(minutes=(i-1) * gameInterval)
    #             parsedGameDate = datetime.strftime(gameTime, '%x')
    #             parsedGameTime = datetime.strftime(gameTime, "%H:%M")
    #             """Create new tuple to add game time so we can display it in !fixtures."""
    #             newFixtureTuple = (
    #                 game[0], game[1], parsedGameDate, parsedGameTime)

    #             """Append new fixtures to current week."""
    #             weekFixtures.append(newFixtureTuple)

    #             """Running scheduler. This requires !scheduler cog"""
    #             if game[0] != "DAY OFF" and game[1] != "DAY OFF":
    #                 await self.scheduleGame(ctx, k, game[0], game[1], gameTime)

    #         newFixtures.append(weekFixtures)

    #     await self.config.guild(ctx.guild).fixtures.set(newFixtures)
    #     await ctx.tick()

    @checks.admin_or_permissions(manage_guild=True)
    @simset.group()
    async def clear(self, ctx):
        """SimLeague Clear Settings"""

    @clear.command(name="all")
    async def clear_all(self, ctx):
        """Clear all teams, stats etc."""
        await self.config.guild(ctx.guild).clear()
        await self.config.guild(ctx.guild).standings.set({})
        await self.config.guild(ctx.guild).stats.set({})
        await self.config.guild(ctx.guild).transfers.set({})
        await self.config.guild(ctx.guild).transferred.set([])
        await self.config.guild(ctx.guild).tots.set({"players": {}, "kit": None, "logo": None})
        await ctx.tick()

    @clear.command(name="stats")
    async def clear_stats(self, ctx):
        """Clear standings and player stats."""
        await self.config.guild(ctx.guild).standings.set({})
        teams = await self.config.guild(ctx.guild).teams()
        async with self.config.guild(ctx.guild).standings() as standings:
            for team in teams:
                standings[team] = {
                    "played": 0,
                    "wins": 0,
                    "losses": 0,
                    "points": 0,
                    "gd": 0,
                    "gf": 0,
                    "ga": 0,
                    "draws": 0,
                    "reds": 0,
                    "yellows": 0,
                    "fouls": 0,
                    "chances": 0,
                }
        await self.config.guild(ctx.guild).stats.set({})
        await ctx.tick()

    @clear.command(name="notes")
    async def clear_notes(self, ctx):
        """Clear player notes."""
        await self.config.guild(ctx.guild).notes.set({})
        await ctx.tick()

    @clear.command(name="cupstats")
    async def clear_cupstats(self, ctx):
        """Clear cup stats."""
        await self.config.guild(ctx.guild).cupstandings.set({})
        teams = await self.config.guild(ctx.guild).teams()
        async with self.config.guild(ctx.guild).cupstandings() as cupstandings:
            for team in teams:
                cupstandings[team] = {
                    "played": 0,
                    "wins": 0,
                    "losses": 0,
                    "points": 0,
                    "gd": 0,
                    "gf": 0,
                    "ga": 0,
                    "draws": 0,
                    "reds": 0,
                    "yellows": 0,
                    "fouls": 0,
                    "chances": 0,
                }
        await self.config.guild(ctx.guild).cupstats.set({})
        await ctx.tick()

    @clear.command(name="transfers")
    async def clear_transfers(self, ctx):
        await self.config.guild(ctx.guild).transferred.set([])
        await ctx.tick()

    @clear.command(name="lock")
    async def clear_lock(self, ctx, team=None):
        teams = await self.config.guild(ctx.guild).teams()
        if team is not None and team not in teams:
            return await ctx.send("This team does not exist.")
        async with self.config.guild(ctx.guild).transfers() as transfers:
            if team is not None:
                transfers[team]["locked"] = None
            else:
                for t in transfers:
                    transfers[t]["locked"] = None
        await ctx.tick()

    @clear.command(name="cup")
    async def clear_cup(self, ctx):
        await self.config.guild(ctx.guild).cupgames.set({})
        await self.config.guild(ctx.guild).cupstats.set({})
        await ctx.tick()

    @clear.command(name="palmares")
    async def clear_palmares(self, ctx):
        await self.config.guild(ctx.guild).palmares.set({})
        await ctx.tick()

    @clear.command(name="tots")
    async def clear_tots(self, ctx):
        await self.config.guild(ctx.guild).tots.set({"players": {}, "kit": None, "logo": None})
        await ctx.tick()
