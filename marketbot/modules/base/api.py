from marketbot import util

async def get_profile(ticker):
    profile = await util.fetch_json("https://financialmodelingprep.com/api/v3/company/profile/" + ticker)
    return profile['profile'] if "profile" in profile else None

async def get_rating(ticker):
    rating = await util.fetch_json("https://financialmodelingprep.com/api/v3/company/rating/" + ticker)
    return rating['rating'] if "rating" in rating else None

