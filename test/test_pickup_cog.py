import unittest

from fogeybot.cogs.pickup.cog import PickupCommands
from cogtesting import *

class TestPickupCog(unittest.TestCase):
    def setUp(self):
        self.api = MockAPI(["Infernal Shrines"])
        self.bot = MockBot()
        self.db = MockDB()
        self.cog = PickupCommands(self.bot, self.api, self.db, None)

    def test_randommap(self):
        invoke_cog_command(self.cog, 'randommap', None)

        assert self.bot.messages
        assert "Infernal Shrines" in self.bot.messages[0]
