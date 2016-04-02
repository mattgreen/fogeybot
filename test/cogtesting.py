import asyncio

def invoke_cog_command(cog, cmd, *args):
    method = getattr(cog, cmd).callback
    asyncio.get_event_loop().run_until_complete(method(cog, *args))

class MockAPI(object):
    def __init__(self, maps):
        self.maps = maps

    async def get_maps(self):
        return self.maps


class MockBot(object):
    def __init__(self):
        self.messages = []

    async def say(self, message):
        self.messages.append(message)


class MockDB(object):
    pass
