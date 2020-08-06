from discord.ext import commands
from humanize import naturaltime as nt
from datetime import datetime as dt
import discord
import itertools


class TEBHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__(command_attrs={
            'help': 'Info about the bot, a command, or a category.'
        })

    def get_command_signature(self, command):
        parent = command.full_parent_name
        if len(command.aliases) > 0:
            fmt = f'{command.name}'
            if parent:
                fmt = f'{parent} {fmt}'
            alias = fmt
        else:
            alias = command.name if not parent else f'{parent} {command.name}'
        return f'{self.clean_prefix}{alias} {command.signature}'

    async def send_bot_help(self, mapping):
        def key(c):
            return c.cog_name or "Uncategorized Commands"

        embed = discord.Embed(colour=self.context.bot.colour)
        n = '\n'
        embed.set_author(name="COMMAND HELP",
                         icon_url="https://images-ext-2.discordapp.net/external/sD41T-9ffMh7zbYSkkuiPVQM-Kb_bTtZbBJ_5IyDZH8/https/lh3.googleusercontent.com/-tJUZwn7QYXg/XyfEX7JY1OI/AAAAAAAAAEw/wieq0NCZufkF1SSQw5KELk7_kb1IsBJrQCLcBGAsYHQ/s1600/1596441692417296-1.png")
        entries = await self.filter_commands(self.context.bot.commands, key=key, sort=True)
        embed.description = f"{self.context.bot.description}\n"
        for ext, cmds in itertools.groupby(entries, key=key):
            embed.description += f"**{ext}**\n{f'{n}'.join([f'> **{self.get_command_signature(cmd)}** - {cmd.help}' for cmd in cmds])}\n"
        await self.context.send(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(colour=self.context.bot.colour)
        embed.title = self.get_command_signature(command)
        embed.description = command.help or "No help provided"
        if command.aliases:
            embed.add_field(name=f"Aliases", value=f"{', '.join([f'`{command}`' for command in command.aliases])}")
        await self.context.send(embed=embed)

    async def send_group_help(self, group):
        embed = discord.Embed(colour=self.context.bot.colour)
        embed.title = self.get_command_signature(group)
        embed.description = group.help or "No help provided"
        if group.aliases:
            embed.add_field(name=f"Aliases", value=f"{', '.join([f'`{command}`' for command in group.aliases])}")
        if isinstance(group, commands.Group):
            embed.add_field(name=f"Subcommands", value=f"{', '.join([f'`{command}`' for command in group.commands])}")
        await self.context.send(embed=embed)


class General(commands.Cog):
    """General commands"""

    def __init__(self, bot):
        self.bot = bot
        self._original_help_command = bot.help_command
        bot.help_command = TEBHelpCommand()
        bot.help_command.cog = self

    def cog_unload(self):
        """
        ah yes, this.
        :return:
        """
        self.bot.help_command = self._original_help_command


    @commands.command()
    async def takbir(self, ctx):
        """Shout Allah hu Akbar"""
        await ctx.send("‎ٱللَّٰهُ أَكْبَرُ")

    @commands.command(aliases=['av'])
    async def avatar(self, ctx, *, member: discord.Member = None):
        """Shows your avatar"""
        member = member or ctx.author
        avatar_url = member.avatar_url_as(static_format='png', size=4096)
        embed = discord.Embed(colour=self.bot.colour)
        embed.title = f"{member}'s Avatar"
        embed.set_thumbnail(url=avatar_url)
        embed.set_image(url=avatar_url)
        embed.description = f"[Click Here]({avatar_url})"
        await ctx.send(embed=embed)


    @commands.command(aliases=['ui', 'user'])
    async def userinfo(self, ctx, *, member: discord.Member = None):
        """Shows you userinfo"""
        member = member or ctx.author
        embed = discord.Embed(colour=self.bot.colour)
        sl = {
            discord.Status.online: "<:online:726127263401246832>",
            discord.Status.offline: "<:offline:726127263203983440>",
            discord.Status.idle: "<:idle:726127192165187594>",
            discord.Status.dnd: "<:dnd:726127192001478746>"
        }
        td = {
            True: '<:bot:703728026512392312>\n',
            False: ''
        }
        embed.title = f"{member}{sl.get(member.status)}"
        embed.set_thumbnail(url=member.avatar_url_as(static_format='png'))
        embed.description = f"{td[member.bot]}"
        embed.description += f"ID: **{member.id}**\n"
        embed.description += f"Created Account: **{nt(dt.utcnow()-member.created_at)}**\n"
        embed.description += f"Joined Guild: **{nt(dt.utcnow()-member.joined_at)}**\n"
        if len(member.roles) == 1 and member.roles[0].id == ctx.guild.id:
            pass
        else:
            embed.description += f"Top Role: {member.top_role.mention}"
        await ctx.send(embed=embed)


    @commands.command()
    async def date(self, ctx):
        """Shows the current date"""
        embed = discord.Embed(colour=self.bot.colour)
        embed.title = "Time (UTC)"
        time = ctx.message.created_at.strftime("%A %B %d, %Y at %I:%M %p")
        embed.description = time
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(General(bot))
