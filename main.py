from discord.ext import commands
import discord
import config


class TheEmpireBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="&", description=f"The Empire Bot",
                         activity=discord.Activity(type=discord.ActivityType.watching, name="Shade"))
        self.ext = ['cogs.admin', 'cogs.general']
        self.task = self.loop.create_task(self.task())
        self.load_extension('jishaku')
        self.colour = 0x00ff00

    def run(self, *args, **kwargs):
        super().run(config.token)

    def close(self):
        super().close()

    async def on_ready(self):
        print("TEB is online.")

    async def task(self):
        await self.wait_until_ready()
        for x in self.ext:
            try:
                self.load_extension(x)
            except Exception as error:
                print(error)



bot = TheEmpireBot()
bot.run()
