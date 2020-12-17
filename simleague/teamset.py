import discord
import validators
from redbot.core import checks, commands

from .abc import MixinMeta


class TeamsetMixin(MixinMeta):
    """Teamset Settings"""

    @commands.group(autohelp=True)
    async def transfer(self, ctx):
        """Transfer Commands."""

    @commands.has_role("Sim Captain")
    @transfer.command(name="swap")
    async def _swap(self, ctx, team1, player1: discord.Member, team2, player2: discord.Member):
        """Swap a player from your team with a player from another team."""
        teams = await self.config.guild(ctx.guild).teams()
        cpt1id = list(teams[team1]["captain"].keys())[0]
        cpt2id = list(teams[team2]["captain"].keys())[0]
        if not await self.config.guild(ctx.guild).transferwindow():
            return await ctx.send("The transfer window is currently closed.")
        if ctx.author.id != int(cpt1id):
            return await ctx.send("You need to pick players from your team")
        transfers = await self.config.guild(ctx.guild).transfers()
        if not transfers[team1]["ready"]:
            return await ctx.send("Your team is not eligible for transfers yet.")
        transferred = await self.config.guild(ctx.guild).transferred()
        if int(cpt1id) == player1.id or int(cpt2id) == player2.id:
            return await ctx.send("You cannot transfer team captains.")
        if player1.id in transferred:
            return await ctx.send(
                "You cannot pick this player as he has already been transferred during this window: {}.".format(
                    player1.name
                )
            )
        if player2.id in transferred:
            return await ctx.send(
                "You cannot pick this player as he has already been transferred during this window: {}.".format(
                    player2.name
                )
            )

        await self.swap(ctx, ctx.guild, team1, player1, team2, player2)
        await ctx.tick()

    @commands.has_role("Sim Captain")
    @transfer.command(name="sign")
    async def _sign(self, ctx, team1, player1: discord.Member, player2: discord.Member):
        """Release a player and sign a free agent."""
        teams = await self.config.guild(ctx.guild).teams()
        cptid = list(teams[team1]["captain"].keys())[0]
        if not await self.config.guild(ctx.guild).transferwindow():
            return await ctx.send("The transfer window is currently closed.")
        if ctx.author.id != int(cptid):
            return await ctx.send("You need to pick players from your team")
        transfers = await self.config.guild(ctx.guild).transfers()
        if not transfers[team1]["ready"]:
            return await ctx.send("Your team is not eligible for transfers yet.")
        if int(cptid) == player1.id:
            return await ctx.send("You cannot release team captains.")
        await self.sign(ctx, ctx.guild, team1, player1, player2)
        await ctx.tick()

    @commands.has_role("Sim Captain")
    @transfer.command(name="pass")
    async def _pass(self, ctx):
        """End your transfer window."""
        if not await self.config.guild(ctx.guild).transferwindow():
            return await ctx.send("The transfer window is currently closed.")

        teams = await self.config.guild(ctx.guild).teams()
        team = None
        for t in teams:
            if int(list(teams[t]["captain"])[0]) == ctx.author.id:
                team = t

        if team is not None:
            await self.skipcurrentteam(ctx, teams, team)

    async def skipcurrentteam(self, ctx, teams, team):
        standings = await self.config.guild(ctx.guild).standings()
        async with self.config.guild(ctx.guild).transfers() as transfers:
            if not transfers[team]["ready"]:
                return await ctx.send("Transfers are not available for {} yet.".format(team))
            sortedstandings = sorted(
                standings,
                key=lambda team: (
                    standings[team]["points"],
                    standings[team]["gd"],
                    standings[team]["gf"],
                ),
                reverse=False,
            )
            currentteamindex = sortedstandings.index(team)
            transfers[sortedstandings[currentteamindex]]["ready"] = False
            if currentteamindex < len(sortedstandings):
                transfers[sortedstandings[currentteamindex + 1]]["ready"] = True
                currentteam = ctx.guild.get_role(
                    teams[sortedstandings[currentteamindex]]["role"]
                ).mention
                nextteam = ctx.guild.get_role(
                    teams[sortedstandings[currentteamindex + 1]]["role"]
                ).mention
                await ctx.send(
                    "Transfers done for {}, now turn for: {}".format(currentteam, nextteam)
                )
                await ctx.tick()

    @checks.admin_or_permissions(manage_guild=True)
    @transfer.command(name="skip")
    async def _skip(self, ctx, team):
        """End transfer window for a given team."""
        if not await self.config.guild(ctx.guild).transferwindow():
            return await ctx.send("The transfer window is currently closed.")

        teams = await self.config.guild(ctx.guild).teams()
        await self.skipcurrentteam(ctx, teams, team)

    @commands.has_role("Sim Captain")
    @transfer.command(name="turn")
    async def turn(self, ctx):
        """Shows the team currently eligible to make transfers."""
        if not await self.config.guild(ctx.guild).transferwindow():
            return await ctx.send("The transfer window is currently closed.")

        transfers = await self.config.guild(ctx.guild).transfers()
        eligibleteam = [team for team in transfers if transfers[team]["ready"] == True]
        await ctx.send(f"Current transferring team: {eligibleteam[0]}")

    @commands.has_role("Sim Captain")
    @transfer.command(name="lock")
    async def _lock(self, ctx, team1, player1: discord.Member):
        """Lock a player to make him intransferable."""
        teams = await self.config.guild(ctx.guild).teams()
        cptid = list(teams[team1]["captain"].keys())[0]
        transfers = await self.config.guild(ctx.guild).transfers()
        if not await self.config.guild(ctx.guild).extensionwindow():
            return await ctx.send("The contract extension window is currently closed.")
        if ctx.author.id != int(cptid):
            return await ctx.send("You need to pick players from your team")
        transfers = await self.config.guild(ctx.guild).transfers()
        if transfers[team1]["locked"] is not None:
            return await ctx.send("You have already locked a player.")
        if int(cptid) == player1.id:
            return await ctx.send("Team captains are already locked.")
        await self.lock(ctx, ctx.guild, team1, player1)

    @transfer.command(name="list")
    async def _tlist(self, ctx, team1=None):
        """Shows players already transferred during this window."""
        transferred = await self.config.guild(ctx.guild).transferred()
        transfers = await self.config.guild(ctx.guild).transfers()
        teams = await self.config.guild(ctx.guild).teams()
        async with ctx.typing():
            if team1 is not None:
                if team1 not in teams:
                    return await ctx.send(f"{team1} is not a valid team.")
                embed = discord.Embed(
                    color=0x800080, description="--------------- Transfer List ---------------"
                )
                av = []
                unav = []
                members = {
                    k: v
                    for (k, v) in teams[team1]["members"].items()
                    if k not in teams[team1]["captain"]
                }
                for m in members:
                    if int(m) in transferred or transfers[team1]["locked"] == int(m):
                        unav.append(m)
                    else:
                        av.append(m)

                avmems = [members[x] if x != "" else "" for x in av]
                unavmems = [members[x] if x != "" else "" for x in unav]

                embed.add_field(
                    name="Team {}".format(team1),
                    value="\n_Available_:\n{}\n\n_Unavailable_:\n{}".format(
                        "\n".join(avmems),
                        "\n".join(unavmems),
                    ),
                    inline=True,
                )
            else:
                embed = discord.Embed(
                    color=0x800080,
                    description="------------------------- Transfer List -------------------------",
                )
                for team in teams:
                    av = []
                    unav = []
                    members = {
                        k: v
                        for (k, v) in teams[team]["members"].items()
                        if k not in teams[team]["captain"]
                    }
                    for m in members:
                        if int(m) in transferred or transfers[team]["locked"] == int(m):
                            unav.append(m)
                        else:
                            av.append(m)

                    avmems = [members[x] if x != "" else "" for x in av]
                    unavmems = [members[x] if x != "" else "" for x in unav]

                    embed.add_field(
                        name="Team {}".format(team),
                        value="\n_Available_:\n{}\n\n_Unavailable_:\n{}".format(
                            "\n".join(avmems),
                            "\n".join(unavmems),
                        ),
                        inline=True,
                    )
        await ctx.send(embed=embed)

    @checks.admin_or_permissions(manage_guild=True)
    @commands.group(autohelp=True)
    async def admintransfer(self, ctx):
        """Admin Transfers."""

    @admintransfer.command(name="lock")
    async def _adminlock(self, ctx, team):
        """Lock players from a team."""
        teams = await self.config.guild(ctx.guild).teams()
        if team not in teams:
            return await ctx.send("Not a valid team.")
        async with self.config.guild(ctx.guild).transferred() as transferred:
            await ctx.send(f"transferred: {transferred}")
            for player in teams[team]["members"]:
                player = str(player)
                if player != teams[team]["captain"]:
                    transferred.append(int(player))
        await ctx.tick()
        
    @admintransfer.command(name="swap")
    async def _adminswap(
        self, ctx, team1, player1: discord.Member, team2, player2: discord.Member
    ):
        """Swap a player from your team with a player from another team."""
        if not await self.config.guild(ctx.guild).transferwindow():
            return await ctx.send("The transfer window is currently closed.")
        teams = await self.config.guild(ctx.guild).teams()
        cpt1id = list(teams[team1]["captain"].keys())[0]
        cpt2id = list(teams[team2]["captain"].keys())[0]
        if int(cpt1id) == player1.id or int(cpt2id) == player2.id:
            return await ctx.send("You cannot transfer team captains.")
        await self.swap(ctx, ctx.guild, team1, player1, team2, player2)
        await ctx.tick()

    @admintransfer.command(name="swapid")
    async def _adminswapid(self, ctx, team1, player1id, team2, player2id):
        """Swap a player from your team with a player from another team."""
        if not await self.config.guild(ctx.guild).transferwindow():
            return await ctx.send("The transfer window is currently closed.")
        teams = await self.config.guild(ctx.guild).teams()
        cpt1id = list(teams[team1]["captain"].keys())[0]
        cpt2id = list(teams[team2]["captain"].keys())[0]
        player1 = await self.bot.fetch_user(player1id)
        if player1 is None:
            player1 = await self.bot.fetch_user(player1id)
        player2 = await self.bot.fetch_user(player2id)
        if player2 is None:
            player2 = await self.bot.fetch_user(player2id)
        if int(cpt1id) == player1.id or int(cpt2id) == player2.id:
            return await ctx.send("You cannot transfer team captains.")
        await self.swap(ctx, ctx.guild, team1, player1, team2, player2)
        await ctx.tick()

    @admintransfer.command(name="sign")
    async def _adminsign(self, ctx, team1, player1: discord.Member, player2: discord.Member):
        """Release a player and sign a free agent."""
        if not await self.config.guild(ctx.guild).transferwindow():
            return await ctx.send("The transfer window is currently closed.")
        teams = await self.config.guild(ctx.guild).teams()
        cptid = list(teams[team1]["captain"].keys())[0]
        if int(cptid) == player1.id:
            return await ctx.send("You cannot release team captains.")
        await self.sign(ctx, ctx.guild, team1, player1, player2)
        await ctx.tick()

    @admintransfer.command(name="signid")
    async def _adminsignid(self, ctx, team1, player1id, player2id):
        """Release a player and sign a free agent."""
        if not await self.config.guild(ctx.guild).transferwindow():
            return await ctx.send("The transfer window is currently closed.")
        teams = await self.config.guild(ctx.guild).teams()
        cptid = list(teams[team1]["captain"].keys())[0]
        player1 = await self.bot.fetch_user(player1id)
        if player1 is None:
            player1 = await self.bot.fetch_user(player1id)
        player2 = await self.bot.fetch_user(player2id)
        if player2 is None:
            player2 = await self.bot.fetch_user(player2id)
        if int(cptid) == player1.id:
            return await ctx.send("You cannot release team captains.")
        await self.sign(ctx, ctx.guild, team1, player1, player2)
        await ctx.tick()

    @checks.admin_or_permissions(manage_guild=True)
    @commands.group(autohelp=True)
    async def teamset(self, ctx):
        """Team Settings."""

    @teamset.command()
    async def role(self, ctx, team: str, *, role: discord.Role):
        """Set a team's role."""
        async with self.config.guild(ctx.guild).teams() as teams:
            if team not in teams:
                return await ctx.send("Not a valid team.")
            teams[team]["role"] = role.id
        await ctx.tick()

    @teamset.command()
    async def stadium(self, ctx, team: str, *, stadium: str):
        """Set a team's stadium."""
        async with self.config.guild(ctx.guild).teams() as teams:
            if team not in teams:
                return await ctx.send("Not a valid team.")
            teams[team]["stadium"] = stadium
        await ctx.tick()

    @teamset.command()
    async def logo(self, ctx, team: str, *, logo: str):
        """Set a team's logo."""
        if not validators.url(logo):
            await ctx.send("This doesn't seem to be a valid URL.")
        if not logo.endswith(".png"):
            await ctx.send("URL must be a png.")
        async with self.config.guild(ctx.guild).teams() as teams:
            if team not in teams:
                return await ctx.send("Not a valid team.")
            teams[team]["logo"] = logo
        await ctx.tick()

    @teamset.command(hidden=True)
    async def bonus(self, ctx, team: str, *, amount: int):
        """Set a team's bonus multiplier."""
        async with self.config.guild(ctx.guild).teams() as teams:
            if team not in teams:
                return await ctx.send("Not a valid team.")
            teams[team]["bonus"] = amount
        await ctx.tick()

    @teamset.command(usage="<current name> <new name>")
    async def name(self, ctx, team: str, *, newname: str):
        """Set a team's name. Try keep names to one word if possible."""
        async with self.config.guild(ctx.guild).teams() as teams:
            if team not in teams:
                return await ctx.send("Not a valid team.")
            teams[newname] = teams[team]
            if teams[team]["role"] is not None:
                role = ctx.guild.get_role(teams[team]["role"])
                await role.edit(name=newname)
            del teams[team]
        async with self.config.guild(ctx.guild).standings() as teams:
            teams[newname] = teams[team]
            del teams[team]
        async with self.config.guild(ctx.guild).cupstandings() as cupteams:
            if len(dict.keys(cupteams)):
                cupteams[newname] = cupteams[team]
                del cupteams[team]
        async with self.config.guild(ctx.guild).transfers() as transfers:
            if team in transfers:
                transfers[newname] = transfers[team]
            del transfers[team]
        async with self.config.guild(ctx.guild).fixtures() as fixtures:
            if len(fixtures):
                for weekday in fixtures:
                    for fixture in weekday:
                        for i in range(len(fixture)):
                            if fixture[i] == team:
                                fixture[i] = newname
        await ctx.tick()

    @teamset.command()
    async def fullname(self, ctx, team: str, *, fullname: str):
        """Set a team's full name."""
        async with self.config.guild(ctx.guild).teams() as teams:
            if team not in teams:
                return await ctx.send("Not a valid team.")
            teams[team]["fullname"] = fullname
        await ctx.tick()

    @teamset.command()
    async def captain(self, ctx, team: str, captain: discord.Member):
        """Set a team's captain."""
        async with self.config.guild(ctx.guild).teams() as teams:
            if team not in teams:
                return await ctx.send("Not a valid team.")
            if str(captain.id) not in teams[team]["members"]:
                return await ctx.send("{} is not a member of {}.".format(captain.name, team))
            teams[team]["captain"] = {}
            teams[team]["captain"] = {str(captain.id): captain.name}

        await ctx.tick()

    @teamset.group(autohelp=True)
    async def kits(self, ctx):
        """Kit Settings."""

    @kits.command()
    async def home(self, ctx, team: str, *, kiturl: str):
        """Set a team's home kit."""
        if not validators.url(kiturl):
            await ctx.send("This doesn't seem to be a valid URL.")
        if not kiturl.endswith(".png"):
            await ctx.send("URL must be a png.")
        async with self.config.guild(ctx.guild).teams() as teams:
            if team not in teams:
                return await ctx.send("Not a valid team.")
            teams[team]["kits"]["home"] = kiturl
        await ctx.tick()

    @kits.command()
    async def away(self, ctx, team: str, *, kiturl: str):
        """Set a team's away kit."""
        if not validators.url(kiturl):
            await ctx.send("This doesn't seem to be a valid URL.")
            return
        if not kiturl.endswith(".png"):
            await ctx.send("URL must be a png.")
        async with self.config.guild(ctx.guild).teams() as teams:
            if team not in teams:
                return await ctx.send("Not a valid team.")
            teams[team]["kits"]["away"] = kiturl
        await ctx.tick()

    @kits.command()
    async def third(self, ctx, team: str, *, kiturl: str):
        """Set a team's third kit."""
        if not validators.url(kiturl):
            await ctx.send("This doesn't seem to be a valid URL.")
        if not kiturl.endswith(".png"):
            await ctx.send("URL must be a png.")
        async with self.config.guild(ctx.guild).teams() as teams:
            if team not in teams:
                return await ctx.send("Not a valid team.")
            teams[team]["kits"]["third"] = kiturl
        await ctx.tick()

    @teamset.command(name="delete")
    async def _delete(self, ctx, *, team):
        """Delete a team."""
        await self.team_delete(ctx, team)
