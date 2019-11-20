from marketbot import util

async def get_profile(ticker):
    profile = util.fetch_json("https://financialmodelingprep.com/api/v3/company/profile/" + ticker)
    return profile

