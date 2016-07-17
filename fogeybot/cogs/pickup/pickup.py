import itertools
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

    def remove_player(self, name):
        for player in self._players:
            if player.name == name:
                self._players.remove(player)
                break

    @property
    def teams(self):
        if len(self._players) < 2:
            raise ValueError("need at least two players")
        if (len(self._players) % 2) != 0:
            raise ValueError("need an even number of players")

        target_team_mmr = 0
        for player in self._players:
            target_team_mmr += player.mmr
        target_team_mmr /= 2

        team1 = []
        team1_mmr = 0

        for possibility in itertools.combinations(self._players, int(len(self._players) / 2)):
            team_mmr = 0
            for p in possibility:
                team_mmr += p.mmr

            if team_mmr > team1_mmr and team_mmr <= target_team_mmr:
                team1 = possibility
                team1_mmr = team_mmr

        team2 = [p for p in self._players if p not in team1]

        return Team(team1), Team(team2)


class Team(object):
    def __init__(self, players):
        self.members = [p.name for p in players]
        self.mean_mmr = int(statistics.mean([p.mmr for p in players]))


class Player(object):
    def __init__(self, name, mmr):
        self.name = name
        self.mmr = mmr

    def __eq__(self, rhs):
        if not isinstance(rhs, Player):
            return False

        return self.name == rhs.name and self.mmr == rhs.mmr

    def __str__(self):
        return "<Player name={}, mmr={}>" % (self.name, self.mmr)
