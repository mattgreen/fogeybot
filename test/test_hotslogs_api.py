import asyncio
import unittest

from fogeybot.hotslogs_api import HotsLogsAPI

class TestHotsLogsAPI(unittest.TestCase):
    def setUp(self):
        self.api = HotsLogsAPI()
        self.run = asyncio.get_event_loop().run_until_complete

    def test_get_maps(self):
        maps = self.run(self.api.get_maps())
        self.assertTrue(len(maps) > 5)

    def test_get_mmr(self):
        mmrs = self.run(self.api.get_mmr("benthor#1644"))
        self.assertTrue("qm" in mmrs and "hl" in mmrs)

    def test_get_mmr_not_found(self):
        mmrs = self.run(self.api.get_mmr("benthor#1645"))
        self.assertIsNone(mmrs)
