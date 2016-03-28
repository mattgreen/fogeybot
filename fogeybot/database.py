import aioredis

class Database(object):
    BATTLETAG_PREFIX = "btag"

    def __init__(self, hostname, port, password):
        self._pool = None
        self._address = (hostname, port)
        self._password = password

    async def connect(self):
        self._pool = await aioredis.create_pool(self._address,
                                                password=self._password,
                                                minsize=2,
                                                maxsize=5)

    async def lookup_battle_tag(self, discord_id):
        with (await self._pool) as redis:
            tag = await redis.get("{}-{}".format(self.BATTLETAG_PREFIX, discord_id))
            if tag is None:
                return None

            return tag.decode('utf-8')

    async def register_battle_tag(self, discord_id, battle_tag):
        with (await self._pool) as redis:
            await redis.set("{}-{}".format(self.BATTLETAG_PREFIX, discord_id), battle_tag)

    async def unregister_battle_tag(self, discord_id):
        with (await self._pool) as redis:
            await redis.delete("{}-{}".format(self.BATTLETAG_PREFIX, discord_id))
