import discord
import re
import logging
import discord
import aiohttp
from typing import Literal, Optional

from .default_players import default_players
from .hungergames import HungerGames
from .enums import ErrorCode
from .utils import sanitize_here_everyone, sanitize_special_chars, strip_mentions
from redbot.core.bot import Red
from redbot.core import Config, bank, checks, commands

prefix = '''!hg '''
hg = HungerGames()

class HungryBot(commands.Cog):
    """Hunger Games."""
    __version__ = "1.0.0"

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=4268355870)
        self.logger = logging.getLogger('red.hisztendahl.HungryBot')
        self.session = aiohttp.ClientSession()

    async def red_delete_data_for_user(
        self,
        *,
        requester: Literal["discord_deleted_user", "owner", "user", "user_strict"],
        user_id: int,
    ):
        await self.config.user_from_id(user_id).clear()

    def cog_unload(self):
        self.bot.loop.create_task(self.session.close())

    @commands.group(autohelp=True)
    async def hg(self, ctx):
        """Hunger Games Commands."""
    
    @hg.command()
    @commands.guild_only()
    async def new(self, ctx, *, title: str = None):
        """
        Start a new Hunger Games simulation in the current channel.
        Each channel can only have one simulation running at a time.

        title - (Optional) The title of the simulation. Defaults to 'The Hunger Games'
        """
        if title is None or title == "":
            title = "The Hunger Games"
        else:
            title = strip_mentions(ctx.message, title)
            title = sanitize_here_everyone(title)
            title = sanitize_special_chars(title)
        owner = ctx.author
        ret = hg.new_game(ctx.channel.id, owner.id, owner.name, title)
        if not await self.__check_errors(ctx, ret):
            return
        await ctx.send("{0} has started {1}! Use `{2}add [-m|-f] <name>` to add a player or `{2}join [-m|-f]` to enter the "
                    "game yourself!".format(owner.mention, title, prefix))


    @hg.command()
    @commands.guild_only()
    async def join(self, ctx, gender=None):
        """
        Adds a tribute with your name to a new simulation.

        gender (Optional) - Use `-m` or `-f` to set male or female gender. Defaults to a random gender.
        """
        name = ctx.author.nick if ctx.author.nick is not None else ctx.author.name
        name = f"**{name}**"
        ret = hg.add_player(ctx.channel.id, name, gender=gender, volunteer=True)
        if not await self.__check_errors(ctx, ret):
            return
        await ctx.send(ret)

    @hg.command()
    @checks.admin_or_permissions(manage_guild=True)
    @commands.guild_only()
    async def change_owner(self, ctx):
        """Change owner of the current active game."""
        name = ctx.author.nick if ctx.author.nick is not None else ctx.author.name
        ret = hg.take_ownership(ctx.channel.id, ctx.author.id, name)
        if not await self.__check_errors(ctx, ret):
            return
        await ctx.send(ret)

    @hg.command(rest_is_raw=True)
    @commands.guild_only()
    async def add(self, ctx, *, name: str):
        """
        Add a user to a new game.

        name - The name of the tribute to add. Limit 32 chars. Leading and trailing whitespace will be trimmed.
        Special chars @*_`~ count for two characters each.
        \tPrepend the name with a `-m ` or `-f ` flag to set male or female gender. Defaults to a random gender.
        """
        name = strip_mentions(ctx.message, name)
        name = sanitize_here_everyone(name)
        name = sanitize_special_chars(name)

        ret = hg.add_player(ctx.channel.id, name)
        if not await self.__check_errors(ctx, ret):
            return
        await ctx.send(ret)


    @hg.command(rest_is_raw=True)
    @commands.guild_only()
    async def remove(self, ctx, *, name: str):
        """
        Remove a user from a new game.
        Only the game's host may use this command.

        name - The name of the tribute to remove.
        """
        name = strip_mentions(ctx.message, name)
        name = sanitize_here_everyone(name)
        name = sanitize_special_chars(name)

        ret = hg.remove_player(ctx.channel.id, name)
        if not await self.__check_errors(ctx, ret):
            return
        await ctx.send(ret)


    @hg.command()
    @commands.guild_only()
    async def fill(self, ctx, group_name=None):
        """
        Pad out empty slots in a new game with default characters.

        group_name (Optional) - The builtin group to draw tributes from. Defaults to members in this guild.
        """
        if group_name is None:
            group = []
            for m in list(ctx.message.guild.members):
                if m.nick is not None:
                    group.append(f"**{m.nick}**")
                else:
                    group.append(f"**{m.name}**")
        else:
            group = default_players.get(group_name)

        ret = hg.pad_players(ctx.channel.id, group)
        if not await self.__check_errors(ctx, ret):
            return
        await ctx.send(ret)


    @hg.command()
    @commands.guild_only()
    async def status(self, ctx):
        """
        Gets the status for the game in the channel.
        """
        ret = hg.status(ctx.channel.id)
        if not await self.__check_errors(ctx, ret):
            return
        embed = discord.Embed(title=ret['title'], description=ret['description'])
        embed.set_footer(text=ret['footer'])
        await ctx.send(embed=embed)


    @hg.command()
    @commands.guild_only()
    async def start(self, ctx):
        """
        Starts the pending game in the channel.
        """
        ret = hg.start_game(ctx.channel.id, ctx.author.id, prefix)
        if not await self.__check_errors(ctx, ret):
            return
        embed = discord.Embed(title=ret['title'], description=ret['description'])
        embed.set_footer(text=ret['footer'])
        await ctx.send(embed=embed)


    @hg.command()
    @commands.guild_only()
    async def end(self, ctx):
        """
        Cancels the current game in the channel.
        """
        ret = hg.end_game(ctx.channel.id, ctx.author.id)
        if not await self.__check_errors(ctx, ret):
            return
        await ctx.send("{0} has been cancelled. Anyone may now start a new game with `{1}new`.".format(ret.title, prefix))


    @hg.command()
    @commands.guild_only()
    async def step(self, ctx):
        """
        Steps forward the current game in the channel by one round.
        """
        ret = hg.step(ctx.channel.id, ctx.author.id)
        if not await self.__check_errors(ctx, ret):
            return
        embed = discord.Embed(title=ret['title'], color=ret['color'], description=ret['description'])
        if ret['footer'] is not None:
            embed.set_footer(text=ret['footer'])
        await ctx.send(embed=embed)


    async def __check_errors(self, ctx, error_code):
        if type(error_code) is not ErrorCode:
            return True
        if error_code is ErrorCode.NO_GAME:
            await ctx.send("There is no game currently running in this channel.")
            return False
        if error_code is ErrorCode.GAME_EXISTS:
            await ctx.send("A game has already been started in this channel.")
            return False
        if error_code is ErrorCode.GAME_STARTED:
            await ctx.send("This game is already running.")
            return False
        if error_code is ErrorCode.GAME_FULL:
            await ctx.send("This game is already at maximum capacity.")
            return False
        if error_code is ErrorCode.PLAYER_EXISTS:
            await ctx.send("That person is already in this game.")
            return False
        if error_code is ErrorCode.CHAR_LIMIT:
            await ctx.send("That name is too long (max 32 chars).")
            return False
        if error_code is ErrorCode.NOT_OWNER:
            await ctx.send("You are not the owner of this game.")
            return False
        if error_code is ErrorCode.INVALID_GROUP:
            await ctx.send("That is not a valid group. Valid groups are:\n```\n{0}\n```"
                            .format("\n".join(list(default_players.keys()))))
            return False
        if error_code is ErrorCode.NOT_ENOUGH_PLAYERS:
            await ctx.send("There are not enough players to start a game. There must be at least 2.")
            return False
        if error_code is ErrorCode.GAME_NOT_STARTED:
            await ctx.send("This game hasn't been started yet.")
            return False
        if error_code is ErrorCode.PLAYER_DOES_NOT_EXIST:
            await ctx.send("There is no player with that name in this game.")
            return False


