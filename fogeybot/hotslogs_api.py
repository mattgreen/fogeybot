import aiohttp

from .errors import APIError

class HotsLogsAPI(object):
    async def get_maps(self):
        try:
            async with aiohttp.get("https://www.hotslogs.com/API/Data/Maps") as response:
                maps = await response.json()
                return [m["PrimaryName"] for m in maps]

        except aiohttp.ClientError:
            raise APIError()

    async def get_mmr(self, tag):
        if "#" not in tag:
            raise ValueError("battle tag must include '#'")

        try:
            async with aiohttp.get("https://www.hotslogs.com/API/Players/1/" + tag.replace("#", "_")) as r:
                response = await r.json()
        except aiohttp.ClientError:
            raise APIError()

        if not response:
            return MMRInfo(MMRInfo.NO_INFO)

        rankings = response.get("LeaderboardRankings")
        if not rankings:
            return MMRInfo(MMRInfo.NO_INFO)

        qm_mmr = 0
        hl_mmr = 0

        for ranking in rankings:
            if ranking["GameMode"] == "QuickMatch":
                qm_mmr = ranking["CurrentMMR"]
            elif ranking["GameMode"] == "HeroLeague":
                hl_mmr = ranking["CurrentMMR"]

        return MMRInfo(MMRInfo.PRESENT, qm_mmr, hl_mmr)


class MMRInfo(object):
    NO_INFO = "not-found"
    PRESENT = "ok"

    def __init__(self, status, qm_mmr=0, hl_mmr=0):
        self.status = status
        self.qm_mmr = qm_mmr
        self.hl_mmr = hl_mmr

    @property
    def mmr(self):
        return max(self.qm_mmr, self.hl_mmr)

    @property
    def present(self):
        return self.status == self.PRESENT

