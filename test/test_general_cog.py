import unittest

from fogeybot.cogs.general.cog import GeneralCommands
from cogtesting import *

class TestGeneralCog(unittest.TestCase):
    def setUp(self):
        self.bot = MockBot()
        self.cog = GeneralCommands(self.bot)

    def test_coinflip(self):
        invoke_cog_command(self.cog, 'coinflip')

        assert self.bot.messages
        assert "heads" in self.bot.messages[0] or "tails" in self.bot.messages[0]
