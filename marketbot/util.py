import aiohttp
import json
import logging

logger = logging.getLogger()


async def fetch(url, headers=None, params=None):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            return await response.text()


async def fetch_json(url, headers=None, params=None): 
    text = await fetch(url, headers=headers, params=params)
    return json.loads(text)




async def opt_webhook_send_embed(channel, embed):
    webhooks = None
    try:
        webhooks = await channel.webhooks()

    except Exception as e:
        logger.error("WH Error:", e)

    if webhooks:
        await webhooks[0].send(embed=embed, username="Ticker Bot", avatar_url="https://www.freeiconspng.com/uploads/stock-exchange-icon-png-1.png")
    else:
        await channel.send(embed=embed)