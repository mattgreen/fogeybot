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
            return None

        rankings = response.get("LeaderboardRankings")
        if not rankings:
            return None

        profile = {}
        for ranking in rankings:
            if ranking["GameMode"] == "QuickMatch":
                profile["qm"] = ranking["CurrentMMR"]
            elif ranking["GameMode"] == "HeroLeague":
                profile["hl"] = ranking["CurrentMMR"]

        return profile
