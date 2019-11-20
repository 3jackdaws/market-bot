import aiohttp
import json


async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def fetch_json(url):
    text = await fetch(url)
    return json.loads(text)