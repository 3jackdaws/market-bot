from marketbot import Bot, Message, util
from discord import Embed, Webhook, TextChannel
from . import api
import re
import logging
import asyncio
from time import time

logger = logging.getLogger("BASE.TICKER")

TICKER_PATTERN = r'\[([a-zA-Z]+)\]'
EXPRESSION_PATTERN = TICKER_PATTERN + r'([.][a-zA-Z]+_[a-zA-Z]+\([]\))?'


class Stock:
    regex = re.compile(EXPRESSION_PATTERN)
    rh_stock_url = "https://robinhood.com/stocks/"
    def __init__(self, ticker):
        self.ticker = ticker.upper()

    async def default(self):
        start = time()
        profile, rating = await asyncio.gather(
            api.get_profile(self.ticker), 
            api.get_rating(self.ticker)
        )
        e = Embed(title=profile['companyName'], url=self.rh_stock_url + self.ticker)
        e.color = 6750105
        e.add_field(name="Price", value=profile['price'], inline=True)
        e.add_field(name="Today", value=profile['changesPercentage'], inline=True)
        e.add_field(name="Rating", value=rating['rating'], inline=True)
        end = time()
        logger.info(f"[{self.ticker}].default() executed in {round((end - start) * 1000, 2)}ms")
        return e

    async def test(self, val):
        e = Embed(title="TEST")
        return e





async def manage_stock_object(bot:Bot, message:Message):
    expr = Stock.regex.match(message.content)
    if expr:
        expression = expr.group(0)
        ticker = expr.group(1)
        stock = Stock(ticker)
        expression = expression.replace(f"[{ticker}]", "s", 1)

        try:
            output = eval(expression, {'s':stock})
            if asyncio.iscoroutine(output):
                output = await output
            channel = bot.get_channel(message.channel.id)  # type: TextChannel
            if isinstance(output, Embed):
                embed = output
            elif isinstance(output, Stock):
                embed = await output.default()
            else:
                return
            
            await util.opt_webhook_send_embed(channel, embed)

        except Exception as e:
            logger.error("MSO Error: " + str(e))



