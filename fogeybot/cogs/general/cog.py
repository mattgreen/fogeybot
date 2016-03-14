import datetime

from discord.ext.commands import command

class GeneralCommands(object):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.datetime.now()

    @command()
    async def info(self):
        msg = "I am FogeyBot! I help start pickup games, and do other bot-y things.\nFor more information, please see https://github.com/mattgreen/fogeybot"
        await self.bot.reply(msg)

    @command()
    async def uptime(self):
        def timedelta_str(dt):
            days = dt.days
            hours, r = divmod(dt.seconds, 3600)
            minutes, _ = divmod(r, 60)
            if minutes == 1:
                return '{0} days, {1} hours and {2} minute'.format(days, hours, minutes)
            else:
                return '{0} days, {1} hours and {2} minutes'.format(days, hours, minutes)

        await self.bot.reply(timedelta_str(datetime.datetime.now() - self.start_time))

