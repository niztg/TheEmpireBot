from discord.ext import commands
import discord
import os

reload = "🔄"
null = "-"

class Admin(commands.Cog):
    """Commands that can only be run by admins/owners"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Reloads Cogs", aliases=['rl'])
    @commands.is_owner()
    async def reload(self, ctx, *extension):
        if not extension:
            for file in self.bot.ext:
                try:
                    self.bot.reload_extension(file)
                except:
                    continue
            embed = discord.Embed(
                description="\n".join([f"{reload} `{f}`" for f in self.bot.ext]),
                colour=self.bot.colour)
            await ctx.send(embed=embed)
            await ctx.message.add_reaction(emoji="☑️")

        else:
            cogs = [f[:-3] for f in os.listdir('cogs') if f.endswith('.py')]
            for i in extension:
                if i not in cogs:
                    return await ctx.send(f"**{i}** is not a valid cog!")

            for f in extension:
                self.bot.reload_extension(f'cogs.{f}')
            a = []
            for x in cogs:
                if x in extension:
                    a.append(f"{reload} `cogs.{x}`")
                else:
                    a.append(f"{null} `ext.{x}`")

            await ctx.message.add_reaction(emoji="☑️")
            await ctx.send(embed=discord.Embed(description="\n".join(a), colour=self.bot.colour))

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        """Shut down the bot"""
        self.bot.close()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def poll(self, ctx, *, poll):
        """Start a poll"""
        embed = discord.Embed(colour=self.bot.colour)
        embed.title = "Poll:"
        embed.description = poll
        embed.set_footer(text=f"✅ if you agree, ❎ if you disagree.")
        msg = await ctx.send(embed=embed)
        for i in ['✅', '❎']:
            await msg.add_reaction(i)


def setup(bot):
    bot.add_cog(Admin(bot))
