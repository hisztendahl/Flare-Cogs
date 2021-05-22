import discord
from redbot.core import commands
from .abc import MixinMeta
from redbot.core.utils.chat_formatting import box
from tabulate import tabulate

class StandingsMixin(MixinMeta):
    """Standings Settings"""

    @commands.group(invoke_without_command=True)
    async def standings(self, ctx, verbose: bool = False):
        """Current sim standings."""
        standings = await self.config.guild(ctx.guild).standings()
        if standings is None:
            return await ctx.send("The table is empty.")
        if not verbose:
            t = []  # PrettyTable(["Team", "Pl", "W", "D", "L", "Pts"])
            for x in sorted(
                standings,
                key=lambda x: (standings[x]["points"], standings[x]["gd"], standings[x]["gf"]),
                reverse=True,
            ):
                gd = standings[x]["gd"]
                gd = f"+{gd}" if gd > 0 else gd
                t.append(
                    [
                        x,
                        standings[x]["played"],
                        standings[x]["wins"],
                        standings[x]["draws"],
                        standings[x]["losses"],
                        standings[x]["points"],
                        gd,
                    ]
                )
            tab = tabulate(t, headers=["Team", "Pl.", "W", "D", "L", "Pts", "Diff"])
            await ctx.send(box(tab))
        else:
            t = []
            for x in sorted(
                standings,
                key=lambda x: (standings[x]["points"], standings[x]["gd"], standings[x]["gf"]),
                reverse=True,
            ):
                gd = standings[x]["gd"]
                gd = f"+{gd}" if gd > 0 else gd
                t.append(
                    [
                        x,
                        standings[x]["played"],
                        standings[x]["wins"],
                        standings[x]["draws"],
                        standings[x]["losses"],
                        standings[x]["gf"],
                        standings[x]["ga"],
                        standings[x]["points"],
                        gd,
                    ]
                )
            tab = tabulate(
                t,
                headers=["Team", "Pl.", "W", "D", "L", "GF", "GA", "Pts", "Diff"],
            )
            await ctx.send(box(tab))

    async def _stat_standings(self, ctx, stat: str, title: str, reverse: bool = True):
        standings = await self.config.guild(ctx.guild).standings()
        if standings is None:
            return await ctx.send("No stat available.")
        t = []
        for x in sorted(
            standings,
            key=lambda x: (standings[x][stat]),
            reverse=reverse,
        ):
            t.append(f"{x} - {standings[x][stat]}")
        embed = discord.Embed(title=title, description="\n".join(t), colour=0xFF0000)
        await ctx.send(embed=embed)

    @standings.command(name="goals")
    async def standings_goals(self, ctx):
        """Teams with the most goals."""
        return await self._stat_standings(ctx, "gf", "Goals")

    @standings.command(name="shots")
    async def _shots(self, ctx):
        """Teams with the most shots."""
        return await  self._stat_standings(ctx, "chances", "Shots")

    @standings.command(name="fouls")
    async def _fouls(self, ctx):
        """Teams with the most fouls."""
        return await  self._stat_standings(ctx, "fouls", "Fouls")

    @standings.command(name="yellows")
    async def _yellows(self, ctx):
        """Teams with the most yellows."""
        return await  self._stat_standings(ctx, "yellows", "Yellow Cards")

    @standings.command(name="reds")
    async def _reds(self, ctx):
        """Teams with the most reds."""
        return await  self._stat_standings(ctx, "reds", "Red Cards")

    @standings.command(name="defence")
    async def _defence(self, ctx):
        """Teams with the least goals conceded."""
        return await  self._stat_standings(ctx, "ga", "Goals Conceded", False)

    @standings.command(name="conversion")
    async def _conversion(self, ctx):
        """Teams with the best conversion rate."""
        standings = await self.config.guild(ctx.guild).standings()
        if standings is None:
            return await ctx.send("No stat available.")
        t = []
        for x in sorted(
            standings,
            key=lambda x: (
                int(standings[x]["gf"]) / int(standings[x]["chances"])
                if int(standings[x]["chances"]) > 0
                else 0
            ),
            reverse=True,
        ):
            if int(standings[x]["chances"]) > 0:
                goal_conversion = int(standings[x]["gf"]) / int(standings[x]["chances"])
                goal_conversion = round(goal_conversion * 100, 2)
            else:
                goal_conversion = 0
            t.append(f"{x} - {goal_conversion}%")
        embed = discord.Embed(
            title="Goal Conversion Rate", description="\n".join(t), colour=0xFF0000
        )
        await ctx.send(embed=embed)
