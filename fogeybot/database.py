from motor.motor_asyncio import AsyncIOMotorClient

class Database(object):
    def __init__(self, uri):
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client['fogeybot']
        self.collection = self.db['users']

    async def test_connection(self):
        await self.collection.count()

    async def lookup_battle_tag(self, discord_id):
        doc = await self.collection.find_one({'_id': {'$eq': discord_id}})
        if doc is None:
            return None

        return doc['battle_tag']

    async def register_battle_tag(self, discord_id, battle_tag):
        existing = await self.collection.find_one({'_id': {'$eq': discord_id}})
        if existing:
            await self.collection.update({'_id': discord_id}, {'$set': {'battle_tag': battle_tag}})
        else:
            await self.collection.insert({'_id': discord_id, 'battle_tag': battle_tag})

    async def unregister_battle_tag(self, discord_id):
        await self.collection.remove({'_id': {'$eq': discord_id}})
