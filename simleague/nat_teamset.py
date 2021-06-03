import discord
import validators
from redbot.core import checks, commands

from .abc import MixinMeta


class NationalTeamsetMixin(MixinMeta):
    """National Teamset Settings"""

    @checks.admin_or_permissions(manage_guild=True)
    @commands.group(autohelp=True)
    async def nat_teamset(self, ctx):
        """Team Settings."""

    # ! Probably not needed
    @nat_teamset.command()
    async def nat_role(self, ctx, team: str, *, role: discord.Role):
        """Set a national team's role."""
        async with self.config.guild(ctx.guild).nteams() as nteams:
            if team not in nteams:
                return await ctx.send("Not a valid team.")
            nteams[team]["role"] = role.id
        await ctx.tick()

    @nat_teamset.command(name="stadium")
    async def nat_stadium(self, ctx, team: str, *, stadium: str):
        """Set a national team's stadium."""
        async with self.config.guild(ctx.guild).nteams() as nteams:
            if team not in nteams:
                return await ctx.send("Not a valid team.")
            nteams[team]["stadium"] = stadium
        await ctx.tick()

    @nat_teamset.command(name="logo")
    async def nat_logo(self, ctx, team: str, *, logo: str):
        """Set a national team's logo."""
        if not validators.url(logo):
            await ctx.send("This doesn't seem to be a valid URL.")
        if not logo.endswith(".png"):
            await ctx.send("URL must be a png.")
        async with self.config.guild(ctx.guild).nteams() as nteams:
            if team not in nteams:
                return await ctx.send("Not a valid team.")
            nteams[team]["logo"] = logo
        await ctx.tick()

    @nat_teamset.command(usage="<current name> <new name>", name="name")
    async def nat_name(self, ctx, team: str, newname: str):
        """Set a national team's name. Try to keep names to one word if possible."""
        async with self.config.guild(ctx.guild).nteams() as nteams:
            if team in nteams:
                nteams[newname] = nteams[team]
                if nteams[team]["role"] is not None:
                    role = ctx.guild.get_role(nteams[team]["role"])
                    if role:
                        await role.edit(name=newname)
                del nteams[team]
        async with self.config.guild(ctx.guild).nstandings() as nstandings:
            if team in nstandings:
                nstandings[newname] = nstandings[team]
                del nstandings[team]
        async with self.config.guild(ctx.guild).nstats() as nstats:
            if team in nstats["cleansheets"]:
                nstats["cleansheets"][newname] = nstats["cleansheets"][team]
                del nstats["cleansheets"][team]
        async with self.config.guild(ctx.guild).ngames() as ngames:
            if len(ngames):
                for rd in ngames:
                    fixtures = ngames[rd]
                    for fixture in fixtures:
                        if fixture["team1"] == team:
                            fixture["team1"] = newname
                        if fixture["team2"] == team:
                            fixture["team2"] = newname
        await ctx.tick()

    @nat_teamset.command(name="fullname")
    async def nat_fullname(self, ctx, team: str, *, fullname: str):
        """Set a national team's full name."""
        async with self.config.guild(ctx.guild).nteams() as nteams:
            if team not in nteams:
                return await ctx.send("Not a valid team.")
            nteams[team]["fullname"] = fullname
        await ctx.tick()

    @nat_teamset.command(name="captain")
    async def nat_captain(self, ctx, team: str, captain: discord.Member):
        """Set a team's captain."""
        async with self.config.guild(ctx.guild).nteams() as nteams:
            if team not in nteams:
                return await ctx.send("Not a valid team.")
            if str(captain.id) not in nteams[team]["members"]:
                return await ctx.send("{} is not a member of {}.".format(captain.name, team))
            nteams[team]["captain"] = {}
            nteams[team]["captain"] = {str(captain.id): captain.name}

        await ctx.tick()

    @nat_teamset.group(autohelp=True, name="kits")
    async def nat_kits(self, ctx):
        """Kit Settings."""

    @nat_kits.command(name="home")
    async def nat_home(self, ctx, team: str, *, kiturl: str):
        """Set a team's home kit."""
        if not validators.url(kiturl):
            await ctx.send("This doesn't seem to be a valid URL.")
        if not kiturl.endswith(".png"):
            await ctx.send("URL must be a png.")
        async with self.config.guild(ctx.guild).nteams() as nteams:
            if team not in nteams:
                return await ctx.send("Not a valid team.")
            nteams[team]["kits"]["home"] = kiturl
        await ctx.tick()

    @nat_kits.command(name="away")
    async def nat_away(self, ctx, team: str, *, kiturl: str):
        """Set a team's away kit."""
        if not validators.url(kiturl):
            await ctx.send("This doesn't seem to be a valid URL.")
            return
        if not kiturl.endswith(".png"):
            await ctx.send("URL must be a png.")
        async with self.config.guild(ctx.guild).nteams() as nteams:
            if team not in nteams:
                return await ctx.send("Not a valid team.")
            nteams[team]["kits"]["away"] = kiturl
        await ctx.tick()

    @nat_teamset.command(name="delete")
    async def nat__delete(self, ctx, *, team):
        """Delete a national team."""
        await self.nat_team_delete(ctx, team)
