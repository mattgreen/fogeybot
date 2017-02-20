import unittest

from fogeybot.cogs.pickup.pickup import Pickup

class TestPickup(unittest.TestCase):
    def setUp(self):
        self.pickup = Pickup()

    def test_starts_with_no_players(self):
        self.assertEqual(len(self.pickup.players), 0)

    def test_add_player(self):
        self.pickup.add_player("name", 1700)
        self.assertEqual(len(self.pickup.players), 1)

    def test_add_players(self):
        self.pickup.add_player("name", 1700)
        self.pickup.add_player("name2", 1700)

        self.assertEqual(len(self.pickup.players), 2)

    def test_add_player_clamps_mmr(self):
        self.pickup.add_player("name", 200)

        self.assertTrue(self.pickup.players[0].mmr > 200)

    def test_updates_mmr_of_same_player(self):
        self.pickup.add_player("name", 1700)
        self.pickup.add_player("name", 1800)

        self.assertEqual(len(self.pickup.players), 1)
        self.assertEqual(self.pickup.players[0].mmr, 1800)

    def test_need_two_players_for_teams(self):
        with self.assertRaises(ValueError):
            self.pickup.teams

    def test_need_even_players_for_teams(self):
        self.pickup.add_player("name", 1700)
        self.pickup.add_player("name2", 1700)
        self.pickup.add_player("name3", 1700)

        with self.assertRaises(ValueError):
            self.pickup.teams

    def test_assigns_teams(self):
        self.pickup.add_player("name", 1700)
        self.pickup.add_player("name2", 600)
        self.pickup.add_player("name3", 600)
        self.pickup.add_player("name4", 1700)

        team1, team2 = self.pickup.teams
        self.assertTrue(len(team1.members) == 2)
        self.assertTrue(len(team2.members) == 2)

    def test_calculates_mean_mmr(self):
        self.pickup.add_player("name", 1700)
        self.pickup.add_player("name2", 600)
        self.pickup.add_player("name3", 600)
        self.pickup.add_player("name4", 1700)

        team1, team2 = self.pickup.teams
        self.assertEqual(team1.mean_mmr, team2.mean_mmr)

    def test_sample_data(self):
        self.pickup.add_player("Velvet", 2325)
        self.pickup.add_player("Krezrel", 2268)
        self.pickup.add_player("Zadkiel", 2259)
        self.pickup.add_player("Poe", 2115)
        self.pickup.add_player("BigBeerd", 1892)
        self.pickup.add_player("Kendo", 1845)
        self.pickup.add_player("Gio", 1832)
        self.pickup.add_player("Shadowleaves", 1776)
        self.pickup.add_player("Hulk", 1601)
        self.pickup.add_player("Bray", 1139)

        team1, team2 = self.pickup.teams
        self.assertTrue(abs(team1.mean_mmr - team2.mean_mmr) < 15)

    def test_sample_data2(self):
        self.pickup.add_player("Razoth", 2950)
        self.pickup.add_player("TickleMeOzmo", 2371)
        self.pickup.add_player("Kendo", 1818)
        self.pickup.add_player("katrinalorien", 1738)
        self.pickup.add_player("Cercie", 1719)
        self.pickup.add_player("VelveThunder", 2439)
        self.pickup.add_player("syrowatts", 2388)
        self.pickup.add_player("drivelikebrazil", 1799)
        self.pickup.add_player("TOFTS", 1761)
        self.pickup.add_player("bray", 1269)

        team1, team2 = self.pickup.teams
        self.assertEqual(team1.mean_mmr, team2.mean_mmr)

    def test_selects_captains_and_players(self):
        self.pickup.add_player("Velvet", 2325)
        self.pickup.add_player("Krezrel", 2268)
        self.pickup.add_player("Zadkiel", 2259)
        self.pickup.add_player("Poe", 2115)
        self.pickup.add_player("BigBeerd", 1892)
        self.pickup.add_player("Kendo", 1845)
        self.pickup.add_player("Gio", 1832)
        self.pickup.add_player("Shadowleaves", 1776)
        self.pickup.add_player("Hulk", 1601)
        self.pickup.add_player("Bray", 1139)

        team1, team2 = self.pickup.teams
        self.assertEqual(team1.captain, "Velvet")
        self.assertEqual(len(team1.players), 4)
        self.assertEqual(team2.captain, "Krezrel")
        self.assertEqual(len(team2.players), 4)

    def test_active(self):
        self.assertFalse(Pickup(5).active)

    def test_removes_player(self):
        self.pickup.add_player("bob", 1700)
        self.pickup.remove_player("bob")

        assert len(self.pickup.players) == 0

    def test_removes_nothing_if_not_found(self):
        self.pickup.add_player("bob", 1700)
        self.pickup.remove_player("cindy")

        assert len(self.pickup.players) == 1
