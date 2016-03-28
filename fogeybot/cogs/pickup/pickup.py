import statistics
import time

class Pickup(object):
    TIMEOUT = 30 * 60

    def __init__(self, now=None):
        if now is None:
            now = time.time()

        self._players = []
        self._updated = now
        self.status_message = None

    @staticmethod
    def inactive():
        return Pickup(0)

    @property
    def active(self):
        return (time.time() - self._updated) < self.TIMEOUT

    def add_player(self, name, mmr, now=None):
        if now is None:
            now = time.time()

        self._updated = now

        if mmr < 400 or mmr > 4500:
            mmr = 1500

        for player in self._players:
            if player.name == name:
                player.mmr = mmr
                return

        self._players.append(Player(name, mmr))

    @property
    def players(self):
        return list(self._players)

    @property
    def teams(self):
        if len(self._players) < 2:
            raise ValueError("need at least two players")
        if (len(self._players) % 2) != 0:
            raise ValueError("need an even number of players")

        team1 = []
        team2 = []

        players_by_mmr = sorted(self._players, key=lambda p: p.mmr)

        while players_by_mmr:
            p1 = players_by_mmr.pop()
            p2 = players_by_mmr.pop()

            if len(team1) % 2 == 0:
                team1.append(p1)
                team2.append(p2)
            else:
                team1.append(p2)
                team2.append(p1)

        return Team(team1), Team(team2)


class Team(object):
    def __init__(self, players):
        self.members = [p.name for p in players]
        self.mean_mmr = int(statistics.mean([p.mmr for p in players]))


class Player(object):
    def __init__(self, name, mmr):
        self.name = name
        self.mmr = mmr
