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
        info = self.run(self.api.get_mmr("benthor#1644"))

        assert info.present
        assert info.qm_mmr > 0
        assert info.hl_mmr > 0

    def test_get_mmr_not_found(self):
        info = self.run(self.api.get_mmr("benthor#1645"))

        assert not info.present
