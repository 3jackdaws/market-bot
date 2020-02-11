from marketbot import Bot, Message, util
from discord import Embed, Webhook, TextChannel
from . import api
import re
import logging
import asyncio
from time import time

logger = logging.getLogger("BASE.TICKER")

TICKER_PATTERN = r'\[([a-zA-Z]+)\]'
EXPRESSION_PATTERN = TICKER_PATTERN + r'([.][a-z]+\(([^_()]*)\))?'

def get_embed(title, url=None, fields=[], color=6750105):
    e = Embed(title=title, url=url)
    e.color = color
    for field in fields:
        e.add_field(name=field[0], value=field[1], inline=field[2] if len(field) > 2 else True)
    return e



class Stock:
    regex = re.compile(EXPRESSION_PATTERN)
    rh_stock_url = "https://robinhood.com/stocks/"
    def __init__(self, ticker):
        self.ticker = ticker.upper()

    async def default(self):
        asset, quote, rating = await asyncio.gather(
            api.get_asset(self.ticker), 
            api.get_quote(self.ticker),
            api.get_rating(self.ticker)
        )

        # print(asset)
        # print(quote)
        # print(rating)

        e = get_embed(
            asset['name'],
            self.rh_stock_url + self.ticker,
            fields=[
                ("Price", quote['price']),
                ("Change (today)", quote['change%']),
                ("Rating", rating['rating'] if rating else "N/A"),
            ]
        )
        return e

    async def change(self, timespan="7 d"):
        start = time()
        matches = re.match("([0-9]+) ?(m|d)", timespan)
        if matches:
            limit = matches.group(1) or "7"
            timespan = matches.group(2) or "d"
        else:
            limit = "7"
            timespan = "d"
        
        try:
            timespan = {
                "m":"minute",
                "d":"day",
            }[timespan]
        except:
            timespan = "day"
        if int(limit) >= 1000:
            return "Timespan limit must be less than 1000."
            
        print(limit, timespan)
        change, asset = await asyncio.gather(
            api.get_change(self.ticker, limit, timespan),
            api.get_asset(self.ticker)
        )
        e = get_embed(
            asset['name'],
            self.rh_stock_url + self.ticker,
            fields=[
                ("Price", change['current']),
                (f"Change ({change['period']})", f"{change['change%']}%"),
            ])
        end = time()
        
        return e
        
    
        





async def manage_stock_object(bot:Bot, message:Message):
    expr = Stock.regex.search(message.content)
    
    if expr:
        
        expression = expr.group(0)
        logger.info(f'[{message.author.name}]: "{message.content}" - Expression: {expression}')
        ticker = expr.group(1)
        arguments = expr.group(3)

        stock = Stock(ticker)
        stock_expr = expression.replace(f"[{ticker}]", "s", 1)
        if arguments:
            stock_expr = stock_expr.replace(arguments, f"'{arguments}'")

        try:
            start = time()
            # logger.info("Evaluating " + stock_expr)
            output = eval(stock_expr, {'s':stock})
            if asyncio.iscoroutine(output):
                output = await output
            if isinstance(output, Stock):
                output = await output.default()
            end = time()
            logger.info(f"{expression} executed in {round((end - start) * 1000, 2)}ms")
            channel = bot.get_channel(message.channel.id)  # type: TextChannel
            if isinstance(output, Embed):
                await util.opt_webhook_send_embed(channel, output)
            elif isinstance(output, str):
                await channel.send(output)

        except Exception as e:
            logger.error("MSO Error: " + str(e))



