import unittest

from fogeybot.pickup import Pickup

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

    def test_active(self):
        self.assertFalse(Pickup(5).active)
