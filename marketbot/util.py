import aiohttp
import json
import logging

logger = logging.getLogger()


async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def fetch_json(url): 
    text = await fetch(url)
    return json.loads(text)




async def opt_webhook_send_embed(channel, embed):
    webhooks = None
    try:
        webhooks = await channel.webhooks()

    except Exception as e:
        logger.error("WH Error:", e)

    if webhooks:
        await webhooks[0].send(embed=embed)
    else:
        await channel.send(embed=embed)