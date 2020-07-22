import discord
from redbot.cogs.mod import Mod as ModClass
from redbot.core import bank, commands
from redbot.core.utils import AsyncIter
from redbot.core.utils.chat_formatting import humanize_number
from redbot.core.utils.common_filters import filter_invites

EMOJIS = {
    "staff": 706198524156706917,
    "early_supporter": 706198530837970998,
    "hypesquad_balance": 706198531538550886,
    "hypesquad_bravery": 706198532998299779,
    "hypesquad_brilliance": 706198535846101092,
    "hypesquad": 706198537049866261,
    "verified_bot_developer": 706198727953612901,
    "bug_hunter": 706199712402898985,
    "bug_hunter_level_2": 706199774616879125,
    "partner": 706206032216457258,
    "verified_bot": 706196603748483174,
    "verified_bot2": 706196604197273640,
}


class Mod(ModClass):
    """Mod with userinfo ehhancements."""

    __version__ = "1.0.0"

    def format_help_for_context(self, ctx):
        """Thanks Sinbad."""
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\nCog Version: {self.__version__}"

    def __init__(self, bot):
        super().__init__(bot)
        self.bot = bot
        self.status_emojis = {
            "mobile": discord.utils.get(self.bot.emojis, id=725387684113023057),
            "online": discord.utils.get(self.bot.emojis, id=724950463417548890),
            "away": discord.utils.get(self.bot.emojis, id=724950462729551883),
            "dnd": discord.utils.get(self.bot.emojis, id=724950462499127338),
            "offline": discord.utils.get(self.bot.emojis, id=724950462746460271),
            "streaming": discord.utils.get(self.bot.emojis, id=724950551900717066),
        }

    # Removes main userinfo command.
    userinfo = None

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(embed_links=True)
    async def userinfo(self, ctx, *, user: discord.Member = None):
        """Show userinfo with some more detail."""
        author = ctx.author
        guild = ctx.guild

        if not user:
            user = author
        sharedguilds = {
            guild async for guild in AsyncIter(self.bot.guilds) if user in guild.members
        }
        roles = user.roles[-1:0:-1]
        names, nicks = await self.get_names_and_nicks(user)

        joined_at = user.joined_at
        since_created = (ctx.message.created_at - user.created_at).days
        if joined_at is not None:
            since_joined = (ctx.message.created_at - joined_at).days
            user_joined = joined_at.strftime("%d %b %Y %H:%M")
        else:
            since_joined = "?"
            user_joined = "Unknown"
        user_created = user.created_at.strftime("%d %b %Y %H:%M")
        voice_state = user.voice
        member_number = (
            sorted(guild.members, key=lambda m: m.joined_at or ctx.message.created_at).index(user)
            + 1
        )

        created_on = "{}\n({} days ago)".format(user_created, since_created)
        joined_on = "{}\n({} days ago)".format(user_joined, since_joined)
        if user.is_on_mobile():
            statusemoji = (
                self.status_emojis["mobile"]
                if self.status_emojis["mobile"]
                else "\N{MOBILE PHONE}"
            )
        elif any(a.type is discord.ActivityType.streaming for a in user.activities):
            statusemoji = (
                self.status_emojis["streaming"]
                if self.status_emojis["streaming"]
                else "\N{LARGE PURPLE CIRCLE}"
            )
        elif user.status.name == "online":
            statusemoji = (
                self.status_emojis["online"]
                if self.status_emojis["online"]
                else "\N{LARGE GREEN CIRCLE}"
            )
        elif user.status.name == "offline":
            statusemoji = (
                self.status_emojis["offline"]
                if self.status_emojis["offline"]
                else "\N{MEDIUM WHITE CIRCLE}"
            )
        elif user.status.name == "dnd":
            statusemoji = (
                self.status_emojis["dnd"] if self.status_emojis["dnd"] else "\N{LARGE RED CIRCLE}"
            )
        elif user.status.name == "idle":
            statusemoji = (
                self.status_emojis["away"]
                if self.status_emojis["away"]
                else "\N{LARGE ORANGE CIRCLE}"
            )
        activity = "Chilling in {} status".format(user.status)
        status_string = self.get_status_string(user)

        if roles:

            role_str = ", ".join([x.mention for x in roles])
            # 400 BAD REQUEST (error code: 50035): Invalid Form Body
            # In embed.fields.2.value: Must be 1024 or fewer in length.
            if len(role_str) > 1024:
                # Alternative string building time.
                # This is not the most optimal, but if you're hitting this, you are losing more time
                # to every single check running on users than the occasional user info invoke
                # We don't start by building this way, since the number of times we hit this should be
                # infintesimally small compared to when we don't across all uses of Red.
                continuation_string = (
                    "and {numeric_number} more roles not displayed due to embed limits."
                )

                available_length = 1024 - len(continuation_string)  # do not attempt to tweak, i18n

                role_chunks = []
                remaining_roles = 0

                for r in roles:
                    chunk = f"{r.mention}, "
                    chunk_size = len(chunk)

                    if chunk_size < available_length:
                        available_length -= chunk_size
                        role_chunks.append(chunk)
                    else:
                        remaining_roles += 1

                role_chunks.append(continuation_string.format(numeric_number=remaining_roles))

                role_str = "".join(role_chunks)

        else:
            role_str = None

        data = discord.Embed(
            description=(status_string or activity) + f"\n\n{len(sharedguilds)} shared servers.",
            colour=user.colour,
        )

        data.add_field(name="Joined Discord on", value=created_on)
        data.add_field(name="Joined this server on", value=joined_on)
        if role_str is not None:
            data.add_field(name="Roles", value=role_str, inline=False)
        if names:
            # May need sanitizing later, but mentions do not ping in embeds currently
            val = filter_invites(", ".join(names))
            data.add_field(name="Previous Names", value=val, inline=False)
        if nicks:
            # May need sanitizing later, but mentions do not ping in embeds currently
            val = filter_invites(", ".join(nicks))
            data.add_field(name="Previous Nicknames", value=val, inline=False)
        if voice_state and voice_state.channel:
            data.add_field(
                name="Current voice channel",
                value="{0.mention} ID: {0.id}".format(voice_state.channel),
                inline=False,
            )
        data.set_footer(text="Member #{} | User ID: {}".format(member_number, user.id))

        name = str(user)
        name = " ~ ".join((name, user.nick)) if user.nick else name
        name = filter_invites(name)

        avatar = user.avatar_url_as(static_format="png")
        data.title = f"{statusemoji} {name}"
        data.set_thumbnail(url=avatar)

        flags = [f.name for f in user.public_flags.all()]
        badges = ""
        for badge in sorted(flags):
            if badge == "verified_bot":
                emoji1 = discord.utils.get(self.bot.emojis, id=EMOJIS["verified_bot"])
                emoji2 = discord.utils.get(self.bot.emojis, id=EMOJIS["verified_bot2"])
                if emoji1:
                    emoji = f"{emoji1}{emoji2}"
                else:
                    emoji = None
            else:
                emoji = discord.utils.get(self.bot.emojis, id=EMOJIS[badge])
            if emoji:
                badges += f"{emoji} {badge.replace('_', ' ').title()}\n"
            else:
                badges += f"\N{BLACK QUESTION MARK ORNAMENT}\N{VARIATION SELECTOR-16} {badge.replace('_', ' ').title()}\n"
        if badges:
            data.add_field(name="Badges", value=badges)
        bankstat = f"**Bank**: {str(humanize_number(await bank.get_balance(user)))} {await bank.get_currency_name(ctx.guild)}\n"
        if "Unbelievaboat" in self.bot.cogs:
            cog = self.bot.get_cog("Unbelievaboat")
            state = await cog.walletdisabledcheck(ctx)
            if not state:
                balance = await cog.walletbalance(user)
                bankstat += f"**Wallet**: {str(humanize_number(balance))} {await bank.get_currency_name(ctx.guild)}"
        data.add_field(name="Balance", value=bankstat)
        await ctx.send(embed=data)
