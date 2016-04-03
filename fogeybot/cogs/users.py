from discord.ext.commands import command

class UserCommands(object):
    def __init__(self, bot, api, db):
        self.bot = bot
        self.api = api
        self.db = db

    @command(description="Registers/updates your battle tag", pass_context=True)
    async def register(self, ctx, battletag: str):
        if '#' not in battletag:
            await self.bot.reply("bad battle tag format, it should look like this: `MrCool#123`")
            return

        mmr = None
        try:
            info = await self.api.get_mmr(battletag)
            mmr = info.mmr

            if info.present:
                msg = "Registration successful\n"
            else:
                msg = "Unable to find `{}` via HotsLogs; either your profile is private, or you made a typo\n".format(battletag)
                msg += "If you made a typo: simply type `!register battletag#123` again\n"
                msg += "If your profile is private: you will need to specify your MMR each time you `!joinpickup`, or make it public"

        except APIError:
            msg = "Registration succeeded, but I was unable to verify your battle tag with HotsLogs\n"
            mmr = None

        await self.db.register_battle_tag(ctx.message.author.id, battletag, mmr)
        await self.bot.reply(msg)

    @command(description="Shows your registered battle tags, if any", pass_context=True)
    async def registrationstatus(self, ctx):
        user_info = await self.db.lookup_battle_tag(ctx.message.author.id)
        if user_info:
            await self.bot.reply("Registered battle tag: `{}`, MMR: {}".format(user_info['battle_tag'], user_info.get('mmr', "(none)")))
        else:
            await self.bot.reply("Battle tag not found")

    @command(description="Unregisters your battle tag", pass_context=True)
    async def unregister(self, ctx):
        await self.db.unregister_battle_tag(ctx.message.author.id)

        await self.bot.reply("Registration removed")

