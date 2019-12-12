from marketbot import util
import os
import logging
import re

logger = logging.getLogger()

headers = {
    'APCA-API-KEY-ID':os.environ.get("ALPACA_ID") or logger.warning("You must set the ALPACA_ID environment variable"),
    'APCA-API-SECRET-KEY':os.environ.get("ALPACA_SECRET") or logger.warning("You must set the ALPACA_SECRET environment variable"),
}

async def get_profile(ticker):
    profile = await util.fetch_json("https://financialmodelingprep.com/api/v3/company/profile/" + ticker)
    return profile['profile'] if "profile" in profile else None

async def get_rating(ticker):
    rating = await util.fetch_json("https://financialmodelingprep.com/api/v3/company/rating/" + ticker)
    return rating['rating'] if "rating" in rating else None

async def get_asset(symbol):
    asset = await util.fetch_json("https://api.alpaca.markets/v2/assets/" + symbol, headers)
    return asset


async def get_quote(symbol):
    symbol = symbol.upper()
    params = {
        'symbols':symbol,
        'limit': 1
    }
    price = await util.fetch_json("https://data.alpaca.markets/v1/bars/day", headers, params)
    
    try:
        close = price[symbol][0]['c']
        open = price[symbol][0]['o']
        change = (close - open) / close
        return {
            'price':round(close, 2),
            'change%': f"{round( change * 100, 2)}%"
        }
    except Exception as e: 
        logger.error(f"{e}: Could not fetch quote for [{symbol}]: JSON {price}")


async def get_change(symbol, limit, timespan):
    params = {
        'symbols':symbol,
        'limit': limit
    }
    prices = await util.fetch_json("https://data.alpaca.markets/v1/bars/" + timespan, headers, params)
    try:
        s = prices[symbol]
        begin = s[0]['c']
        end = s[-1]['c']

        print(f"BEGIN: {begin}, END: {end}")
        change = ( end - begin ) / end
        return {
            "change%": round(change * 100, 2),
            "period":f"{limit} {timespan}",
            "current":end
        }
    except Exception as e:
        logger.error(e)