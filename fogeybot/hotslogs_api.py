import aiohttp
import asyncio

class HotsLogsAPI(object):
    async def _get(self, url, timeout=5):
        with aiohttp.ClientSession() as client:
            async with client.get(url) as response:
                return await response.json()

    async def get_maps(self):
        try:
            maps = await self._get("https://www.hotslogs.com/API/Data/Maps")

            return [m["PrimaryName"]
                    for m in maps
                    if "mines" not in m["PrimaryName"].lower()]

        except aiohttp.ClientError:
            raise APIError()

    async def get_mmr(self, tag):
        if "#" not in tag:
            raise ValueError("battle tag must include '#'")

        try:
            response = await self._get("https://www.hotslogs.com/API/Players/1/" + tag.replace("#", "_"))
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


class APIError(Exception):
    pass
